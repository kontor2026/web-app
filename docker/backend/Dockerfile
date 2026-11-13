# Backend: Pipeline (FastAPI). Spricht je nach LLM_PROVIDER mit dem Inferenz-Container oder der Claude-API.
FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt
COPY backend/app backend/app
COPY backend/seed backend/seed
# Beispielfotos: für den Foto-Abgleich der Demo-Objekte beim ersten Start.
COPY assets/samples assets/samples
ENV STATION_DATA=/data
VOLUME /data
EXPOSE 8000
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
