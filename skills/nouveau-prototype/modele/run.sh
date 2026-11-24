#!/bin/bash
# P-<XX> — campagne de mesures. Durée : <environ N min>.
# ESSAI=1 ./run.sh : valide toutes les commandes en quelques minutes
# (entrées réduites, résultats dans essai/).
# Rien de lourd en parallèle pendant la campagne.
set -euo pipefail
cd "$(dirname "$0")"
cargo build --release 2>&1 | tail -1
B=target/release/p<XX>-<nom-court>
R=../../data
S=$R/sources
G=$R/generated
O=resultats
[[ ${ESSAI:-0} == 1 ]] && O=essai
mkdir -p $O

# 1. <Scénario>
$B --mode <scenario> --res $O/<fichier>.csv

echo "Campagne terminée : $O/"
