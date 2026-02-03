#!/usr/bin/env python3
"""
Analyse Batch Spark #1: Top 10 Produits les Plus Consultés
============================================================

Objectif:
    Identifier les produits (par leur ID) ayant reçu le plus de requêtes
    sur l'ensemble de la période couverte par les logs.

Méthode:
    1. Charger les logs depuis HDFS
    2. Parser les lignes pour extraire les URLs
    3. Filtrer uniquement les URLs de produits (contenant ?id=)
    4. Extraire les IDs de produits
    5. Compter les occurrences par ID
    6. Trier par ordre décroissant
    7. Sauvegarder les résultats dans MongoDB

Architecture:
    HDFS → Spark (RDD/DataFrame) → MongoDB
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, regexp_extract, count, desc
import re

# Configuration MongoDB
MONGO_URI = "mongodb://mongodb:27017"
MONGO_DB = "logs_analytics"
MONGO_COLLECTION = "top_products"

def create_spark_session():
    """Crée une session Spark avec configuration MongoDB"""
    spark = SparkSession.builder \
        .appName("Top Products Analysis") \
        .config("spark.mongodb.output.uri", f"{MONGO_URI}/{MONGO_DB}.{MONGO_COLLECTION}") \
        .getOrCreate()
    
    return spark

def parse_log_line(line):
    """
    Parse une ligne de log Apache et extrait les informations pertinentes
    
    Format: IP - - [timestamp] "METHOD URL HTTP/1.1" CODE SIZE
    Exemple: 192.168.1.100 - - [28/Jan/2025:15:40:02 +0000] "GET /products/lipstick?id=105 HTTP/1.1" 301 512
    """
    # Regex pour extraire l'URL
    pattern = r'\"[A-Z]+\s+([^\s]+)\s+HTTP'
    match = re.search(pattern, line)
    if match:
        return match.group(1)
    return None

def extract_product_id(url):
    """
    Extrait l'ID du produit depuis l'URL
    
    Exemple: /products/lipstick?id=105 → 105
    """
    if url and '?id=' in url:
        match = re.search(r'\?id=(\d+)', url)
        if match:
            return int(match.group(1))
    return None

def analyze_top_products(spark, input_path):
    """
    Analyse principale: identifie les produits les plus consultés
    
    Args:
        spark: Session Spark
        input_path: Chemin HDFS des logs
    
    Returns:
        DataFrame avec les top produits
    """
    print("\n" + "="*60)
    print("🚀 DÉMARRAGE DE L'ANALYSE: TOP 10 PRODUITS")
    print("="*60)
    
    # Étape 1: Charger les données depuis HDFS
    print("\n📂 Chargement des logs depuis HDFS...")
    logs_rdd = spark.sparkContext.textFile(input_path)
    total_lines = logs_rdd.count()
    print(f"   ✓ {total_lines} lignes chargées")
    
    # Étape 2: Parser les URLs
    print("\n🔍 Extraction des URLs...")
    urls_rdd = logs_rdd.map(parse_log_line).filter(lambda x: x is not None)
    print(f"   ✓ {urls_rdd.count()} URLs extraites")
    
    # Étape 3: Filtrer les URLs de produits et extraire les IDs
    print("\n🔢 Extraction des IDs de produits...")
    product_ids_rdd = urls_rdd.map(extract_product_id).filter(lambda x: x is not None)
    product_count = product_ids_rdd.count()
    print(f"   ✓ {product_count} consultations de produits détectées")
    
    # Étape 4: Compter les occurrences par ID
    print("\n📊 Comptage des consultations par produit...")
    product_counts = product_ids_rdd.map(lambda x: (x, 1)) \
                                    .reduceByKey(lambda a, b: a + b)
    
    # Étape 5: Convertir en DataFrame pour manipulation plus facile
    df = product_counts.toDF(["product_id", "views"])
    
    # Étape 6: Trier et prendre le top 10
    print("\n🏆 Identification du Top 10...")
    top_products_df = df.orderBy(desc("views")).limit(10)
    
    # Affichage des résultats
    print("\n" + "="*60)
    print("📈 RÉSULTATS: TOP 10 PRODUITS LES PLUS CONSULTÉS")
    print("="*60)
    top_products_df.show(truncate=False)
    
    # Statistiques supplémentaires
    total_views = df.agg({"views": "sum"}).collect()[0][0]
    unique_products = df.count()
    top_10_views = top_products_df.agg({"views": "sum"}).collect()[0][0]
    
    print(f"\n📊 Statistiques globales:")
    print(f"   • Produits uniques: {unique_products}")
    print(f"   • Consultations totales: {total_views}")
    print(f"   • Top 10 représente: {(top_10_views/total_views)*100:.1f}% des vues")
    
    return top_products_df

def save_to_mongodb(df, collection_name):
    """
    Sauvegarde les résultats dans MongoDB
    
    Args:
        df: DataFrame Spark à sauvegarder
        collection_name: Nom de la collection MongoDB
    """
    print(f"\n💾 Sauvegarde des résultats dans MongoDB ({collection_name})...")
    
    # Ajouter un timestamp
    from pyspark.sql.functions import current_timestamp
    df_with_timestamp = df.withColumn("analyzed_at", current_timestamp())
    
    # Écriture dans MongoDB
    df_with_timestamp.write \
        .format("mongo") \
        .mode("overwrite") \
        .option("database", MONGO_DB) \
        .option("collection", collection_name) \
        .save()
    
    print("   ✓ Résultats sauvegardés avec succès!")
    print(f"   ℹ️  Requête MongoDB: db.{collection_name}.find().pretty()")

def main():
    """Fonction principale"""
    # Chemins
    INPUT_PATH = "hdfs://namenode:9000/logs/web_server.log"
    
    # Créer la session Spark
    spark = create_spark_session()
    spark.sparkContext.setLogLevel("WARN")  # Réduire les logs verbeux
    
    try:
        # Exécuter l'analyse
        top_products_df = analyze_top_products(spark, INPUT_PATH)
        
        # Sauvegarder dans MongoDB
        save_to_mongodb(top_products_df, MONGO_COLLECTION)
        
        print("\n" + "="*60)
        print("✅ ANALYSE TERMINÉE AVEC SUCCÈS!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ ERREUR: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        spark.stop()

if __name__ == "__main__":
    main()
