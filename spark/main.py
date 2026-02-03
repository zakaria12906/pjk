#!/usr/bin/env python3
"""
PROJET BIG DATA - Script Principal
===================================
Lance automatiquement les 2 analyses :
1. BATCH - Top 10 produits les plus consultés
2. STREAMING - Détection d'erreurs en temps réel
"""

import sys
import subprocess
from pyspark.sql import SparkSession

def print_banner(text):
    """Affiche un bandeau formaté"""
    print("\n" + "=" * 70)
    print(text)
    print("=" * 70 + "\n")

def run_analysis(script_path, name):
    """Exécute un script d'analyse"""
    print_banner(f"🚀 Lancement: {name}")
    
    try:
        # Exécuter le script Python
        exec(open(script_path).read(), {'__name__': '__main__'})
        print(f"\n✅ {name} terminée avec succès!\n")
        return True
    except Exception as e:
        print(f"\n❌ Erreur dans {name}: {e}\n")
        return False

def main():
    print_banner("🎯 PROJET BIG DATA - Analyse de Logs Web")
    print("📊 2 analyses vont être exécutées:")
    print("   1. BATCH - Top 10 produits")
    print("   2. STREAMING - Détection erreurs 404/500")
    print()
    
    # Chemin des analyses
    batch_script = "/spark-apps/batch/top_products_mongodb.py"
    streaming_script = "/spark-apps/streaming/error_detection_simple.py"
    
    # Lancer les analyses
    success_batch = run_analysis(batch_script, "Analyse BATCH")
    success_streaming = run_analysis(streaming_script, "Analyse STREAMING")
    
    # Résumé
    print_banner("📊 RÉSUMÉ DES ANALYSES")
    
    if success_batch and success_streaming:
        print("✅ Toutes les analyses ont réussi!")
        print()
        print("📊 Résultats disponibles dans MongoDB:")
        print("   - Collection: logs_analytics.top_products")
        print("   - Collection: logs_analytics.error_alerts")
        print()
        print("💡 Pour consulter les résultats:")
        print("   docker exec -it mongodb mongosh")
        print("   use logs_analytics")
        print("   db.top_products.find().pretty()")
        print("   db.error_alerts.find().pretty()")
        print()
        return 0
    else:
        print("❌ Certaines analyses ont échoué")
        if not success_batch:
            print("   - Analyse BATCH: ÉCHEC")
        if not success_streaming:
            print("   - Analyse STREAMING: ÉCHEC")
        return 1

if __name__ == "__main__":
    sys.exit(main())
