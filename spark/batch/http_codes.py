#!/usr/bin/env python3
"""
Analyse Batch Spark #2: Répartition des Codes HTTP
===================================================

Objectif:
    Analyser la fréquence des codes HTTP (200, 404, 500, etc.) pour
    évaluer les performances et la santé du serveur web.

Méthode:
    1. Charger les logs depuis HDFS
    2. Parser les lignes pour extraire les codes HTTP
    3. Compter les occurrences de chaque code
    4. Calculer les pourcentages
    5. Classifier les codes par catégorie (succès, erreur, redirection)
    6. Sauvegarder les résultats dans MongoDB

KPIs générés:
    - Taux de succès (2xx)
    - Taux d'erreur client (4xx)
    - Taux d'erreur serveur (5xx)
    - Taux de redirection (3xx)

Architecture:
    HDFS → Spark (RDD/DataFrame) → MongoDB
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, desc, sum as spark_sum, round as spark_round
import re

# Configuration MongoDB
MONGO_URI = "mongodb://mongodb:27017"
MONGO_DB = "logs_analytics"
MONGO_COLLECTION = "http_codes"

# Classification des codes HTTP
CODE_CATEGORIES = {
    "2xx - Succès": [200, 201, 202, 204],
    "3xx - Redirection": [301, 302, 303, 304, 307, 308],
    "4xx - Erreur Client": [400, 401, 403, 404, 405, 408, 429],
    "5xx - Erreur Serveur": [500, 502, 503, 504]
}

def create_spark_session():
    """Crée une session Spark avec configuration MongoDB"""
    spark = SparkSession.builder \
        .appName("HTTP Codes Analysis") \
        .config("spark.mongodb.output.uri", f"{MONGO_URI}/{MONGO_DB}.{MONGO_COLLECTION}") \
        .getOrCreate()
    
    return spark

def parse_http_code(line):
    """
    Parse une ligne de log et extrait le code HTTP
    
    Format: IP - - [timestamp] "METHOD URL HTTP/1.1" CODE SIZE
    Exemple: 192.168.1.100 - - [28/Jan/2025:15:40:02 +0000] "GET /products/lipstick?id=105 HTTP/1.1" 301 512
    """
    # Regex pour extraire le code HTTP (après le dernier guillemet)
    pattern = r'"\s+(\d{3})\s+'
    match = re.search(pattern, line)
    if match:
        return int(match.group(1))
    return None

def categorize_code(code):
    """
    Catégorise un code HTTP selon sa classe
    
    Args:
        code: Code HTTP (int)
    
    Returns:
        Catégorie du code (str)
    """
    for category, codes in CODE_CATEGORIES.items():
        if code in codes:
            return category
    return "Autre"

def analyze_http_codes(spark, input_path):
    """
    Analyse principale: répartition des codes HTTP
    
    Args:
        spark: Session Spark
        input_path: Chemin HDFS des logs
    
    Returns:
        Tuple (codes_df, categories_df) avec les DataFrames de résultats
    """
    print("\n" + "="*60)
    print("🚀 DÉMARRAGE DE L'ANALYSE: CODES HTTP")
    print("="*60)
    
    # Étape 1: Charger les données depuis HDFS
    print("\n📂 Chargement des logs depuis HDFS...")
    logs_rdd = spark.sparkContext.textFile(input_path)
    total_lines = logs_rdd.count()
    print(f"   ✓ {total_lines} lignes chargées")
    
    # Étape 2: Parser les codes HTTP
    print("\n🔍 Extraction des codes HTTP...")
    http_codes_rdd = logs_rdd.map(parse_http_code).filter(lambda x: x is not None)
    valid_codes = http_codes_rdd.count()
    print(f"   ✓ {valid_codes} codes HTTP extraits")
    
    # Étape 3: Compter les occurrences par code
    print("\n📊 Comptage des occurrences par code...")
    code_counts = http_codes_rdd.map(lambda x: (x, 1)) \
                                 .reduceByKey(lambda a, b: a + b)
    
    # Convertir en DataFrame
    codes_df = code_counts.toDF(["http_code", "count"])
    
    # Calculer les pourcentages
    total_requests = codes_df.agg(spark_sum("count")).collect()[0][0]
    codes_df = codes_df.withColumn("percentage", 
                                   spark_round((col("count") / total_requests) * 100, 2))
    
    # Trier par nombre de requêtes
    codes_df = codes_df.orderBy(desc("count"))
    
    # Affichage des résultats détaillés
    print("\n" + "="*60)
    print("📈 RÉSULTATS: RÉPARTITION DES CODES HTTP")
    print("="*60)
    codes_df.show(truncate=False)
    
    # Étape 4: Analyse par catégorie
    print("\n📊 Analyse par catégorie...")
    
    # Ajouter la catégorie à chaque code
    from pyspark.sql.functions import udf
    from pyspark.sql.types import StringType
    
    categorize_udf = udf(categorize_code, StringType())
    codes_with_category = codes_df.withColumn("category", categorize_udf(col("http_code")))
    
    # Agréger par catégorie
    categories_df = codes_with_category.groupBy("category") \
                                       .agg(spark_sum("count").alias("count"),
                                            spark_sum("percentage").alias("percentage"))
    
    categories_df = categories_df.orderBy(desc("count"))
    
    print("\n" + "="*60)
    print("📊 RÉPARTITION PAR CATÉGORIE")
    print("="*60)
    categories_df.show(truncate=False)
    
    # Étape 5: KPIs de santé du serveur
    print("\n" + "="*60)
    print("🏥 INDICATEURS DE SANTÉ DU SERVEUR (KPIs)")
    print("="*60)
    
    categories_list = categories_df.collect()
    kpis = {}
    
    for row in categories_list:
        category = row["category"]
        percentage = row["percentage"]
        
        if "Succès" in category:
            kpis["success_rate"] = percentage
            print(f"   ✅ Taux de succès (2xx): {percentage:.2f}%")
        elif "Redirection" in category:
            kpis["redirect_rate"] = percentage
            print(f"   🔄 Taux de redirection (3xx): {percentage:.2f}%")
        elif "Erreur Client" in category:
            kpis["client_error_rate"] = percentage
            print(f"   ⚠️  Taux d'erreur client (4xx): {percentage:.2f}%")
        elif "Erreur Serveur" in category:
            kpis["server_error_rate"] = percentage
            print(f"   ❌ Taux d'erreur serveur (5xx): {percentage:.2f}%")
    
    # Évaluation de la santé
    print("\n💡 Évaluation:")
    success_rate = kpis.get("success_rate", 0)
    server_error_rate = kpis.get("server_error_rate", 0)
    
    if success_rate >= 95 and server_error_rate < 1:
        print("   🟢 Serveur en EXCELLENTE santé")
    elif success_rate >= 85 and server_error_rate < 3:
        print("   🟡 Serveur en BONNE santé")
    elif success_rate >= 70:
        print("   🟠 Serveur en santé MOYENNE - Attention requise")
    else:
        print("   🔴 Serveur en MAUVAISE santé - Action immédiate requise!")
    
    # Ajouter les KPIs au DataFrame des catégories
    from pyspark.sql.functions import lit, current_timestamp
    categories_df = categories_df.withColumn("analyzed_at", current_timestamp())
    
    return codes_df, categories_df, kpis

def save_to_mongodb(codes_df, categories_df, kpis):
    """
    Sauvegarde les résultats dans MongoDB
    
    Args:
        codes_df: DataFrame avec les codes détaillés
        categories_df: DataFrame avec les catégories
        kpis: Dictionnaire des KPIs
    """
    print(f"\n💾 Sauvegarde des résultats dans MongoDB...")
    
    from pyspark.sql.functions import current_timestamp
    
    # Sauvegarder les codes détaillés
    codes_df_timestamped = codes_df.withColumn("analyzed_at", current_timestamp())
    codes_df_timestamped.write \
        .format("mongo") \
        .mode("overwrite") \
        .option("database", MONGO_DB) \
        .option("collection", "http_codes_detailed") \
        .save()
    print("   ✓ Codes détaillés sauvegardés")
    
    # Sauvegarder les catégories
    categories_df.write \
        .format("mongo") \
        .mode("overwrite") \
        .option("database", MONGO_DB) \
        .option("collection", "http_codes_categories") \
        .save()
    print("   ✓ Catégories sauvegardées")
    
    # Sauvegarder les KPIs dans une collection séparée
    from datetime import datetime
    kpis_data = [{
        "analyzed_at": datetime.now(),
        "success_rate": kpis.get("success_rate", 0),
        "redirect_rate": kpis.get("redirect_rate", 0),
        "client_error_rate": kpis.get("client_error_rate", 0),
        "server_error_rate": kpis.get("server_error_rate", 0)
    }]
    
    spark = SparkSession.getActiveSession()
    kpis_df = spark.createDataFrame(kpis_data)
    kpis_df.write \
        .format("mongo") \
        .mode("overwrite") \
        .option("database", MONGO_DB) \
        .option("collection", "server_health_kpis") \
        .save()
    print("   ✓ KPIs de santé sauvegardés")
    
    print(f"\n   ℹ️  Requêtes MongoDB:")
    print(f"      db.http_codes_detailed.find().pretty()")
    print(f"      db.http_codes_categories.find().pretty()")
    print(f"      db.server_health_kpis.find().pretty()")

def main():
    """Fonction principale"""
    # Chemins
    INPUT_PATH = "hdfs://namenode:9000/logs/web_server.log"
    
    # Créer la session Spark
    spark = create_spark_session()
    spark.sparkContext.setLogLevel("WARN")
    
    try:
        # Exécuter l'analyse
        codes_df, categories_df, kpis = analyze_http_codes(spark, INPUT_PATH)
        
        # Sauvegarder dans MongoDB
        save_to_mongodb(codes_df, categories_df, kpis)
        
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
