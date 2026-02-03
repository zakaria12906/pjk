#!/bin/bash
################################################################################
# Script de Préparation HDFS
# Crée les répertoires et charge les données dans HDFS
################################################################################

set -e

echo "=========================================="
echo "📦 PRÉPARATION DE HDFS"
echo "=========================================="
echo ""

# Attendre que HDFS soit prêt
echo "⏳ Attente du démarrage de HDFS..."
sleep 10

# Créer les répertoires dans HDFS
echo ""
echo "📁 Création des répertoires dans HDFS..."
docker exec namenode hdfs dfs -mkdir -p /logs
docker exec namenode hdfs dfs -mkdir -p /output
docker exec namenode hdfs dfs -chmod -R 777 /logs
docker exec namenode hdfs dfs -chmod -R 777 /output
echo "✅ Répertoires créés"

# Copier les logs dans HDFS
echo ""
echo "📤 Upload des logs dans HDFS..."
docker exec namenode hdfs dfs -put -f /data/web_server.log /logs/
echo "✅ Logs uploadés"

# Vérifier
echo ""
echo "🔍 Vérification..."
docker exec namenode hdfs dfs -ls /logs
echo ""
docker exec namenode hdfs dfs -du -h /logs
echo ""

echo "=========================================="
echo "✅ HDFS PRÊT"
echo "=========================================="
echo ""
echo "Vous pouvez maintenant:"
echo "  - Accéder à l'interface web: http://localhost:9870"
echo "  - Lancer les analyses batch: ./scripts/run_batch.sh"
echo ""
