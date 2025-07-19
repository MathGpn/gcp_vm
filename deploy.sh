#!/bin/bash

# Script de déploiement pour GCP VM
echo "🚀 Démarrage du déploiement..."

# Vérifier si Docker est installé
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé. Installation en cours..."
    
    # Installation de Docker sur Ubuntu/Debian
    sudo apt-get update
    sudo apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release
    
    # Ajouter la clé GPG officielle de Docker
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    
    # Ajouter le repository Docker
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    # Installer Docker
    sudo apt-get update
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io
    
    echo "✅ Docker installé avec succès"
fi

# Vérifier si Docker Compose est installé
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose n'est pas installé. Installation en cours..."
    
    # Installation de Docker Compose
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    
    echo "✅ Docker Compose installé avec succès"
fi

# Ajouter l'utilisateur actuel au groupe docker
sudo usermod -aG docker $USER

# Arrêter les conteneurs existants s'ils existent
echo "🛑 Arrêt des conteneurs existants..."
sudo docker-compose down --remove-orphans

# Construire et démarrer les conteneurs
echo "🏗️  Construction et démarrage des conteneurs..."
sudo docker-compose up --build -d

# Attendre que les services soient prêts
echo "⏳ Attente que les services soient prêts..."
sleep 30

# Vérifier l'état des conteneurs
echo "📊 État des conteneurs:"
sudo docker-compose ps

# Afficher les logs
echo "📝 Derniers logs du backend:"
sudo docker-compose logs --tail=20 backend

echo "📝 Derniers logs du frontend:"
sudo docker-compose logs --tail=20 frontend

# Test de connectivité
echo "🧪 Test de connectivité..."

# Test API Backend
if curl -f http://localhost:8000/health &> /dev/null; then
    echo "✅ API Backend accessible sur http://localhost:8000"
    echo "📚 Documentation API: http://localhost:8000/docs"
else
    echo "❌ API Backend non accessible"
fi

# Test Frontend
if curl -f http://localhost:8501 &> /dev/null; then
    echo "✅ Frontend accessible sur http://localhost:8501"
else
    echo "❌ Frontend non accessible"
fi

# Configuration du firewall (optionnel)
echo "🔥 Configuration du firewall..."
sudo ufw allow 8000/tcp comment 'FastAPI Backend'
sudo ufw allow 8501/tcp comment 'Streamlit Frontend'
sudo ufw allow 5432/tcp comment 'PostgreSQL Database'

echo ""
echo "🎉 Déploiement terminé!"
echo "📱 Frontend Streamlit: http://$(curl -s ifconfig.me):8501"
echo "🔗 API FastAPI: http://$(curl -s ifconfig.me):8000"
echo "📚 Documentation API: http://$(curl -s ifconfig.me):8000/docs"
echo ""
echo "Pour voir les logs en temps réel:"
echo "sudo docker-compose logs -f"
echo ""
echo "Pour arrêter l'application:"
echo "sudo docker-compose down"