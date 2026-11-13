#!/bin/sh
# Startet Ollama, lädt beim ersten Mal das Basismodell und legt das Stationsmodell an.
set -e
ollama serve &
PID=$!
until ollama list >/dev/null 2>&1; do sleep 1; done

ollama pull "$BASE_MODEL"
sed "s|^FROM .*|FROM $BASE_MODEL|" /station/Modelfile > /tmp/Modelfile
ollama create "$STATION_MODEL" -f /tmp/Modelfile
echo "Inferenz bereit: $STATION_MODEL (Basis $BASE_MODEL)"

wait $PID
