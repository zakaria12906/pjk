#!/usr/bin/env python3
"""
Analyse Streaming Spark #2: Détection des Produits en Tendance
===============================================================

Objectif:
    Identifier en temps réel les produits populaires qui génèrent
    un volume anormal de consultations (> 20 vues par minute).

Méthode:
    1. Consommer les logs depuis Kafka en temps réel
    2. Parser et extraire les IDs de produits
    3. Fenêtrage temporel (1 minute)
    4. Compter les consultations par produit
    5. Détecter les produits "en tendance" (> 20 vues/minute)
    6. Calculer la vélocité (variation du nombre de vues)
    7. Sauvegarder les tendances dans MongoDB

Fenêtrage:
    - Window size: 1 minute (détection rapide)
    - Slide interval: 30 secondes (mise à jour fréquente)
    - Watermark: 20 secondes

Critères de tendance:
    - HOT: > 50 consultations/minute
    - TRENDING: > 20 consultations/minute
    - RISING: 10-20 consultations/minute avec croissance

Architecture:
    Kafka → Spark Structured Streaming → MongoDB
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    from_json, col, window, count, current_timestamp, 
    lit, when, regexp_extract, desc
)
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType
import re

# Configuration
KAFKA_BOOTSTRAP_SERVERS = "kafka:9093"
KAFKA_TOPIC = "web-logs"
MONGO_URI = "mongodb://mongodb:27017"
MONGO_DB = "logs_analytics"
MONGO_COLLECTION = "trending_products"

# Seuils de tendance
HOT_THRESHOLD = 50        # Produit très populaire
TRENDING_THRESHOLD = 20   # Produit en tendance
RISING_THRESHOLD = 10     # Produit en croissance

def create_spark_session():
    """Crée une session Spark Structured Streaming"""
    spark = SparkSession.builder \
        .appName("Real-Time Trending Products") \
        .config("spark.mongodb.output.uri", f"{MONGO_URI}/{MONGO_DB}.{MONGO_COLLECTION}") \
        .config("spark.streaming.stopGracefullyOnShutdown", "true") \
        .getOrCreate()
    
    return spark

def extract_product_info(url):
    """
    Extrait l'ID et la catégorie du produit depuis l'URL
    
    Exemples:
        /products/lipstick?id=105 → (105, "lipstick", "makeup")
        /products/skincare/cream?id=501 → (501, "cream", "skincare")
    """
    if not url or '?id=' not in url:
        return None, None, None
    
    # Extraire l'ID
    id_match = re.search(r'\?id=(\d+)', url)
    if not id_match:
        return None, None, None
    
    product_id = int(id_match.group(1))
    
    # Extraire la catégorie et le type de produit
    category = "other"
    product_type = "unknown"
    
    if '/products/skincare/' in url:
        category = "skincare"
        product_type = url.split('/products/skincare/')[1].split('?')[0]
    elif '/products/hair/' in url:
        category = "hair"
        product_type = url.split('/products/hair/')[1].split('?')[0]
    elif '/products/' in url:
        category = "makeup"
        product_type = url.split('/products/')[1].split('?')[0]
    
    return product_id, product_type, category

def setup_streaming_query(spark):
    """
    Configure la requête de streaming Spark
    
    Returns:
        DataFrame de streaming
    """
    print("\n" + "="*60)
    print("🚀 DÉMARRAGE DU STREAMING: PRODUITS EN TENDANCE")
    print("="*60)
    
    # Étape 1: Lire depuis Kafka
    print("\n📡 Connexion à Kafka...")
    print(f"   • Topic: {KAFKA_TOPIC}")
    print(f"   • Bootstrap servers: {KAFKA_BOOTSTRAP_SERVERS}")
    
    kafka_df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
        .option("subscribe", KAFKA_TOPIC) \
        .option("startingOffsets", "latest") \
        .load()
    
    # Étape 2: Convertir les valeurs Kafka en string
    logs_df = kafka_df.selectExpr("CAST(value AS STRING) as log_line", "timestamp")
    
    # Étape 3: Parser les logs pour extraire URL et code HTTP
    parsed_df = logs_df.select(
        regexp_extract(col("log_line"), r'^([\d\.]+)', 1).alias("ip"),
        col("timestamp").alias("event_time"),
        regexp_extract(col("log_line"), r'\"[A-Z]+\s+([^\s]+)\s+HTTP', 1).alias("url"),
        regexp_extract(col("log_line"), r'"\s+(\d{3})\s+', 1).cast("int").alias("http_code")
    ).filter(col("url").isNotNull())
    
    # Étape 4: Filtrer uniquement les URLs de produits (avec ?id=) et succès (200)
    product_df = parsed_df.filter(
        (col("url").contains("?id=")) & (col("http_code") == 200)
    )
    
    # Étape 5: Extraire l'ID et la catégorie du produit
    product_df = product_df.select(
        col("event_time"),
        col("ip"),
        col("url"),
        regexp_extract(col("url"), r'\?id=(\d+)', 1).cast("int").alias("product_id"),
        when(col("url").contains("/skincare/"), "skincare")
        .when(col("url").contains("/hair/"), "hair")
        .otherwise("makeup").alias("category"),
        regexp_extract(
            col("url"),
            r'/products/(?:skincare/|hair/)?([^?]+)',
            1
        ).alias("product_type")
    ).filter(col("product_id").isNotNull())
    
    # Étape 6: Configuration du fenêtrage
    print("\n⏱️  Configuration du fenêtrage temporel:")
    print("   • Taille de fenêtre: 1 minute")
    print("   • Intervalle de glissement: 30 secondes")
    print("   • Watermark: 20 secondes")
    
    # Ajouter watermark
    product_df = product_df.withWatermark("event_time", "20 seconds")
    
    # Étape 7: Agréger par fenêtre et produit
    windowed_products = product_df.groupBy(
        window(col("event_time"), "1 minute", "30 seconds"),
        col("product_id"),
        col("product_type"),
        col("category")
    ).agg(
        count("*").alias("views_count"),
        count(col("ip").distinct()).alias("unique_viewers")
    )
    
    # Étape 8: Classifier les tendances
    print("\n📈 Configuration des seuils de tendance:")
    print(f"   • HOT: > {HOT_THRESHOLD} vues/minute")
    print(f"   • TRENDING: > {TRENDING_THRESHOLD} vues/minute")
    print(f"   • RISING: {RISING_THRESHOLD}-{TRENDING_THRESHOLD} vues/minute")
    
    trending_df = windowed_products.withColumn(
        "trend_status",
        when(col("views_count") > HOT_THRESHOLD, "HOT")
        .when(col("views_count") > TRENDING_THRESHOLD, "TRENDING")
        .when(col("views_count") >= RISING_THRESHOLD, "RISING")
        .otherwise("NORMAL")
    )
    
    # Ajouter des badges et messages
    trending_df = trending_df.withColumn(
        "trend_badge",
        when(col("trend_status") == "HOT", "🔥")
        .when(col("trend_status") == "TRENDING", "📈")
        .when(col("trend_status") == "RISING", "⬆️")
        .otherwise("📊")
    )
    
    trending_df = trending_df.withColumn(
        "alert_message",
        when(col("trend_status") == "HOT",
             lit("🔥 PRODUIT TRÈS POPULAIRE! Vérifier le stock"))
        .when(col("trend_status") == "TRENDING",
             lit("📈 PRODUIT EN TENDANCE! Considérer une promotion"))
        .when(col("trend_status") == "RISING",
             lit("⬆️ PRODUIT EN CROISSANCE! Surveiller de près"))
        .otherwise(lit("📊 Activité normale"))
    )
    
    # Calculer le ratio de viewers uniques (engagement)
    trending_df = trending_df.withColumn(
        "engagement_rate",
        (col("unique_viewers") / col("views_count") * 100).cast("int")
    )
    
    # Ajouter timestamp de détection
    trending_df = trending_df.withColumn("detected_at", current_timestamp())
    
    # Filtrer pour ne garder que les produits intéressants (au moins RISING)
    trending_only = trending_df.filter(
        col("trend_status").isin(["HOT", "TRENDING", "RISING"])
    )
    
    # Sélectionner et ordonner les colonnes finales
    final_df = trending_only.select(
        col("window.start").alias("window_start"),
        col("window.end").alias("window_end"),
        col("product_id"),
        col("product_type"),
        col("category"),
        col("views_count"),
        col("unique_viewers"),
        col("engagement_rate"),
        col("trend_status"),
        col("trend_badge"),
        col("alert_message"),
        col("detected_at")
    )
    
    return final_df

def write_to_mongodb(df):
    """
    Configure l'écriture vers MongoDB
    
    Args:
        df: DataFrame à écrire
    
    Returns:
        StreamingQuery
    """
    print("\n💾 Configuration de l'écriture vers MongoDB...")
    
    query = df.writeStream \
        .outputMode("append") \
        .format("mongo") \
        .option("database", MONGO_DB) \
        .option("collection", MONGO_COLLECTION) \
        .option("checkpointLocation", "/tmp/spark-checkpoint-trending") \
        .start()
    
    return query

def write_to_console(df):
    """
    Configuration de l'affichage console (pour debugging)
    
    Args:
        df: DataFrame à afficher
    
    Returns:
        StreamingQuery
    """
    print("\n📺 Configuration de l'affichage console...")
    
    query = df.writeStream \
        .outputMode("append") \
        .format("console") \
        .option("truncate", "false") \
        .start()
    
    return query

def main():
    """Fonction principale"""
    # Créer la session Spark
    spark = create_spark_session()
    spark.sparkContext.setLogLevel("WARN")
    
    try:
        # Setup streaming
        trending_df = setup_streaming_query(spark)
        
        # Écriture simultanée vers MongoDB et console
        mongodb_query = write_to_mongodb(trending_df)
        console_query = write_to_console(trending_df)
        
        print("\n" + "="*60)
        print("✅ STREAMING DÉMARRÉ - DÉTECTION DES TENDANCES...")
        print("="*60)
        print("\n💡 Le système surveille maintenant les produits populaires")
        print("   Appuyez sur Ctrl+C pour arrêter\n")
        
        # Attendre la terminaison
        mongodb_query.awaitTermination()
        console_query.awaitTermination()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Arrêt demandé par l'utilisateur...")
        spark.streams.active[0].stop()
        print("✅ Streaming arrêté proprement\n")
    except Exception as e:
        print(f"\n❌ ERREUR: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        spark.stop()

if __name__ == "__main__":
    main()
