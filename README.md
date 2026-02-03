# TP Avancé - Analyse de Logs Web avec Architecture Big Data

## Description

Projet d'analyse de logs web d'un site e-commerce de cosmétiques utilisant une architecture Big Data distribuée.

**Dépôt GitHub**: https://github.com/zakaria12906/pjk.git

---

## 📁 Structure du Projet

```
Projet_charazad/
├── README.md                          # Ce fichier
├── docker-compose.yml                 # Orchestration des services
├── .gitignore
│
├── data/
│   └── web_server.log                # Fichier de logs (40 lignes)
│
├── spark/
│   ├── requirements.txt              # pyspark==3.3.0, pymongo==4.3.3
│   ├── batch/
│   │   └── top_products.py           # Analyse batch: Top 10 produits
│   └── streaming/
│       └── error_detection.py        # Analyse streaming: Détection erreurs
│
└── kafka/
    ├── requirements.txt              # kafka-python==2.0.2
    └── log_producer.py               # Producteur Kafka
```

---

## 🎯 Analyses Implémentées

### 1. Analyse Batch - Produits les Plus Consultés

**Fichier**: `spark/batch/top_products.py`

**Objectif**: Identifier les 10 produits (par leur ID) ayant reçu le plus de requêtes.

**Algorithme**:
- Lecture des logs depuis HDFS
- Parsing et extraction des IDs de produits
- Comptage par ID avec MapReduce
- Tri décroissant et sélection du Top 10
- Sauvegarde dans MongoDB

**Collection MongoDB**: `logs_analytics.top_products`

---

### 2. Analyse Streaming - Détection d'Erreurs en Temps Réel

**Fichier**: `spark/streaming/error_detection.py`

**Objectif**: Surveiller les logs pour détecter des pics d'erreurs (codes 404 ou 500) sur un intervalle de 5 minutes.

**Méthode**:
- Consommation depuis Kafka (topic: `web-logs`)
- Fenêtrage temporel: 5 minutes (slide 1 minute)
- Filtrage des codes 404 et 500
- Génération d'alertes si:
  - Erreurs 500 > 10
  - Erreurs 404 > 30
- Sauvegarde des alertes dans MongoDB

**Collection MongoDB**: `logs_analytics.error_alerts`

---

## 🏗️ Architecture Big Data

```
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│  Web Server  │ -->  │    HDFS      │ -->  │ Spark Batch  │
│   (Logs)     │      │  (Storage)   │      │  Processing  │
└──────────────┘      └──────────────┘      └──────┬───────┘
                                                    │
                                                    ▼
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│ Log Producer │ -->  │    Kafka     │ -->  │Spark Stream  │
│  (Simulator) │      │  (Streaming) │      │  Processing  │
└──────────────┘      └──────────────┘      └──────┬───────┘
                                                    │
                                                    ▼
                                            ┌──────────────┐
                                            │   MongoDB    │
                                            │  (Results)   │
                                            └──────────────┘
```

### Services Docker

| Service | Image | Port | Rôle |
|---------|-------|------|------|
| namenode | bde2020/hadoop-namenode:2.0.0 | 9870, 9000 | HDFS NameNode |
| datanode | bde2020/hadoop-datanode:2.0.0 | 9864 | HDFS DataNode |
| spark-master | bitnami/spark:3.3.0 | 8080, 7077 | Spark Master |
| spark-worker | bitnami/spark:3.3.0 | 8081 | Spark Worker |
| zookeeper | confluentinc/cp-zookeeper:7.3.0 | 2181 | Coordination |
| kafka | confluentinc/cp-kafka:7.3.0 | 9092, 9093 | Message Broker |
| mongodb | mongo:6.0 | 27017 | Base de données |

---

## 🚀 Installation et Exécution

### Prérequis
- Docker >= 20.10
- Docker Compose >= 2.0
- 8GB RAM minimum
- Python 3.7+

### 1. Démarrer les services

```bash
cd /Users/zakariaeelouazzani/Desktop/Projet_charazad

docker-compose up -d

# Vérifier que tous les services sont démarrés
docker-compose ps
```

**Attendez ~2 minutes que tous les services soient prêts.**

### 2. Préparer HDFS

```bash
# Créer les répertoires dans HDFS
docker exec namenode hdfs dfs -mkdir -p /logs
docker exec namenode hdfs dfs -chmod -R 777 /logs

# Copier les logs dans HDFS
docker exec namenode hdfs dfs -put /data/web_server.log /logs/

# Vérifier
docker exec namenode hdfs dfs -ls /logs
```

### 3. Exécuter l'analyse Batch

```bash
docker exec spark-master spark-submit \
  --master spark://spark-master:7077 \
  --packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 \
  /spark-apps/batch/top_products.py
```

**Consulter les résultats**:
```bash
docker exec -it mongodb mongo
> use logs_analytics
> db.top_products.find().pretty()
```

### 4. Exécuter l'analyse Streaming

**Terminal 1 - Démarrer le producteur Kafka**:
```bash
docker exec -it kafka bash
cd /kafka-apps
python3 log_producer.py

# Dans le menu, choisir:
# 2. ERRORS (pour tester la détection d'erreurs)
# Durée: 300 secondes
```

**Terminal 2 - Démarrer Spark Streaming**:
```bash
docker exec spark-master spark-submit \
  --master spark://spark-master:7077 \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0,org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 \
  /spark-apps/streaming/error_detection.py
```

**Terminal 3 - Consulter les alertes**:
```bash
docker exec -it mongodb mongo
> use logs_analytics
> db.error_alerts.find().sort({detected_at: -1}).pretty()
```

---

## 📊 Interfaces Web

| Service | URL | Description |
|---------|-----|-------------|
| HDFS NameNode | http://localhost:9870 | Interface web HDFS |
| Spark Master | http://localhost:8080 | Interface Spark Master |
| Spark Worker | http://localhost:8081 | État Worker |

---

## 🛑 Arrêter les Services

```bash
docker-compose down
```

Pour supprimer également les volumes (données):
```bash
docker-compose down -v
```

---

## 🛠️ Technologies Utilisées

- **HDFS** 3.2.1 - Stockage distribué
- **Apache Spark** 3.3.0 - Traitement batch et streaming
- **Apache Kafka** 7.3.0 - Streaming de données
- **Zookeeper** 7.3.0 - Coordination
- **MongoDB** 6.0 - Stockage des résultats
- **Docker** & **Docker Compose** - Orchestration

---

## 📝 Justifications Techniques

### Pourquoi HDFS ?
- Tolérance aux pannes (réplication)
- Scalabilité horizontale
- Intégration native avec Spark

### Pourquoi Spark ?
- Performance in-memory (100x MapReduce)
- API unifiée batch + streaming
- Support Python (PySpark)

### Pourquoi Kafka ?
- Débit massif
- Persistance durable
- Découplage producteur/consommateur

### Pourquoi MongoDB ?
- Schéma flexible (JSON)
- Performance avec index
- Connector Spark natif

---

## 📚 Livrables

Conformément au sujet du TP, ce projet contient:

1. ✅ **Code source des traitements Spark**:
   - `spark/batch/top_products.py`
   - `spark/streaming/error_detection.py`

2. ✅ **Fichier docker-compose.yml**:
   - Orchestration de 7 services (Hadoop, Spark, Kafka, MongoDB)

3. ✅ **Architecture distribuée fonctionnelle**:
   - HDFS pour stockage
   - Spark pour traitement (batch + stream)
   - Communication inter-services vérifiée

---

## 🐛 Dépannage

### Port déjà utilisé
```bash
lsof -i :9870
kill -9 <PID>
```

### HDFS en safe mode
```bash
docker exec namenode hdfs dfsadmin -safemode leave
```

### Voir les logs
```bash
docker logs -f spark-master
docker logs -f kafka
```

---

## 📦 Dépôt GitHub

**URL**: https://github.com/zakaria12906/pjk.git

```bash
git clone https://github.com/zakaria12906/pjk.git
cd pjk
```

---

**Projet réalisé dans le cadre du TP Avancé - Big Data**
