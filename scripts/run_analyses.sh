#!/bin/bash
set -e

echo "=========================================="
echo "🚀 Démarrage des analyses automatiques"
echo "=========================================="

# Attendre que les services soient prêts
echo "⏳ Attente des services (60 secondes)..."
sleep 60

echo ""
echo "=========================================="
echo "📊 ÉTAPE 1/3 - Préparation HDFS"
echo "=========================================="

# Vérifier si le fichier existe déjà dans HDFS
if docker exec namenode hdfs dfs -test -e /logs/web_server.log 2>/dev/null; then
    echo "✅ Fichier déjà présent dans HDFS"
else
    echo "📂 Création des répertoires HDFS..."
    docker exec namenode hdfs dfs -mkdir -p /logs
    docker exec namenode hdfs dfs -chmod -R 777 /logs
    
    echo "📤 Upload du fichier de logs..."
    docker exec namenode hdfs dfs -put /data/web_server.log /logs/
    
    echo "✅ HDFS préparé"
fi

echo ""
echo "=========================================="
echo "📊 ÉTAPE 2/3 - Analyse BATCH (Top Produits)"
echo "=========================================="

docker exec spark-master /opt/spark/bin/spark-submit \
  --master spark://spark-master:7077 \
  /spark-apps/batch/top_products_mongodb.py

echo "✅ Analyse BATCH terminée"

echo ""
echo "=========================================="
echo "📊 ÉTAPE 3/3 - Analyse STREAMING (Détection Erreurs)"
echo "=========================================="

docker exec spark-master /opt/spark/bin/spark-submit \
  --master spark://spark-master:7077 \
  /spark-apps/streaming/error_detection_simple.py

echo "✅ Analyse STREAMING terminée"

echo ""
echo "=========================================="
echo "🎉 TOUTES LES ANALYSES SONT TERMINÉES !"
echo "=========================================="
echo ""
echo "📊 Résultats disponibles dans MongoDB:"
echo "   - Collection: logs_analytics.top_products"
echo "   - Collection: logs_analytics.error_alerts"
echo ""
echo "💡 Pour voir les résultats:"
echo "   docker exec -it mongodb mongosh"
echo "   use logs_analytics"
echo "   db.top_products.find().pretty()"
echo "   db.error_alerts.find().pretty()"
echo ""
