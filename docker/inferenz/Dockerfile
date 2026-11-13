# Inferenz: Ollama mit dem Stationsmodell (Qwen3-VL, größerer Kontext, siehe backend/Modelfile).
# Die Modellgewichte (ca. 3,3 GB) lädt der Container beim ersten Start in das Volume.
FROM ollama/ollama:0.40.14
COPY backend/Modelfile /station/Modelfile
COPY docker/inferenz/entrypoint.sh /station/entrypoint.sh
ENV BASE_MODEL=qwen3-vl:4b \
    STATION_MODEL=station-vl
HEALTHCHECK --interval=15s --timeout=5s --start-period=30s --retries=200 \
    CMD ollama show "$STATION_MODEL" >/dev/null 2>&1 || exit 1
ENTRYPOINT ["/bin/sh", "/station/entrypoint.sh"]
