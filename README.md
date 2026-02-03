# 🚀 Projet Charazad - Architecture Big Data pour l'Analyse de Logs Web

## 📋 Description

Projet d'analyse de logs web utilisant une architecture Big Data distribuée avec Docker. Le système analyse les logs d'un site e-commerce de cosmétiques en utilisant **Apache Spark** (batch et streaming), **HDFS**, **Kafka**, et **MongoDB**.

**Dépôt GitHub**: https://github.com/zakaria12906/pjk.git

---

## 🎯 Fonctionnalités

### 📊 Analyses Batch (Données Historiques)
1. **Top 10 Produits** - Produits les plus consultés
2. **Codes HTTP** - KPIs de santé du serveur (taux de succès, erreurs)
3. **Top 10 IPs** - IPs les plus actives avec détection de bots

### ⚡ Analyses Streaming (Temps Réel)
1. **Détection d'Erreurs** - Alertes sur pics d'erreurs 404/500 (fenêtre 5 min)
2. **Produits Tendance** - Produits populaires en temps réel (>20 vues/min)

---

## 🏗️ Architecture

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

**Services Docker:**
- **HDFS**: NameNode (9870) + DataNode (9864)
- **Spark**: Master (8080, 7077) + Worker (8081)
- **Kafka**: Broker (9092, 9093) + Zookeeper (2181)
- **MongoDB**: Database (27017)

---

## 📁 Structure du Projet

```
Projet_charazad/
├── README.md                      # Ce fichier
├── ARCHITECTURE.md                # Justifications techniques détaillées
├── QUICKSTART.md                  # Guide démarrage rapide (10 min)
├── LIVRABLE.md                    # Document de livraison
├── INDEX.md                       # Navigation dans le projet
├── docker-compose.yml             # Orchestration des services
│
├── data/
│   ├── web_server.log            # Logs d'exemple (40 lignes)
│   └── generate_logs.py          # Générateur de logs (10k lignes)
│
├── spark/
│   ├── requirements.txt          # pyspark, pymongo
│   ├── batch/
│   │   ├── top_products.py       # Analyse #1: Top produits
│   │   ├── http_codes.py         # Analyse #2: Codes HTTP
│   │   └── top_ips.py            # Analyse #3: Top IPs
│   └── streaming/
│       ├── error_detection.py    # Streaming #1: Détection erreurs
│       └── trending_products.py  # Streaming #2: Produits tendance
│
├── kafka/
│   ├── requirements.txt          # kafka-python
│   └── log_producer.py           # Producteur Kafka (simulation)
│
└── scripts/
    ├── setup.sh                  # Configuration initiale
    ├── prepare_hdfs.sh           # Préparation HDFS
    ├── run_batch.sh              # Lancer analyses batch
    ├── run_streaming.sh          # Guide streaming
    ├── stop.sh                   # Arrêter les services
    └── clean.sh                  # Nettoyage complet
```

---

## 🚀 Installation et Démarrage Rapide

### Prérequis
- Docker >= 20.10
- Docker Compose >= 2.0
- 8GB RAM minimum
- 20GB espace disque
- Python 3.7+

### Démarrage en 5 Étapes (10 minutes)

#### 1. Configuration initiale (2 min)
```bash
cd /Users/zakariaeelouazzani/Desktop/Projet_charazad
chmod +x scripts/*.sh
./scripts/setup.sh
```

#### 2. Démarrer les services (3 min)
```bash
docker-compose up -d

# Vérifier que tous les services sont actifs
docker-compose ps
```

**Attendez ~2 minutes que tous les services démarrent.**

#### 3. Préparer HDFS (1 min)
```bash
./scripts/prepare_hdfs.sh
```

#### 4. Lancer les analyses batch (2 min)
```bash
./scripts/run_batch.sh
```

Cela lance séquentiellement:
- Top 10 Produits (~30s)
- Répartition Codes HTTP (~30s)
- Top 10 IPs Actives (~30s)

#### 5. Consulter les résultats (1 min)
```bash
docker exec -it mongodb mongo

# Dans le shell MongoDB:
use logs_analytics
show collections

# Voir les résultats
db.top_products.find().pretty()
db.http_codes_detailed.find().pretty()
db.top_ips.find().pretty()
```

---

## 📊 Interfaces Web

| Service | URL | Description |
|---------|-----|-------------|
| HDFS NameNode | http://localhost:9870 | Browse HDFS files |
| HDFS DataNode | http://localhost:9864 | DataNode status |
| Spark Master | http://localhost:8080 | Cluster overview |
| Spark Worker | http://localhost:8081 | Worker status |

---

## ⚡ Tester le Streaming (Optionnel)

### Terminal 1: Producteur Kafka
```bash
docker exec -it kafka bash
cd /kafka-apps
python3 log_producer.py

# Dans le menu:
# 1. Choisir "2" pour mode ERRORS (pic d'erreurs)
# 2. Durée: 300 secondes (5 minutes)
```

### Terminal 2: Détection d'erreurs
```bash
docker exec -it spark-master bash

spark-submit \
  --master spark://spark-master:7077 \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0,org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 \
  /spark-apps/streaming/error_detection.py
```

### Terminal 3: Voir les alertes
```bash
docker exec -it mongodb mongo

use logs_analytics
# Rafraîchir toutes les 5 secondes
db.error_alerts.find().sort({detected_at: -1}).limit(5).pretty()
```

---

## 🛑 Arrêter les Services

```bash
./scripts/stop.sh

# OU directement
docker-compose down
```

---

## 🧹 Nettoyage Complet

**⚠️ ATTENTION: Supprime toutes les données !**

```bash
./scripts/clean.sh
```

---

## 🐛 Dépannage

### Erreur: "Cannot connect to Docker daemon"
```bash
# Démarrer Docker Desktop (Mac/Windows)
# OU sur Linux:
sudo systemctl start docker
```

### Erreur: "Port already in use"
```bash
# Trouver le processus (exemple: 9870)
lsof -i :9870
kill -9 <PID>
```

### Erreur: "HDFS in safe mode"
```bash
docker exec namenode hdfs dfsadmin -safemode leave
```

### Spark job échoue avec OutOfMemory
```bash
# Augmenter la mémoire dans docker-compose.yml
SPARK_WORKER_MEMORY=4G  # au lieu de 2G
docker-compose restart spark-worker
```

---

## 🛠️ Justifications Techniques

### Pourquoi HDFS ?
- ✅ Tolérance aux pannes (réplication)
- ✅ Scalabilité horizontale
- ✅ Intégration native avec Spark
- ✅ Optimisé pour gros fichiers

### Pourquoi Spark ?
- ✅ Performance in-memory (100x MapReduce)
- ✅ API unifiée batch + streaming
- ✅ Écosystème riche (MLlib, SQL)
- ✅ Support Python (PySpark)

### Pourquoi Kafka ?
- ✅ Débit massif (millions msg/sec)
- ✅ Persistance durable
- ✅ Découplage producteur/consommateur
- ✅ Rejouabilité des messages

### Pourquoi MongoDB ?
- ✅ Schéma flexible (JSON)
- ✅ Performance (index B-tree)
- ✅ Agrégations puissantes
- ✅ Connector Spark natif

Pour plus de détails, voir **[ARCHITECTURE.md](ARCHITECTURE.md)**.

---

## 📚 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Guide de démarrage rapide (10 min)
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Justifications techniques complètes
- **[LIVRABLE.md](LIVRABLE.md)** - Document de livraison académique
- **[INDEX.md](INDEX.md)** - Navigation et index du projet

---

## 💡 Commandes Utiles

### Logs des conteneurs
```bash
docker logs -f spark-master     # Logs Spark
docker logs -f kafka            # Logs Kafka
docker logs -f namenode         # Logs HDFS
```

### État du cluster
```bash
docker-compose ps               # État des conteneurs
docker stats                    # Usage CPU/RAM
docker exec namenode hdfs dfsadmin -report  # État HDFS
```

### Shell interactif
```bash
docker exec -it spark-master bash   # Shell Spark
docker exec -it namenode bash       # Shell Hadoop
docker exec -it mongodb mongo       # Shell MongoDB
```

---

## ✅ Checklist de Validation

Avant de considérer le projet comme fonctionnel:

- [ ] Tous les conteneurs sont en état "Up" (`docker-compose ps`)
- [ ] HDFS contient le fichier de logs (`hdfs dfs -ls /logs`)
- [ ] Les 3 analyses batch s'exécutent sans erreur
- [ ] Les résultats sont visibles dans MongoDB
- [ ] Les interfaces web sont accessibles
- [ ] Le streaming fonctionne (optionnel)

---

## 🎓 Objectifs Pédagogiques

En complétant ce projet, vous aurez maîtrisé:

✅ Architecture distribuée avec Docker  
✅ HDFS pour stockage distribué  
✅ Spark Batch (RDD, DataFrame)  
✅ Spark Structured Streaming  
✅ Kafka pour streaming de données  
✅ MongoDB pour NoSQL  
✅ Intégration complète de l'écosystème Big Data

---

## 📊 Tests et Documentation de Test

Le dossier contient également des guides de test pour l'application web:

- **GUIDE_TEST_ETAPES.md** - Guide de test étape par étape
- **RESUME_API.md** - Résumé des endpoints API
- **RESULTATS_TESTS.md** - Template pour résultats de tests

Ces fichiers documentent comment tester l'application web dont les logs sont analysés.

---

## 👨‍💻 Auteur

Projet réalisé dans le cadre du cours de Big Data et Data Engineering.

**Dépôt GitHub**: https://github.com/zakaria12906/pjk.git

---

## 📝 Licence

MIT License - Usage académique et éducatif.

---

**Bon courage ! 🚀**

*Pour un démarrage ultra-rapide, consultez [QUICKSTART.md](QUICKSTART.md)*
