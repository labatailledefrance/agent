#!/usr/bin/env python3
"""Vérifie les liens des fichiers Markdown de l'espace de travail.

Contrôle les liens relatifs et les URL https://github.com/labatailledefrance/<dépôt>/...
(ramenées aux fichiers locaux du dépôt cloné), fichiers et ancres compris.
Signale aussi les liens relatifs qui sortent de leur dépôt (ils sont cassés
sur GitHub) et les liens vers data/ ou CLAUDE.md.

Usage : verifier-liens.py [racine]   (par défaut : deux dossiers au-dessus de .claude/skills/…)
Code de sortie : 0 si tout va bien, 1 sinon.
"""
import collections
import glob
import os
import re
import sys
import urllib.parse

RACINE = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else
                         os.path.join(os.path.dirname(__file__), '..', '..', '..'))
ORG = 'https://github.com/labatailledefrance/'
# Dépôt GitHub -> dossier local
DEPOTS = {'documentation': 'documentation', 'prototypes': 'prototypes',
          'game': 'game', 'agent': '.claude'}
LIEN = re.compile(r'\[([^\]]*)\]\(([^)\s]+)\)')
# target* : compilation ; modele : gabarits aux liens à compléter (<…>).
EXCLUS = re.compile(r'/(target[^/]*|\.git|node_modules|modele)/')


def ancre(titre):
    """Ancre GitHub d'un titre : minuscules, ponctuation retirée, espaces -> tirets."""
    titre = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', titre)   # liens dans le titre
    titre = re.sub(r'[`*_]', '', titre).strip().lower()
    return re.sub(r'[^\w\- ]', '', titre).replace(' ', '-')


_ancres = {}


def ancres(chemin):
    if chemin not in _ancres:
        texte = re.sub(r'```.*?```', '', open(chemin, encoding='utf-8').read(), flags=re.S)
        vus, res = collections.Counter(), set()
        for t in re.findall(r'^#{1,6} (.*)$', texte, flags=re.M):
            a = ancre(t)
            res.add(a if not vus[a] else f'{a}-{vus[a]}')
            vus[a] += 1
        _ancres[chemin] = res
    return _ancres[chemin]


def depot_de(chemin):
    rel = os.path.relpath(chemin, RACINE).split(os.sep)[0]
    return rel if rel in DEPOTS.values() else None


fichiers = [f for f in glob.glob(os.path.join(RACINE, '**', '*.md'), recursive=True)
            if not EXCLUS.search(f) and '/data/' not in f]
fichiers += [f for f in glob.glob(os.path.join(RACINE, '.claude', '**', '*.md'), recursive=True)
             if f not in fichiers and not EXCLUS.search(f)]

problemes = []
for f in sorted(fichiers):
    d = os.path.dirname(f)
    texte = re.sub(r'```.*?```', '', open(f, encoding='utf-8').read(), flags=re.S)
    texte = re.sub(r'`[^`\n]*`', '', texte)          # code en ligne
    for _, url in LIEN.findall(texte):
        m = re.match(re.escape(ORG) + r'([\w.-]+)(?:/(?:blob|tree)/main/([^#]*))?(#.*)?$', url)
        if m:
            if m.group(1) not in DEPOTS:
                problemes.append((f, url, 'dépôt inconnu'))
                continue
            cible = os.path.join(RACINE, DEPOTS[m.group(1)], urllib.parse.unquote(m.group(2) or ''))
            a = (m.group(3) or '')[1:]
        elif re.match(r'^[a-z]+:', url):
            continue                                      # autre URL externe
        else:
            p, _, a = url.partition('#')
            cible = os.path.normpath(os.path.join(d, urllib.parse.unquote(p))) if p else f
            src = depot_de(f)   # None : fichier local hors dépôt (README de la racine)
            if p and src:
                rel = os.path.relpath(cible, RACINE)
                vers_claude = os.path.basename(cible) == 'CLAUDE.md' and src != '.claude'
                if rel.split(os.sep)[0] == 'data' or vers_claude:
                    problemes.append((f, url, 'lien vers data/ ou CLAUDE.md : mettre le chemin en texte'))
                    continue
                if depot_de(cible) != src:
                    problemes.append((f, url, 'lien relatif qui sort du dépôt : URL GitHub attendue'))
        a = urllib.parse.unquote(a)
        if not os.path.exists(cible):
            problemes.append((f, url, 'fichier absent'))
        elif a and cible.endswith('.md') and a not in ancres(cible):
            problemes.append((f, url, 'ancre absente'))

for f, url, motif in problemes:
    print(f'{os.path.relpath(f, RACINE)} : {motif} : {url}')
print(f'{len(fichiers)} fichiers, {len(problemes)} problème(s)')
sys.exit(1 if problemes else 0)
