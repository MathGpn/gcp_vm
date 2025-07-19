import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import os

# Configuration de la page
st.set_page_config(
    page_title="Mon Application",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# URL de l'API (utilise une variable d'environnement ou localhost par défaut)
API_BASE_URL = os.getenv("API_URL", "http://localhost:8000")

# Initialiser le session state
if 'items_cache' not in st.session_state:
    st.session_state.items_cache = []
if 'last_update' not in st.session_state:
    st.session_state.last_update = datetime.now()
if 'force_refresh' not in st.session_state:
    st.session_state.force_refresh = True

def check_api_health():
    """Vérifier si l'API est accessible"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def get_items():
    """Récupérer tous les items depuis l'API"""
    try:
        response = requests.get(f"{API_BASE_URL}/items")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Erreur lors de la récupération des items: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur de connexion à l'API: {str(e)}")
        return []

def get_items_cached():
    """Récupérer les items avec cache"""
    # Rafraîchir seulement si nécessaire
    if st.session_state.force_refresh:
        st.session_state.items_cache = get_items()
        st.session_state.last_update = datetime.now()
        st.session_state.force_refresh = False
    
    return st.session_state.items_cache

def create_item(name, description, price):
    """Créer un nouvel item"""
    try:
        data = {
            "name": name,
            "description": description,
            "price": price
        }
        response = requests.post(f"{API_BASE_URL}/items", json=data)
        if response.status_code == 200:
            # Forcer le refresh du cache au prochain appel
            st.session_state.force_refresh = True
            return True, response.json()
        else:
            return False, f"Erreur {response.status_code}: {response.text}"
    except requests.exceptions.RequestException as e:
        return False, f"Erreur de connexion: {str(e)}"

def delete_item(item_id):
    """Supprimer un item"""
    try:
        response = requests.delete(f"{API_BASE_URL}/items/{item_id}")
        if response.status_code == 200:
            # Forcer le refresh du cache au prochain appel
            st.session_state.force_refresh = True
            return True
        return False
    except requests.exceptions.RequestException:
        return False

# Interface principale
def main():
    st.title("🚀 Mon Application Streamlit + FastAPI")
    st.markdown("---")
    
    # Vérification de l'état de l'API (seulement au premier chargement)
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("Tableau de bord")
    
    with col2:
        # Cache le statut de l'API pour éviter les appels répétés
        if 'api_status' not in st.session_state:
            st.session_state.api_status = check_api_health()
        
        if st.session_state.api_status:
            st.success("🟢 API Connectée")
        else:
            st.error("🔴 API Déconnectée")
            st.warning(f"Vérifiez que l'API est accessible sur {API_BASE_URL}")
            if st.button("🔄 Tester la connexion"):
                st.session_state.api_status = check_api_health()
                st.rerun()
            return
    
    # Sidebar pour les actions
    with st.sidebar:
        st.header("Actions")
        
        # Formulaire pour ajouter un item
        with st.expander("➕ Ajouter un item", expanded=False):
            with st.form("add_item_form"):
                name = st.text_input("Nom du produit", placeholder="Ex: Smartphone")
                description = st.text_area("Description", placeholder="Description détaillée...")
                price = st.number_input("Prix (€)", min_value=0.01, step=0.01, format="%.2f")
                
                submit_button = st.form_submit_button("Créer l'item")
                
                if submit_button:
                    if name and price > 0:
                        success, result = create_item(name, description, price)
                        if success:
                            st.success("✅ Item créé avec succès!")
                            # Pas de st.rerun() - le cache sera rafraîchi automatiquement
                        else:
                            st.error(f"❌ Erreur: {result}")
                    else:
                        st.error("Veuillez remplir tous les champs obligatoires")
        
        # Bouton de rafraîchissement manuel
        if st.button("🔄 Rafraîchir les données", use_container_width=True):
            st.session_state.force_refresh = True
            st.session_state.api_status = check_api_health()
            st.rerun()
        
        # Afficher la dernière mise à jour
        st.caption(f"Dernière mise à jour: {st.session_state.last_update.strftime('%H:%M:%S')}")
    
    # Contenu principal - utiliser le cache
    items = get_items_cached()
    
    if items:
        st.subheader(f"📦 Liste des produits ({len(items)} items)")
        
        # Affichage en colonnes
        for idx, item in enumerate(items):
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
                
                with col1:
                    st.write(f"**{item['name']}**")
                    if item.get('description'):
                        st.caption(item['description'])
                
                with col2:
                    st.write(f"💰 **{item['price']:.2f} €**")
                
                with col3:
                    if 'created_at' in item:
                        created_date = datetime.fromisoformat(item['created_at'].replace('Z', '+00:00'))
                        st.caption(f"📅 {created_date.strftime('%d/%m/%Y')}")
                
                with col4:
                    if st.button("🗑️", key=f"delete_{item['id']}", help="Supprimer cet item"):
                        if delete_item(item['id']):
                            st.success("Item supprimé!")
                            st.rerun()  # Ici c'est OK car c'est une action ponctuelle
                        else:
                            st.error("Erreur lors de la suppression")
                
                st.divider()
        
        # Statistiques rapides
        st.subheader("📊 Statistiques")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Nombre total d'items", len(items))
        
        with col2:
            total_value = sum(item['price'] for item in items)
            st.metric("Valeur totale", f"{total_value:.2f} €")
        
        with col3:
            avg_price = total_value / len(items) if items else 0
            st.metric("Prix moyen", f"{avg_price:.2f} €")
        
        # Graphique simple
        if len(items) > 1:
            st.subheader("📈 Répartition des prix")
            chart_data = pd.DataFrame({
                'Produit': [item['name'] for item in items],
                'Prix': [item['price'] for item in items]
            })
            st.bar_chart(chart_data.set_index('Produit'))
    
    else:
        st.info("📝 Aucun item trouvé. Utilisez le panneau latéral pour ajouter des produits.")

if __name__ == "__main__":
    main()