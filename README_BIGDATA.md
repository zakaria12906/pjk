# 🚀 Architecture Distribuée pour l'Analyse de Logs Web

## 📋 Description du Projet

Projet d'analyse de logs web d'un site e-commerce spécialisé dans les cosmétiques utilisant une architecture Big Data distribuée avec Docker.

### Technologies Utilisées
- **HDFS**: Stockage distribué des logs
- **Apache Spark**: Traitement batch et streaming
- **Apache Kafka**: Streaming de données en temps réel
- **MongoDB**: Stockage des résultats d'analyses
- **Docker & Docker Compose**: Orchestration des conteneurs

---

## 🎯 Analyses Implémentées

### 📊 Analyses Batch (sur données statiques)
1. **Top 10 Produits les plus consultés**
   - Identifie les produits ayant reçu le plus de requêtes
   - Output: ID produit + nombre de consultations

2. **Répartition des Codes HTTP**
   - Analyse la fréquence des codes HTTP (200, 404, 500, etc.)
   - KPI de santé du serveur

3. **Top 10 Adresses IP les plus actives**
   - Identifie les IPs générant le plus de requêtes
   - Détection d'activité suspecte (bots, DDoS)

### ⚡ Analyses Streaming (temps réel)
1. **Détection d'erreurs en temps réel**
   - Surveillance des pics d'erreurs 404/500
   - Alerte si > 10 erreurs sur une fenêtre de 5 minutes

2. **Produits en tendance**
   - Identification des produits populaires en temps réel
   - Alerte si > 20 consultations en 1 minute

---

## 🏗️ Architecture Technique

```
┌─────────────────────────────────────────────────────────────┐
│                     ARCHITECTURE BIG DATA                    │
└─────────────────────────────────────────────────────────────┘

┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│  Web Server  │ -->  │    HDFS      │ -->  │ Spark Batch  │
│   (Logs)     │      │  (Storage)   │      │  Processing  │
└──────────────┘      └──────────────┘      └──────────────┘
                                                     │
                                                     ▼
                                            ┌──────────────┐
┌──────────────┐      ┌──────────────┐     │   MongoDB    │
│ Log Producer │ -->  │    Kafka     │     │  (Results)   │
│  (Simulator) │      │  (Streaming) │     └──────────────┘
└──────────────┘      └──────────────┘              ▲
                             │                      │
                             ▼                      │
                      ┌──────────────┐              │
                      │Spark Stream  │ ─────────────┘
                      │  Processing  │
                      └──────────────┘
```

---

## 📁 Structure du Projet

```
bigdata-logs-analysis/
├── docker-compose.yml              # Orchestration des conteneurs
├── README.md                       # Documentation
├── data/
│   ├── web_server.log             # Fichier de logs exemple
│   └── generate_logs.py           # Générateur de logs
├── spark/
│   ├── batch/
│   │   ├── top_products.py        # Analyse: Produits populaires
│   │   ├── http_codes.py          # Analyse: Codes HTTP
│   │   └── top_ips.py             # Analyse: IPs actives
│   ├── streaming/
│   │   ├── error_detection.py     # Streaming: Détection erreurs
│   │   └── trending_products.py   # Streaming: Produits tendance
│   └── requirements.txt            # Dépendances Python
├── kafka/
│   └── log_producer.py            # Producteur Kafka pour simulation
└── config/
    ├── hdfs-site.xml              # Configuration HDFS
    └── spark-defaults.conf        # Configuration Spark
```

---

## 🚀 Installation et Lancement

### Prérequis
- Docker >= 20.10
- Docker Compose >= 2.0
- 8GB RAM minimum
- 20GB d'espace disque

### Étape 1: Cloner et préparer l'environnement

```bash
cd bigdata-logs-analysis

# Créer les répertoires nécessaires
mkdir -p data spark/batch spark/streaming kafka config hdfs namenode datanode
```

### Étape 2: Générer les données de logs

```bash
# Générer un fichier de logs d'exemple
python3 data/generate_logs.py
```

### Étape 3: Démarrer l'architecture

```bash
# Lancer tous les conteneurs
docker-compose up -d

# Vérifier que tous les services sont démarrés
docker-compose ps
```

**Services disponibles:**
- Hadoop NameNode: http://localhost:9870
- Hadoop DataNode: http://localhost:9864
- Spark Master: http://localhost:8080
- Spark Worker: http://localhost:8081
- MongoDB: localhost:27017
- Kafka: localhost:9092
- Zookeeper: localhost:2181

### Étape 4: Préparer HDFS

```bash
# Accéder au conteneur Hadoop
docker exec -it namenode bash

# Créer les répertoires dans HDFS
hdfs dfs -mkdir -p /logs
hdfs dfs -mkdir -p /output

# Copier les logs dans HDFS
hdfs dfs -put /data/web_server.log /logs/

# Vérifier
hdfs dfs -ls /logs
exit
```

---

## 🔧 Exécution des Analyses

### Analyses Batch

#### 1. Top 10 Produits les plus consultés

```bash
docker exec -it spark-master bash

spark-submit \
  --master spark://spark-master:7077 \
  --packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 \
  /spark-apps/batch/top_products.py
```

#### 2. Répartition des Codes HTTP

```bash
spark-submit \
  --master spark://spark-master:7077 \
  --packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 \
  /spark-apps/batch/http_codes.py
```

#### 3. Top 10 IPs les plus actives

```bash
spark-submit \
  --master spark://spark-master:7077 \
  --packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 \
  /spark-apps/batch/top_ips.py
```

### Analyses Streaming

#### 1. Détection d'erreurs en temps réel

```bash
# Terminal 1: Démarrer le consumer Spark Streaming
spark-submit \
  --master spark://spark-master:7077 \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0,org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 \
  /spark-apps/streaming/error_detection.py
```

```bash
# Terminal 2: Démarrer le producer Kafka
docker exec -it kafka bash
python3 /kafka-apps/log_producer.py
```

#### 2. Produits en tendance

```bash
spark-submit \
  --master spark://spark-master:7077 \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0,org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 \
  /spark-apps/streaming/trending_products.py
```

---

## 📊 Consultation des Résultats

### Via MongoDB

```bash
# Accéder à MongoDB
docker exec -it mongodb mongo

# Utiliser la base de données
use logs_analytics

# Voir les collections
show collections

# Top produits
db.top_products.find().pretty()

# Codes HTTP
db.http_codes.find().pretty()

# Top IPs
db.top_ips.find().pretty()

# Alertes erreurs (streaming)
db.error_alerts.find().pretty()

# Produits tendance (streaming)
db.trending_products.find().pretty()
```

### Via HDFS (résultats intermédiaires)

```bash
# Lister les résultats
docker exec -it namenode hdfs dfs -ls /output

# Voir le contenu
docker exec -it namenode hdfs dfs -cat /output/top_products/part-*
```

---

## 🧪 Tests et Validation

### Vérifier la santé des services

```bash
# Vérifier HDFS
docker exec namenode hdfs dfsadmin -report

# Vérifier Spark
curl http://localhost:8080

# Vérifier Kafka topics
docker exec kafka kafka-topics.sh --list --bootstrap-server localhost:9092

# Vérifier MongoDB
docker exec mongodb mongo --eval "db.adminCommand('ping')"
```

### Monitoring des logs

```bash
# Logs Spark Master
docker logs -f spark-master

# Logs Kafka
docker logs -f kafka

# Logs HDFS
docker logs -f namenode
```

---

## 🛠️ Justifications Techniques

### Pourquoi HDFS ?
- **Tolérance aux pannes**: Réplication des blocs (facteur 3 par défaut)
- **Scalabilité**: Ajout facile de DataNodes
- **Performance**: Optimisé pour gros fichiers séquentiels
- **Intégration**: Native avec Spark

### Pourquoi Spark ?
- **Performance**: Traitement in-memory (100x plus rapide que MapReduce)
- **Unification**: Même API pour batch et streaming
- **Écosystème**: MLlib, GraphX, Spark SQL
- **Langage**: Python (PySpark) facile à maintenir

### Pourquoi Kafka ?
- **Débit**: Millions de messages/seconde
- **Persistance**: Logs durables et rejouables
- **Découplage**: Producteurs/consommateurs indépendants
- **Scalabilité**: Partitionnement distribué

### Pourquoi MongoDB ?
- **Flexibilité**: Schéma JSON dynamique
- **Performance**: Index optimisés pour requêtes
- **Agrégation**: Pipeline puissant pour analytics
- **Scalabilité**: Sharding horizontal

### Pourquoi Docker ?
- **Reproductibilité**: Même environnement partout
- **Isolation**: Pas de conflits de dépendances
- **Rapidité**: Déploiement en quelques minutes
- **Portabilité**: Fonctionne sur tout OS

---

## 📈 Améliorations Possibles

1. **Visualisation**: Ajouter Grafana/Kibana pour dashboards
2. **Orchestration**: Utiliser Airflow pour pipelines complexes
3. **ML**: Prédiction de charge avec Spark MLlib
4. **Sécurité**: Authentification Kerberos, TLS
5. **Monitoring**: Prometheus + Alertmanager
6. **Stockage**: Ajouter HBase pour requêtes temps réel

---

## 🐛 Troubleshooting

### Erreur: "Cannot connect to Spark Master"
```bash
docker-compose restart spark-master
docker-compose logs spark-master
```

### Erreur: "HDFS in Safe Mode"
```bash
docker exec namenode hdfs dfsadmin -safemode leave
```

### Erreur: "Kafka connection refused"
```bash
# Vérifier Zookeeper
docker-compose restart zookeeper
# Redémarrer Kafka
docker-compose restart kafka
```

### Mémoire insuffisante
```bash
# Augmenter la mémoire dans docker-compose.yml
SPARK_WORKER_MEMORY=4g
```

---

## 👨‍💻 Auteur

Projet réalisé dans le cadre du cours de Big Data et Data Engineering.

## 📝 Licence

MIT License - Usage académique et éducatif.
