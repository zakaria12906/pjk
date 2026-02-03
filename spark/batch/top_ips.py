#!/usr/bin/env python3
"""
Analyse Batch Spark #3: Top 10 Adresses IP les Plus Actives
============================================================

Objectif:
    Identifier les adresses IP générant le plus de requêtes pour:
    - Détecter les utilisateurs les plus actifs
    - Identifier les potentiels bots ou attaques DDoS
    - Analyser les patterns d'utilisation

Méthode:
    1. Charger les logs depuis HDFS
    2. Parser les lignes pour extraire les IPs
    3. Compter les requêtes par IP
    4. Identifier le Top 10
    5. Calculer des statistiques (requêtes/heure, pattern d'activité)
    6. Détecter les comportements suspects
    7. Sauvegarder les résultats dans MongoDB

Critères de suspicion:
    - > 1000 requêtes par IP (possible bot)
    - Ratio d'erreurs élevé (> 30%)
    - Activité concentrée sur peu de ressources

Architecture:
    HDFS → Spark (RDD/DataFrame) → MongoDB
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, desc, sum as spark_sum, round as spark_round, avg
import re
from datetime import datetime

# Configuration MongoDB
MONGO_URI = "mongodb://mongodb:27017"
MONGO_DB = "logs_analytics"
MONGO_COLLECTION = "top_ips"

# Seuils de détection
SUSPICIOUS_THRESHOLD = 1000  # Nombre de requêtes considéré comme suspect
ERROR_RATE_THRESHOLD = 30    # Pourcentage d'erreurs suspect

def create_spark_session():
    """Crée une session Spark avec configuration MongoDB"""
    spark = SparkSession.builder \
        .appName("Top IPs Analysis") \
        .config("spark.mongodb.output.uri", f"{MONGO_URI}/{MONGO_DB}.{MONGO_COLLECTION}") \
        .getOrCreate()
    
    return spark

def parse_log_line_full(line):
    """
    Parse complète une ligne de log pour extraire IP, URL, et code HTTP
    
    Format: IP - - [timestamp] "METHOD URL HTTP/1.1" CODE SIZE
    Retourne: (ip, url, http_code)
    """
    try:
        # Extraire l'IP (au début de la ligne)
        ip_pattern = r'^([\d\.]+)'
        ip_match = re.match(ip_pattern, line)
        
        # Extraire l'URL
        url_pattern = r'\"[A-Z]+\s+([^\s]+)\s+HTTP'
        url_match = re.search(url_pattern, line)
        
        # Extraire le code HTTP
        code_pattern = r'"\s+(\d{3})\s+'
        code_match = re.search(code_pattern, line)
        
        if ip_match and url_match and code_match:
            ip = ip_match.group(1)
            url = url_match.group(1)
            code = int(code_match.group(1))
            return (ip, url, code)
    except:
        pass
    
    return None

def analyze_top_ips(spark, input_path):
    """
    Analyse principale: identifie les IPs les plus actives
    
    Args:
        spark: Session Spark
        input_path: Chemin HDFS des logs
    
    Returns:
        DataFrame avec les top IPs et leurs statistiques
    """
    print("\n" + "="*60)
    print("🚀 DÉMARRAGE DE L'ANALYSE: TOP 10 IPS ACTIVES")
    print("="*60)
    
    # Étape 1: Charger les données depuis HDFS
    print("\n📂 Chargement des logs depuis HDFS...")
    logs_rdd = spark.sparkContext.textFile(input_path)
    total_lines = logs_rdd.count()
    print(f"   ✓ {total_lines} lignes chargées")
    
    # Étape 2: Parser les logs complets
    print("\n🔍 Extraction des informations (IP, URL, Code)...")
    parsed_rdd = logs_rdd.map(parse_log_line_full).filter(lambda x: x is not None)
    parsed_count = parsed_rdd.count()
    print(f"   ✓ {parsed_count} lignes parsées avec succès")
    
    # Convertir en DataFrame pour analyses complexes
    df = parsed_rdd.toDF(["ip", "url", "http_code"])
    
    # Étape 3: Statistiques par IP
    print("\n📊 Calcul des statistiques par IP...")
    
    # Compter le total de requêtes par IP
    ip_stats = df.groupBy("ip").agg(
        count("*").alias("total_requests"),
        spark_sum((col("http_code") >= 400).cast("int")).alias("error_requests"),
        count(col("url").contains("/products/").cast("int")).alias("product_requests")
    )
    
    # Calculer le taux d'erreur
    ip_stats = ip_stats.withColumn(
        "error_rate",
        spark_round((col("error_requests") / col("total_requests")) * 100, 2)
    )
    
    # Calculer le ratio de requêtes produits
    ip_stats = ip_stats.withColumn(
        "product_ratio",
        spark_round((col("product_requests") / col("total_requests")) * 100, 2)
    )
    
    # Étape 4: Détection de comportements suspects
    print("\n🔍 Détection de comportements suspects...")
    
    from pyspark.sql.functions import when, lit
    
    ip_stats = ip_stats.withColumn(
        "is_suspicious",
        when(col("total_requests") > SUSPICIOUS_THRESHOLD, lit(True))
        .when(col("error_rate") > ERROR_RATE_THRESHOLD, lit(True))
        .otherwise(lit(False))
    )
    
    ip_stats = ip_stats.withColumn(
        "suspicion_reason",
        when(col("total_requests") > SUSPICIOUS_THRESHOLD, lit("High request volume (possible bot)"))
        .when(col("error_rate") > ERROR_RATE_THRESHOLD, lit("High error rate (possible attack)"))
        .otherwise(lit("Normal"))
    )
    
    # Étape 5: Top 10 IPs les plus actives
    print("\n🏆 Identification du Top 10...")
    top_ips_df = ip_stats.orderBy(desc("total_requests")).limit(10)
    
    # Affichage des résultats
    print("\n" + "="*60)
    print("📈 RÉSULTATS: TOP 10 ADRESSES IP LES PLUS ACTIVES")
    print("="*60)
    top_ips_df.show(truncate=False)
    
    # Statistiques globales
    total_ips = ip_stats.count()
    total_requests = ip_stats.agg(spark_sum("total_requests")).collect()[0][0]
    suspicious_ips = ip_stats.filter(col("is_suspicious") == True).count()
    top_10_requests = top_ips_df.agg(spark_sum("total_requests")).collect()[0][0]
    
    print(f"\n📊 Statistiques globales:")
    print(f"   • IPs uniques: {total_ips}")
    print(f"   • Requêtes totales: {total_requests}")
    print(f"   • IPs suspectes: {suspicious_ips} ({(suspicious_ips/total_ips)*100:.1f}%)")
    print(f"   • Top 10 représente: {(top_10_requests/total_requests)*100:.1f}% du trafic")
    
    # Analyse des IPs suspectes dans le Top 10
    suspicious_in_top = top_ips_df.filter(col("is_suspicious") == True).count()
    if suspicious_in_top > 0:
        print(f"\n⚠️  ALERTE: {suspicious_in_top} IP(s) suspecte(s) dans le Top 10!")
        print("\n🔍 Détails des IPs suspectes:")
        top_ips_df.filter(col("is_suspicious") == True).select(
            "ip", "total_requests", "error_rate", "suspicion_reason"
        ).show(truncate=False)
        
        print("\n💡 Recommandations:")
        print("   1. Vérifier les logs détaillés de ces IPs")
        print("   2. Considérer une limitation de débit (rate limiting)")
        print("   3. Mettre en place un CAPTCHA si nécessaire")
        print("   4. Analyser les patterns temporels d'activité")
    else:
        print("\n✅ Aucun comportement suspect détecté dans le Top 10")
    
    # Analyse de répartition du trafic
    print("\n" + "="*60)
    print("📊 ANALYSE DE LA RÉPARTITION DU TRAFIC")
    print("="*60)
    
    # Calculer la médiane et moyenne de requêtes par IP
    median_requests = ip_stats.approxQuantile("total_requests", [0.5], 0.01)[0]
    avg_requests = ip_stats.agg(avg("total_requests")).collect()[0][0]
    
    print(f"   • Moyenne de requêtes par IP: {avg_requests:.1f}")
    print(f"   • Médiane de requêtes par IP: {median_requests}")
    
    # Distribution par quartiles
    quartiles = ip_stats.approxQuantile("total_requests", [0.25, 0.5, 0.75], 0.01)
    print(f"\n   Distribution des requêtes:")
    print(f"   • Q1 (25%): {quartiles[0]} requêtes")
    print(f"   • Q2 (50%): {quartiles[1]} requêtes")
    print(f"   • Q3 (75%): {quartiles[2]} requêtes")
    
    return top_ips_df

def save_to_mongodb(df, collection_name):
    """
    Sauvegarde les résultats dans MongoDB
    
    Args:
        df: DataFrame Spark à sauvegarder
        collection_name: Nom de la collection MongoDB
    """
    print(f"\n💾 Sauvegarde des résultats dans MongoDB ({collection_name})...")
    
    from pyspark.sql.functions import current_timestamp
    
    # Ajouter un timestamp
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
    spark.sparkContext.setLogLevel("WARN")
    
    try:
        # Exécuter l'analyse
        top_ips_df = analyze_top_ips(spark, INPUT_PATH)
        
        # Sauvegarder dans MongoDB
        save_to_mongodb(top_ips_df, MONGO_COLLECTION)
        
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
