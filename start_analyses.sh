#!/bin/bash
set -e

echo "=========================================="
echo "🚀 PROJET BIG DATA - Analyses Automatiques"
echo "=========================================="
echo ""

# Vérifier que Docker tourne
if ! docker ps > /dev/null 2>&1; then
    echo "❌ Docker n'est pas démarré !"
    echo "   Lancez Docker Desktop d'abord"
    exit 1
fi

# Démarrer les services
echo "📦 Démarrage des services Docker..."
docker-compose up -d

echo "⏳ Attente que tous les services soient prêts (90 secondes)..."
sleep 90

echo ""
echo "=========================================="
echo "📊 ÉTAPE 1/3 - Préparation HDFS"
echo "=========================================="

# Vérifier si le fichier existe déjà dans HDFS
if docker exec namenode hdfs dfs -test -e /logs/web_server.log 2>/dev/null; then
    echo "✅ Fichier déjà présent dans HDFS"
else
    echo "📂 Création des répertoires HDFS..."
    docker exec namenode hdfs dfs -mkdir -p /logs 2>/dev/null || true
    docker exec namenode hdfs dfs -chmod -R 777 /logs 2>/dev/null || true
    
    echo "📤 Upload du fichier de logs dans HDFS..."
    docker exec namenode hdfs dfs -put /data/web_server.log /logs/ 2>/dev/null || echo "Fichier déjà présent"
    
    echo "✅ HDFS préparé"
fi

echo ""
echo "=========================================="
echo "📊 ÉTAPE 2/3 - Analyse BATCH (Top 10 Produits)"
echo "=========================================="

docker exec spark-master /opt/spark/bin/spark-submit \
  --master spark://spark-master:7077 \
  /spark-apps/batch/top_products_mongodb.py

echo ""
echo "✅ Analyse BATCH terminée"

echo ""
echo "=========================================="
echo "📊 ÉTAPE 3/3 - Analyse STREAMING (Détection Erreurs)"
echo "=========================================="

docker exec spark-master /opt/spark/bin/spark-submit \
  --master spark://spark-master:7077 \
  /spark-apps/streaming/error_detection_simple.py

echo ""
echo "✅ Analyse STREAMING terminée"

echo ""
echo "=========================================="
echo "🎉 TOUTES LES ANALYSES SONT TERMINÉES !"
echo "=========================================="
echo ""
echo "📊 Résultats disponibles dans MongoDB:"
echo ""
echo "   1️⃣  Top 10 Produits:"
echo "       docker exec -it mongodb mongosh"
echo "       use logs_analytics"
echo "       db.top_products.find().pretty()"
echo ""
echo "   2️⃣  Alertes d'erreurs:"
echo "       docker exec -it mongodb mongosh"
echo "       use logs_analytics"
echo "       db.error_alerts.find().pretty()"
echo ""
echo "📊 Interfaces Web:"
echo "   - HDFS:        http://localhost:9870"
echo "   - Spark:       http://localhost:8080"
echo ""
echo "🛑 Pour arrêter:"
echo "   docker-compose down"
echo ""
