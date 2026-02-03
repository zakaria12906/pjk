#!/usr/bin/env python3
"""
Producteur Kafka: Simulateur de Logs en Temps Réel
===================================================

Objectif:
    Générer et envoyer des logs web vers Kafka pour simuler
    un flux de données en temps réel.

Fonctionnalités:
    - Génération continue de logs réalistes
    - Simulation de pics d'erreurs (pour tester les alertes)
    - Simulation de produits en tendance
    - Contrôle du débit (logs/seconde)
    - Modes: normal, errors, trending

Architecture:
    Log Generator → Kafka Producer → Kafka Topic (web-logs)
"""

import random
import time
from datetime import datetime
from kafka import KafkaProducer
import json
import sys

# Configuration Kafka
KAFKA_BOOTSTRAP_SERVERS = ['localhost:9092']
KAFKA_TOPIC = 'web-logs'

# Configuration de la génération
LOGS_PER_SECOND = 10  # Débit normal
BATCH_SIZE = 10       # Nombre de logs envoyés par batch

# Données de simulation
IPS = [
    "192.168.1.100", "192.168.1.101", "192.168.1.102", "192.168.2.11",
    "192.168.2.22", "192.168.3.56", "192.168.4.78", "192.168.5.90",
    "192.168.7.89", "192.168.8.45", "10.0.0.1", "10.0.0.2",
    "172.16.0.100", "172.16.0.101", "203.0.113.45", "203.0.113.46"
]

# Produits cosmétiques
PRODUCTS = {
    "makeup": [
        ("lipstick", range(100, 120)),
        ("foundation", range(200, 215)),
        ("mascara", range(1, 10)),
        ("eyeliner", range(4560, 4570)),
        ("blush", range(300, 310))
    ],
    "skincare": [
        ("cream", range(500, 520)),
        ("sunscreen", range(1, 20)),
        ("serum", range(600, 615)),
        ("moisturizer", range(700, 710))
    ],
    "hair": [
        ("shampoo", range(4820, 4835)),
        ("conditioner", range(5000, 5015)),
        ("mask", range(5100, 5110))
    ]
}

FUNCTIONAL_PAGES = [
    "/cart", "/checkout", "/user/login", "/user/register",
    "/user/profile", "/search", "/", "/about", "/contact"
]

# Probabilités par mode
MODES = {
    "normal": {
        "200": 0.80, "301": 0.05, "404": 0.10, "500": 0.03, "403": 0.02
    },
    "errors": {
        "200": 0.40, "301": 0.05, "404": 0.30, "500": 0.20, "403": 0.05
    },
    "trending": {
        "200": 0.95, "301": 0.02, "404": 0.02, "500": 0.01, "403": 0.00
    }
}

# Produit en tendance (pour le mode trending)
TRENDING_PRODUCT_ID = 105
TRENDING_PRODUCT_TYPE = "lipstick"

def create_producer():
    """Crée et configure le producteur Kafka"""
    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: v.encode('utf-8'),
            acks='all',
            retries=3
        )
        print("✅ Connexion à Kafka réussie")
        return producer
    except Exception as e:
        print(f"❌ Erreur de connexion à Kafka: {e}")
        sys.exit(1)

def weighted_choice(choices):
    """Sélection pondérée"""
    items = list(choices.keys())
    weights = list(choices.values())
    return random.choices(items, weights=weights)[0]

def generate_url(mode="normal"):
    """
    Génère une URL selon le mode
    
    Args:
        mode: "normal", "errors", ou "trending"
    """
    if mode == "trending":
        # En mode trending, 60% du trafic va vers le produit tendance
        if random.random() < 0.60:
            return f"/products/{TRENDING_PRODUCT_TYPE}?id={TRENDING_PRODUCT_ID}"
    
    # Sinon, génération normale
    if random.random() < 0.70:  # 70% produits
        category = random.choice(list(PRODUCTS.keys()))
        product_type, id_range = random.choice(PRODUCTS[category])
        
        if category == "makeup":
            path = f"/products/{product_type}"
        else:
            path = f"/products/{category}/{product_type}"
        
        product_id = random.choice(list(id_range))
        return f"{path}?id={product_id}"
    else:
        return random.choice(FUNCTIONAL_PAGES)

def generate_log(mode="normal"):
    """
    Génère une ligne de log selon le mode
    
    Args:
        mode: "normal", "errors", ou "trending"
    
    Returns:
        str: Ligne de log au format Apache
    """
    ip = random.choice(IPS)
    method = "GET" if random.random() < 0.85 else "POST"
    url = generate_url(mode)
    
    # Code HTTP selon le mode
    http_code = int(weighted_choice(MODES[mode]))
    
    # Taille de réponse selon le code
    size_ranges = {
        200: (500, 10000),
        301: (200, 600),
        404: (800, 1500),
        500: (300, 1000),
        403: (400, 900)
    }
    size_range = size_ranges.get(http_code, (300, 1000))
    response_size = random.randint(size_range[0], size_range[1])
    
    # Timestamp actuel
    timestamp = datetime.now().strftime("%d/%b/%Y:%H:%M:%S +0000")
    
    # Format Apache Common Log
    log_line = f'{ip} - - [{timestamp}] "{method} {url} HTTP/1.1" {http_code} {response_size}'
    
    return log_line

def send_logs(producer, mode="normal", duration=60):
    """
    Envoie des logs vers Kafka pendant une durée donnée
    
    Args:
        producer: KafkaProducer instance
        mode: Mode de génération
        duration: Durée en secondes (None = infini)
    """
    print(f"\n🚀 Démarrage de l'envoi de logs (mode: {mode})")
    print(f"   • Débit: {LOGS_PER_SECOND} logs/seconde")
    print(f"   • Topic: {KAFKA_TOPIC}")
    
    if duration:
        print(f"   • Durée: {duration} secondes\n")
    else:
        print(f"   • Durée: Infini (Ctrl+C pour arrêter)\n")
    
    start_time = time.time()
    total_sent = 0
    errors = 0
    
    try:
        while True:
            # Vérifier la durée
            if duration and (time.time() - start_time) >= duration:
                break
            
            # Générer et envoyer un batch de logs
            for _ in range(BATCH_SIZE):
                log_line = generate_log(mode)
                
                try:
                    producer.send(KAFKA_TOPIC, value=log_line)
                    total_sent += 1
                except Exception as e:
                    errors += 1
                    print(f"❌ Erreur d'envoi: {e}")
            
            # Afficher la progression
            if total_sent % 100 == 0:
                elapsed = time.time() - start_time
                rate = total_sent / elapsed if elapsed > 0 else 0
                print(f"📊 {total_sent} logs envoyés | {rate:.1f} logs/sec | Erreurs: {errors}")
            
            # Attendre pour respecter le débit
            time.sleep(BATCH_SIZE / LOGS_PER_SECOND)
    
    except KeyboardInterrupt:
        print("\n\n🛑 Arrêt demandé par l'utilisateur...")
    
    finally:
        # Statistiques finales
        elapsed = time.time() - start_time
        print("\n" + "="*60)
        print("📊 STATISTIQUES FINALES")
        print("="*60)
        print(f"   • Logs envoyés: {total_sent}")
        print(f"   • Durée: {elapsed:.1f} secondes")
        print(f"   • Débit moyen: {total_sent/elapsed:.1f} logs/sec")
        print(f"   • Erreurs: {errors}")
        print("="*60 + "\n")
        
        producer.flush()
        producer.close()

def interactive_menu():
    """Menu interactif pour choisir le mode"""
    print("\n" + "="*60)
    print("🎛️  SIMULATEUR DE LOGS WEB - MENU INTERACTIF")
    print("="*60)
    print("\nChoisissez un mode de simulation:\n")
    print("  1. 📊 NORMAL - Trafic normal (80% succès, 10% 404, 3% 500)")
    print("  2. 🚨 ERRORS - Pic d'erreurs (40% succès, 30% 404, 20% 500)")
    print("  3. 🔥 TRENDING - Produit en tendance (95% succès, produit #105)")
    print("  4. 🔄 CYCLE - Alterner entre les modes (30s chacun)")
    print("  5. ❌ QUITTER\n")
    
    choice = input("Votre choix (1-5): ").strip()
    
    if choice == "1":
        return "normal"
    elif choice == "2":
        return "errors"
    elif choice == "3":
        return "trending"
    elif choice == "4":
        return "cycle"
    elif choice == "5":
        return None
    else:
        print("❌ Choix invalide")
        return interactive_menu()

def cycle_modes(producer):
    """Cycle entre les différents modes"""
    modes = ["normal", "errors", "trending"]
    cycle_duration = 30  # secondes par mode
    
    print("\n🔄 MODE CYCLE - Alternance entre les modes toutes les 30 secondes")
    print("   Appuyez sur Ctrl+C pour arrêter\n")
    
    try:
        while True:
            for mode in modes:
                print(f"\n{'='*60}")
                print(f"🔄 Changement de mode: {mode.upper()}")
                print(f"{'='*60}\n")
                send_logs(producer, mode=mode, duration=cycle_duration)
                
                # Recréer le producer après chaque cycle
                producer = create_producer()
    
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du cycle")

def main():
    """Fonction principale"""
    print("\n" + "="*60)
    print("🎯 PRODUCTEUR KAFKA - SIMULATEUR DE LOGS WEB")
    print("="*60)
    
    # Créer le producteur
    producer = create_producer()
    
    # Menu interactif
    mode = interactive_menu()
    
    if mode is None:
        print("\n👋 Au revoir!\n")
        return
    
    if mode == "cycle":
        cycle_modes(producer)
    else:
        # Demander la durée
        print(f"\nCombien de temps générer des logs? (en secondes, 0 = infini)")
        duration_input = input("Durée: ").strip()
        
        try:
            duration = int(duration_input) if duration_input != "0" else None
        except ValueError:
            duration = 60  # Défaut: 1 minute
        
        # Envoyer les logs
        send_logs(producer, mode=mode, duration=duration)
    
    print("\n✅ Simulation terminée\n")

if __name__ == "__main__":
    main()
