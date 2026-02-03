#!/bin/bash
################################################################################
# Script d'Exécution des Analyses Batch
# Lance les 3 analyses Spark Batch séquentiellement
################################################################################

set -e

echo "=========================================="
echo "🚀 LANCEMENT DES ANALYSES BATCH"
echo "=========================================="
echo ""

# Analyse 1: Top Produits
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Analyse #1: Top 10 Produits"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

docker exec spark-master spark-submit \
  --master spark://spark-master:7077 \
  --packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 \
  /spark-apps/batch/top_products.py

echo ""
echo "✅ Analyse #1 terminée"
echo ""
sleep 3

# Analyse 2: Codes HTTP
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Analyse #2: Répartition des Codes HTTP"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

docker exec spark-master spark-submit \
  --master spark://spark-master:7077 \
  --packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 \
  /spark-apps/batch/http_codes.py

echo ""
echo "✅ Analyse #2 terminée"
echo ""
sleep 3

# Analyse 3: Top IPs
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Analyse #3: Top 10 IPs Actives"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

docker exec spark-master spark-submit \
  --master spark://spark-master:7077 \
  --packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 \
  /spark-apps/batch/top_ips.py

echo ""
echo "✅ Analyse #3 terminée"
echo ""

# Afficher les résultats dans MongoDB
echo "=========================================="
echo "✅ TOUTES LES ANALYSES TERMINÉES"
echo "=========================================="
echo ""
echo "📊 Consulter les résultats dans MongoDB:"
echo ""
echo "  docker exec -it mongodb mongo"
echo "  > use logs_analytics"
echo "  > show collections"
echo "  > db.top_products.find().pretty()"
echo "  > db.http_codes_detailed.find().pretty()"
echo "  > db.top_ips.find().pretty()"
echo ""
