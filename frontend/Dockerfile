FROM python:3.12-slim

# install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app/frontend

# Copier les fichiers nécessaires à l'installation des dépendances
COPY pyproject.toml uv.lock ./

# Installer les dépendances avec uv (inclut maintenant redis)
RUN uv pip install --system --requirements=pyproject.toml

# Copier le code de l'application
COPY frontend/ .

# Exposer le port 8501 (port par défaut de Streamlit)
EXPOSE 8501

# Configuration Streamlit
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Commande pour démarrer Streamlit
CMD ["streamlit", "run", "main.py"]