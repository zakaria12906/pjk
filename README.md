# TP Avancé - Analyse de Logs Web avec Architecture Big Data

## Description

Analyse de logs web d'un site e-commerce de cosmétiques utilisant une architecture Big Data distribuée (HDFS, Spark, Kafka, MongoDB).

---

## 📁 Structure du Projet

```
Projet_charazad/
├── docker-compose.yml              # Orchestration des services
├── data/
│   └── web_server.log             # Fichier de logs à analyser
├── spark/
│   ├── requirements.txt           # pyspark, pymongo
│   ├── batch/
│   │   └── top_products.py        # Analyse batch: Top 10 produits
│   └── streaming/
│       └── error_detection.py     # Analyse streaming: Détection erreurs
└── kafka/
    ├── requirements.txt           # kafka-python
    └── log_producer.py            # Producteur Kafka
```

---

## 🎯 Analyses Implémentées

### 1. Analyse Batch - Top 10 Produits

- **Fichier**: `spark/batch/top_products.py`
- **Objectif**: Identifier les produits les plus consultés
- **Source**: HDFS (`/logs/web_server.log`)
- **Output**: MongoDB (`logs_analytics.top_products`)

### 2. Analyse Streaming - Détection d'Erreurs

- **Fichier**: `spark/streaming/error_detection.py`
- **Objectif**: Détecter pics d'erreurs 404/500 sur fenêtre 5 minutes
- **Source**: Kafka (topic `web-logs`)
- **Output**: MongoDB (`logs_analytics.error_alerts`)

---

## 🏗️ Architecture

7 services Docker orchestrés:

| Service | Port | Rôle |
|---------|------|------|
| namenode | 9870, 9000 | HDFS NameNode |
| datanode | 9864 | HDFS DataNode |
| spark-master | 8080, 7077 | Spark Master |
| spark-worker | 8081 | Spark Worker |
| zookeeper | 2181 | Coordination |
| kafka | 9092 | Message Broker |
| mongodb | 27017 | Base de données |

---

## 🚀 Installation et Exécution

### 1. Démarrer les services

```bash
docker-compose up -d
sleep 120  # Attendre 2 minutes
```

### 2. Préparer HDFS

```bash
docker exec namenode hdfs dfs -mkdir -p /logs
docker exec namenode hdfs dfs -chmod -R 777 /logs
docker exec namenode hdfs dfs -put /data/web_server.log /logs/
```

### 3. Exécuter l'analyse Batch

```bash
docker exec spark-master spark-submit \
  --master spark://spark-master:7077 \
  --packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 \
  /spark-apps/batch/top_products.py
```

**Résultats**:
```bash
docker exec -it mongodb mongo
> use logs_analytics
> db.top_products.find().pretty()
```

### 4. Exécuter l'analyse Streaming

**Terminal 1 - Producteur**:
```bash
docker exec -it kafka bash
cd /kafka-apps
pip3 install -r requirements.txt
python3 log_producer.py
# Choisir: 2 (ERRORS), Durée: 300
```

**Terminal 2 - Spark Streaming**:
```bash
docker exec spark-master spark-submit \
  --master spark://spark-master:7077 \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0,org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 \
  /spark-apps/streaming/error_detection.py
```

**Résultats** (après 5-6 minutes):
```bash
docker exec -it mongodb mongo
> use logs_analytics
> db.error_alerts.find().sort({detected_at: -1}).pretty()
```

---

## 📊 Interfaces Web

- **HDFS**: http://localhost:9870
- **Spark Master**: http://localhost:8080
- **Spark Worker**: http://localhost:8081

---

## 🛑 Arrêter

```bash
docker-compose down
```

Pour supprimer les volumes (données):
```bash
docker-compose down -v
```

---

## 🛠️ Technologies

- HDFS 3.2.1 - Stockage distribué
- Apache Spark 3.3.0 - Traitement batch et streaming
- Apache Kafka 7.3.0 - Streaming de données
- MongoDB 6.0 - Stockage des résultats
- Docker & Docker Compose - Orchestration

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

https://github.com/zakaria12906/pjk.git
