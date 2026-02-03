#!/usr/bin/env python3
"""
Analyse Streaming Spark #1: Détection d'Erreurs en Temps Réel
==============================================================

Objectif:
    Surveiller les logs en temps réel pour détecter des pics d'erreurs
    (codes 404 ou 500) et générer des alertes.

Méthode:
    1. Consommer les logs depuis Kafka en temps réel
    2. Parser les lignes pour extraire IP, URL, et code HTTP
    3. Filtrer les erreurs (404, 500)
    4. Fenêtrage temporel (5 minutes)
    5. Compter les erreurs par type dans chaque fenêtre
    6. Générer des alertes si seuil dépassé (> 10 erreurs)
    7. Sauvegarder les alertes dans MongoDB

Fenêtrage:
    - Window size: 5 minutes
    - Slide interval: 1 minute
    - Watermark: 30 secondes (pour gérer les données en retard)

Alertes:
    - CRITIQUE: > 20 erreurs 500 en 5 minutes
    - HAUTE: > 10 erreurs 500 en 5 minutes
    - MOYENNE: > 30 erreurs 404 en 5 minutes

Architecture:
    Kafka → Spark Structured Streaming → MongoDB
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    from_json, col, window, count, current_timestamp, 
    lit, when, sum as spark_sum
)
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType
import re

# Configuration
KAFKA_BOOTSTRAP_SERVERS = "kafka:9093"
KAFKA_TOPIC = "web-logs"
MONGO_URI = "mongodb://mongodb:27017"
MONGO_DB = "logs_analytics"
MONGO_COLLECTION = "error_alerts"

# Seuils d'alerte
CRITICAL_500_THRESHOLD = 20  # Erreurs 500 critiques
HIGH_500_THRESHOLD = 10      # Erreurs 500 haute priorité
MEDIUM_404_THRESHOLD = 30    # Erreurs 404 moyenne priorité

def create_spark_session():
    """Crée une session Spark Structured Streaming"""
    spark = SparkSession.builder \
        .appName("Real-Time Error Detection") \
        .config("spark.mongodb.output.uri", f"{MONGO_URI}/{MONGO_DB}.{MONGO_COLLECTION}") \
        .config("spark.streaming.stopGracefullyOnShutdown", "true") \
        .getOrCreate()
    
    return spark

def parse_log_udf(log_line):
    """
    Parse une ligne de log et retourne un dictionnaire
    
    Format: IP - - [timestamp] "METHOD URL HTTP/1.1" CODE SIZE
    """
    try:
        # Extraire l'IP
        ip_pattern = r'^([\d\.]+)'
        ip_match = re.match(ip_pattern, log_line)
        
        # Extraire le timestamp
        timestamp_pattern = r'\[(.*?)\]'
        timestamp_match = re.search(timestamp_pattern, log_line)
        
        # Extraire l'URL
        url_pattern = r'\"[A-Z]+\s+([^\s]+)\s+HTTP'
        url_match = re.search(url_pattern, log_line)
        
        # Extraire le code HTTP
        code_pattern = r'"\s+(\d{3})\s+'
        code_match = re.search(code_pattern, log_line)
        
        if ip_match and timestamp_match and url_match and code_match:
            return {
                "ip": ip_match.group(1),
                "timestamp": timestamp_match.group(1),
                "url": url_match.group(1),
                "http_code": int(code_match.group(1))
            }
    except Exception as e:
        print(f"Erreur parsing: {e}")
    
    return None

def setup_streaming_query(spark):
    """
    Configure la requête de streaming Spark
    
    Returns:
        StreamingQuery object
    """
    print("\n" + "="*60)
    print("🚀 DÉMARRAGE DU STREAMING: DÉTECTION D'ERREURS")
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
    
    # Étape 3: Parser les logs avec regex
    from pyspark.sql.functions import regexp_extract
    
    parsed_df = logs_df.select(
        regexp_extract(col("log_line"), r'^([\d\.]+)', 1).alias("ip"),
        col("timestamp").alias("event_time"),
        regexp_extract(col("log_line"), r'\"[A-Z]+\s+([^\s]+)\s+HTTP', 1).alias("url"),
        regexp_extract(col("log_line"), r'"\s+(\d{3})\s+', 1).cast("int").alias("http_code")
    ).filter(col("http_code").isNotNull())
    
    # Étape 4: Filtrer uniquement les erreurs (4xx et 5xx)
    error_df = parsed_df.filter(
        (col("http_code") >= 400) & (col("http_code") < 600)
    )
    
    # Étape 5: Classifier les erreurs
    error_df = error_df.withColumn(
        "error_type",
        when(col("http_code") == 404, "NOT_FOUND")
        .when(col("http_code") == 500, "INTERNAL_ERROR")
        .when(col("http_code") == 503, "SERVICE_UNAVAILABLE")
        .when(col("http_code") == 403, "FORBIDDEN")
        .otherwise("OTHER_ERROR")
    )
    
    # Étape 6: Fenêtrage temporel (5 minutes, slide 1 minute)
    print("\n⏱️  Configuration du fenêtrage temporel:")
    print("   • Taille de fenêtre: 5 minutes")
    print("   • Intervalle de glissement: 1 minute")
    print("   • Watermark: 30 secondes")
    
    # Ajouter un watermark pour gérer les données en retard
    error_df = error_df.withWatermark("event_time", "30 seconds")
    
    # Agréger les erreurs par fenêtre et type
    windowed_errors = error_df.groupBy(
        window(col("event_time"), "5 minutes", "1 minute"),
        col("error_type"),
        col("http_code")
    ).agg(
        count("*").alias("error_count"),
        count(col("ip")).alias("unique_ips")
    )
    
    # Étape 7: Générer des alertes basées sur les seuils
    print("\n🚨 Configuration des seuils d'alerte:")
    print(f"   • CRITIQUE (500): > {CRITICAL_500_THRESHOLD} erreurs")
    print(f"   • HAUTE (500): > {HIGH_500_THRESHOLD} erreurs")
    print(f"   • MOYENNE (404): > {MEDIUM_404_THRESHOLD} erreurs")
    
    alerts_df = windowed_errors.withColumn(
        "alert_level",
        when(
            (col("http_code") == 500) & (col("error_count") > CRITICAL_500_THRESHOLD),
            "CRITICAL"
        )
        .when(
            (col("http_code") == 500) & (col("error_count") > HIGH_500_THRESHOLD),
            "HIGH"
        )
        .when(
            (col("http_code") == 404) & (col("error_count") > MEDIUM_404_THRESHOLD),
            "MEDIUM"
        )
        .otherwise("INFO")
    )
    
    alerts_df = alerts_df.withColumn(
        "alert_message",
        when(col("alert_level") == "CRITICAL",
             lit("🔴 ALERTE CRITIQUE: Pic d'erreurs 500 détecté!"))
        .when(col("alert_level") == "HIGH",
             lit("🟠 ALERTE HAUTE: Erreurs 500 anormales!"))
        .when(col("alert_level") == "MEDIUM",
             lit("🟡 ALERTE MOYENNE: Nombreuses erreurs 404!"))
        .otherwise(lit("ℹ️ INFO: Erreurs normales"))
    )
    
    # Ajouter timestamp de détection
    alerts_df = alerts_df.withColumn("detected_at", current_timestamp())
    
    # Sélectionner les colonnes finales
    final_df = alerts_df.select(
        col("window.start").alias("window_start"),
        col("window.end").alias("window_end"),
        col("error_type"),
        col("http_code"),
        col("error_count"),
        col("unique_ips"),
        col("alert_level"),
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
        .option("checkpointLocation", "/tmp/spark-checkpoint-errors") \
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
        alerts_df = setup_streaming_query(spark)
        
        # Écriture simultanée vers MongoDB et console
        mongodb_query = write_to_mongodb(alerts_df)
        console_query = write_to_console(alerts_df)
        
        print("\n" + "="*60)
        print("✅ STREAMING DÉMARRÉ - EN ATTENTE DE LOGS...")
        print("="*60)
        print("\n💡 Le système surveille maintenant les erreurs en temps réel")
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
