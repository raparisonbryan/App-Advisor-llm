# === 🏗️ STAGE 1: build (install only what's needed) ===
FROM python:3.12-slim AS builder

WORKDIR /app

# Copie uniquement les requirements
COPY requirements.txt .

# Installer seulement ce qu’il faut pour build les deps Python
RUN apt-get update && apt-get install -y \
    build-essential git \
    && pip install --upgrade pip \
    && pip install --prefix=/install --no-cache-dir -r requirements.txt

# === 🚀 STAGE 2: runtime allégé ===
FROM python:3.12-slim

WORKDIR /app

# Copier les dépendances installées par pip
COPY --from=builder /install /usr/local

# Copier le code source uniquement
COPY . .

# Supprimer les cache pip et apt
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /root/.cache

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
