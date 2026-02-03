#!/usr/bin/env python3
"""Test simple Spark - Lecture logs HDFS"""

from pyspark.sql import SparkSession
import re

# Créer session Spark
spark = SparkSession.builder \
    .appName("Test Simple") \
    .getOrCreate()

print("=" * 50)
print("✅ Spark Session créée avec succès")
print("=" * 50)

# Lire le fichier de logs
try:
    logs_rdd = spark.sparkContext.textFile("hdfs://namenode:9000/logs/web_server.log")
    print(f"✅ Fichier chargé depuis HDFS")
    print(f"✅ Nombre de lignes: {logs_rdd.count()}")
    print("=" * 50)
    print("Premières lignes:")
    for line in logs_rdd.take(5):
        print(line)
    print("=" * 50)
except Exception as e:
    print(f"❌ Erreur: {e}")

# Analyser les produits
def extract_product_id(line):
    """Extraire l'ID du produit"""
    match = re.search(r'/products/[^?]+\?id=(\d+)', line)
    if match:
        return match.group(1)
    return None

# Extraire les IDs
product_ids = logs_rdd.map(extract_product_id).filter(lambda x: x is not None)
print(f"✅ Nombre de requêtes produits: {product_ids.count()}")

# Top 10 produits
from operator import add
top_products = product_ids.map(lambda x: (x, 1)) \
    .reduceByKey(add) \
    .sortBy(lambda x: x[1], ascending=False) \
    .take(10)

print("=" * 50)
print("🏆 TOP 10 PRODUITS:")
for i, (product_id, count) in enumerate(top_products, 1):
    print(f"{i}. Produit ID {product_id}: {count} requêtes")
print("=" * 50)

spark.stop()
print("✅ Test terminé avec succès!")
