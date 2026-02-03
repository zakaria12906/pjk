#!/usr/bin/env python3
"""
Générateur de logs web pour un site e-commerce de cosmétiques
Format: Apache Common Log Format
"""

import random
from datetime import datetime, timedelta

# Configuration
NUM_LOGS = 10000  # Nombre de lignes à générer
OUTPUT_FILE = "web_server.log"

# Données de base
IPS = [
    "192.168.1.100", "192.168.1.101", "192.168.1.102", "192.168.2.11",
    "192.168.2.22", "192.168.3.56", "192.168.4.78", "192.168.5.90",
    "192.168.7.89", "192.168.8.45", "10.0.0.1", "10.0.0.2",
    "172.16.0.100", "172.16.0.101", "203.0.113.45", "203.0.113.46"
]

# Produits cosmétiques avec IDs
PRODUCTS = [
    # Maquillage
    ("/products/lipstick", range(100, 120)),
    ("/products/foundation", range(200, 215)),
    ("/products/mascara", range(1, 10)),
    ("/products/eyeliner", range(4560, 4570)),
    ("/products/blush", range(300, 310)),
    
    # Soins de la peau
    ("/products/skincare/cream", range(500, 520)),
    ("/products/skincare/sunscreen", range(1, 20)),
    ("/products/skincare/serum", range(600, 615)),
    ("/products/skincare/moisturizer", range(700, 710)),
    
    # Soins capillaires
    ("/products/hair/shampoo", range(4820, 4835)),
    ("/products/hair/conditioner", range(5000, 5015)),
    ("/products/hair/mask", range(5100, 5110)),
]

# Pages fonctionnelles
FUNCTIONAL_PAGES = [
    "/cart",
    "/checkout",
    "/user/login",
    "/user/register",
    "/user/profile",
    "/search",
    "/",
    "/about",
    "/contact"
]

# Méthodes HTTP avec probabilités
HTTP_METHODS = {
    "GET": 0.85,     # 85% GET
    "POST": 0.13,    # 13% POST
    "PUT": 0.01,     # 1% PUT
    "DELETE": 0.01   # 1% DELETE
}

# Codes HTTP avec probabilités
HTTP_CODES = {
    200: 0.80,   # 80% succès
    301: 0.05,   # 5% redirections
    404: 0.10,   # 10% non trouvé
    500: 0.03,   # 3% erreur serveur
    403: 0.02    # 2% accès refusé
}

# Tailles de réponse (en octets) selon le code
RESPONSE_SIZES = {
    200: (500, 10000),   # Succès: 500B - 10KB
    301: (200, 600),     # Redirection: 200B - 600B
    404: (800, 1500),    # Not found: 800B - 1.5KB
    500: (300, 1000),    # Erreur: 300B - 1KB
    403: (400, 900)      # Forbidden: 400B - 900B
}

def weighted_choice(choices):
    """Sélection pondérée basée sur les probabilités"""
    items = list(choices.keys())
    weights = list(choices.values())
    return random.choices(items, weights=weights)[0]

def generate_url():
    """Génère une URL aléatoire (produit ou page fonctionnelle)"""
    if random.random() < 0.70:  # 70% produits, 30% pages fonctionnelles
        product_path, id_range = random.choice(PRODUCTS)
        product_id = random.choice(list(id_range))
        return f"{product_path}?id={product_id}"
    else:
        return random.choice(FUNCTIONAL_PAGES)

def generate_log_line(timestamp):
    """Génère une ligne de log au format Apache Common Log"""
    ip = random.choice(IPS)
    method = weighted_choice(HTTP_METHODS)
    url = generate_url()
    http_code = weighted_choice(HTTP_CODES)
    size_range = RESPONSE_SIZES[http_code]
    response_size = random.randint(size_range[0], size_range[1])
    
    # Format: IP - - [timestamp] "METHOD URL HTTP/1.1" CODE SIZE
    time_str = timestamp.strftime("%d/%b/%Y:%H:%M:%S +0000")
    log_line = f'{ip} - - [{time_str}] "{method} {url} HTTP/1.1" {http_code} {response_size}'
    
    return log_line

def generate_logs():
    """Génère le fichier complet de logs"""
    print(f"🚀 Génération de {NUM_LOGS} lignes de logs...")
    
    # Date de début: 28 janvier 2025
    start_date = datetime(2025, 1, 28, 10, 0, 0)
    
    logs = []
    
    for i in range(NUM_LOGS):
        # Incrément temporel aléatoire (0-10 secondes)
        time_increment = timedelta(seconds=random.randint(0, 10))
        current_time = start_date + (time_increment * i)
        
        log_line = generate_log_line(current_time)
        logs.append(log_line)
        
        # Progression
        if (i + 1) % 1000 == 0:
            print(f"  ✓ {i + 1}/{NUM_LOGS} lignes générées")
    
    # Écriture dans le fichier
    with open(OUTPUT_FILE, 'w') as f:
        f.write('\n'.join(logs))
    
    print(f"\n✅ Fichier '{OUTPUT_FILE}' créé avec succès!")
    print(f"📊 Statistiques:")
    print(f"  - Nombre de lignes: {NUM_LOGS}")
    print(f"  - Taille du fichier: {len('\n'.join(logs)) / 1024:.2f} KB")
    print(f"  - Période couverte: {start_date} à {current_time}")
    
    # Statistiques des codes HTTP générés
    code_counts = {}
    for log in logs:
        code = log.split('"')[2].split()[0]
        code_counts[code] = code_counts.get(code, 0) + 1
    
    print(f"\n📈 Répartition des codes HTTP:")
    for code, count in sorted(code_counts.items()):
        percentage = (count / NUM_LOGS) * 100
        print(f"  - {code}: {count} ({percentage:.1f}%)")

if __name__ == "__main__":
    generate_logs()
