#!/bin/bash
################################################################################
# Script de Configuration Initiale
# Prépare l'environnement pour le projet Big Data
################################################################################

set -e  # Arrêter en cas d'erreur

echo "=========================================="
echo "🚀 CONFIGURATION INITIALE DU PROJET"
echo "=========================================="
echo ""

# Vérifier Docker
echo "📦 Vérification de Docker..."
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé. Veuillez l'installer: https://docs.docker.com/get-docker/"
    exit 1
fi
echo "✅ Docker détecté: $(docker --version)"

# Vérifier Docker Compose
echo ""
echo "📦 Vérification de Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose n'est pas installé. Veuillez l'installer: https://docs.docker.com/compose/install/"
    exit 1
fi
echo "✅ Docker Compose détecté: $(docker-compose --version)"

# Créer les répertoires nécessaires
echo ""
echo "📁 Création des répertoires..."
mkdir -p data
mkdir -p spark/batch
mkdir -p spark/streaming
mkdir -p kafka
mkdir -p config
mkdir -p hdfs/namenode
mkdir -p hdfs/datanode
echo "✅ Répertoires créés"

# Rendre les scripts exécutables
echo ""
echo "🔧 Configuration des permissions..."
chmod +x data/generate_logs.py
chmod +x spark/batch/*.py
chmod +x spark/streaming/*.py
chmod +x kafka/log_producer.py
chmod +x scripts/*.sh
echo "✅ Permissions configurées"

# Vérifier Python
echo ""
echo "🐍 Vérification de Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé"
    exit 1
fi
echo "✅ Python détecté: $(python3 --version)"

# Générer les données de logs
echo ""
echo "📊 Génération des logs d'exemple..."
cd data
python3 generate_logs.py
cd ..
echo "✅ Logs générés"

# Afficher les informations
echo ""
echo "=========================================="
echo "✅ CONFIGURATION TERMINÉE"
echo "=========================================="
echo ""
echo "Prochaines étapes:"
echo "  1. Démarrer les services: docker-compose up -d"
echo "  2. Préparer HDFS: ./scripts/prepare_hdfs.sh"
echo "  3. Lancer les analyses batch: ./scripts/run_batch.sh"
echo "  4. Lancer le streaming: ./scripts/run_streaming.sh"
echo ""
echo "Pour plus d'informations, voir README.md"
echo ""
