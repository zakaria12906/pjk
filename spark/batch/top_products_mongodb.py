#!/usr/bin/env python3
"""
Analyse Batch Spark: Top 10 Produits + MongoDB
===============================================
"""

from pyspark.sql import SparkSession
from pymongo import MongoClient
from datetime import datetime
import re

# Configuration MongoDB
MONGO_URI = "mongodb://mongodb:27017"
MONGO_DB = "logs_analytics"
MONGO_COLLECTION = "top_products"

# Créer session Spark
spark = SparkSession.builder \
    .appName("Top Products Analysis - MongoDB") \
    .getOrCreate()

print("=" * 60)
print("✅ Spark Session créée avec succès")
print("=" * 60)

# Lire le fichier de logs depuis HDFS
try:
    logs_rdd = spark.sparkContext.textFile("hdfs://namenode:9000/logs/web_server.log")
    print(f"✅ Fichier chargé depuis HDFS")
    print(f"✅ Nombre de lignes: {logs_rdd.count()}")
except Exception as e:
    print(f"❌ Erreur lecture HDFS: {e}")
    spark.stop()
    exit(1)

# Fonction pour extraire l'ID du produit et sa catégorie
def extract_product_info(line):
    """Extraire l'ID du produit et sa catégorie"""
    # Pattern pour capturer: /products/CATEGORY/item?id=ID ou /products/item?id=ID
    match = re.search(r'/products/([^/?]+)(?:/([^?]+))?\?id=(\d+)', line)
    if match:
        if match.group(2):  # /products/category/item?id=X
            category = match.group(1)
            product_id = match.group(3)
        else:  # /products/item?id=X
            category = match.group(1).split('?')[0]
            product_id = match.group(2) if match.group(2) else match.group(3)
        
        # Nettoyer le category name
        if '?' in category:
            category = category.split('?')[0]
            
        return (product_id, category)
    return None

# Extraire les informations produits
product_info = logs_rdd.map(extract_product_info).filter(lambda x: x is not None)
print(f"✅ Nombre de requêtes produits: {product_info.count()}")

# Compter par ID de produit
from operator import add
product_counts = product_info.map(lambda x: (x, 1)) \
    .reduceByKey(add) \
    .sortBy(lambda x: x[1], ascending=False) \
    .take(10)

print("=" * 60)
print("🏆 TOP 10 PRODUITS:")
results = []
for i, ((product_id, category), count) in enumerate(product_counts, 1):
    print(f"{i}. Produit ID {product_id} ({category}): {count} requêtes")
    results.append({
        "rank": i,
        "product_id": product_id,
        "product_category": category,
        "request_count": count,
        "analysis_date": datetime.now().strftime("%Y-%m-%d"),
        "data_source": "hdfs:///logs/web_server.log"
    })
print("=" * 60)

# Sauvegarder dans MongoDB
try:
    print("\n📊 Sauvegarde dans MongoDB...")
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    collection = db[MONGO_COLLECTION]
    
    # Supprimer les anciennes données
    collection.delete_many({})
    print(f"✅ Collection {MONGO_COLLECTION} vidée")
    
    # Insérer les nouveaux résultats
    if results:
        collection.insert_many(results)
        print(f"✅ {len(results)} documents insérés dans MongoDB")
        print(f"   Base: {MONGO_DB}")
        print(f"   Collection: {MONGO_COLLECTION}")
    
    client.close()
    print("=" * 60)
    print("✅ Sauvegarde MongoDB réussie!")
    print("=" * 60)
    
except Exception as e:
    print(f"❌ Erreur MongoDB: {e}")

spark.stop()
print("\n✅ Analyse terminée avec succès!")
print("\nPour voir les résultats dans MongoDB:")
print("  docker exec -it mongodb mongosh")
print("  use logs_analytics")
print("  db.top_products.find().pretty()")
