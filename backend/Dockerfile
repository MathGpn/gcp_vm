FROM python:3.12-slim

# install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app/backend

# Copier les fichiers nécessaires à l'installation des dépendances
COPY pyproject.toml uv.lock ./

# Installer les dépendances avec uv (inclut maintenant redis)
RUN uv pip install --system --requirements=pyproject.toml

# Copier le code de l'application
COPY backend/ .

# Exposer le port 8000
EXPOSE 8000

# Commande pour démarrer l'application
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]