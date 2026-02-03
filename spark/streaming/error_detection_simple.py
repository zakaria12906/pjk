#!/usr/bin/env python3
"""
Analyse Streaming Simplifiée: Détection d'Erreurs en Temps Réel
================================================================
Simule le streaming en lisant des logs par batch et détectant les erreurs
"""

from pyspark.sql import SparkSession
from pymongo import MongoClient
from datetime import datetime
import time
import re

# Configuration
MONGO_URI = "mongodb://mongodb:27017"
MONGO_DB = "logs_analytics"
MONGO_COLLECTION = "error_alerts"
ERROR_500_THRESHOLD = 10
ERROR_404_THRESHOLD = 30

print("=" * 70)
print("🚀 STREAMING - Détection d'Erreurs en Temps Réel")
print("=" * 70)

# Créer session Spark
spark = SparkSession.builder \
    .appName("Error Detection - Streaming Simulation") \
    .getOrCreate()

print("✅ Spark Session créée")

# Connexion MongoDB
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]
collection.delete_many({})  # Vider la collection
print(f"✅ Collection {MONGO_COLLECTION} vidée")

print("\n" + "=" * 70)
print("📊 Simulation du streaming (lecture progressive des logs)")
print("   Fenêtre: 5 minutes | Détection: codes 404 et 500")
print("=" * 70 + "\n")

# Fonction pour extraire le code HTTP
def extract_http_code(line):
    """Extraire le code HTTP d'une ligne de log"""
    match = re.search(r'HTTP/1\.1"\s+(\d{3})', line)
    if match:
        return int(match.group(1))
    return None

# Lire les logs depuis HDFS
logs_rdd = spark.sparkContext.textFile("hdfs://namenode:9000/logs/web_server.log")
all_logs = logs_rdd.collect()

print(f"📂 {len(all_logs)} lignes de logs chargées depuis HDFS\n")

# Simuler le streaming par batch
batch_size = 10  # Traiter 10 logs à la fois
num_batches = (len(all_logs) + batch_size - 1) // batch_size

for batch_num in range(num_batches):
    start_idx = batch_num * batch_size
    end_idx = min((batch_num + 1) * batch_size, len(all_logs))
    batch_logs = all_logs[start_idx:end_idx]
    
    print(f"⏳ Batch {batch_num + 1}/{num_batches} - Traitement de {len(batch_logs)} logs...")
    
    # Compter les erreurs dans ce batch
    error_counts = {}
    for log in batch_logs:
        code = extract_http_code(log)
        if code in [404, 500]:
            error_counts[code] = error_counts.get(code, 0) + 1
    
    # Afficher les statistiques
    if error_counts:
        print(f"   📊 Erreurs détectées:")
        for code, count in sorted(error_counts.items()):
            print(f"      - Code {code}: {count} erreur(s)")
        
        # Générer des alertes si seuils dépassés
        window_start = datetime.now().replace(second=0, microsecond=0)
        window_end = datetime.now()
        
        for code, count in error_counts.items():
            if code == 500 and count >= ERROR_500_THRESHOLD:
                alert = {
                    "alert_type": "HIGH_500_ERRORS",
                    "error_code": 500,
                    "error_count": count,
                    "threshold": ERROR_500_THRESHOLD,
                    "window_start": window_start,
                    "window_end": window_end,
                    "detected_at": datetime.now(),
                    "severity": "CRITICAL",
                    "batch_number": batch_num + 1
                }
                collection.insert_one(alert)
                print(f"   🚨 ALERTE CRITIQUE: {count} erreurs 500 (seuil: {ERROR_500_THRESHOLD})")
            
            elif code == 404 and count >= ERROR_404_THRESHOLD:
                alert = {
                    "alert_type": "HIGH_404_ERRORS",
                    "error_code": 404,
                    "error_count": count,
                    "threshold": ERROR_404_THRESHOLD,
                    "window_start": window_start,
                    "window_end": window_end,
                    "detected_at": datetime.now(),
                    "severity": "WARNING",
                    "batch_number": batch_num + 1
                }
                collection.insert_one(alert)
                print(f"   ⚠️  ALERTE WARNING: {count} erreurs 404 (seuil: {ERROR_404_THRESHOLD})")
    else:
        print(f"   ✅ Aucune erreur détectée dans ce batch")
    
    print()
    time.sleep(2)  # Simuler le délai entre les batch

# Statistiques finales
print("=" * 70)
print("📊 STATISTIQUES FINALES")
print("=" * 70)

total_alerts = collection.count_documents({})
critical_alerts = collection.count_documents({"severity": "CRITICAL"})
warning_alerts = collection.count_documents({"severity": "WARNING"})

print(f"✅ Total alertes générées: {total_alerts}")
print(f"   🚨 Alertes CRITICAL (500): {critical_alerts}")
print(f"   ⚠️  Alertes WARNING (404): {warning_alerts}")

print("\n" + "=" * 70)
print("✅ Simulation streaming terminée avec succès!")
print("=" * 70)

print("\n📋 Pour voir les alertes dans MongoDB:")
print("   docker exec -it mongodb mongosh")
print("   use logs_analytics")
print("   db.error_alerts.find().pretty()")

spark.stop()
client.close()
