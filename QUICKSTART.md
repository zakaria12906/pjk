# ⚡ Guide de Démarrage Rapide

Ce guide vous permet de lancer le projet en **moins de 10 minutes**.

---

## 📋 Prérequis

Vérifiez que vous avez:
- ✅ Docker >= 20.10
- ✅ Docker Compose >= 2.0
- ✅ 8GB RAM disponible
- ✅ 20GB espace disque
- ✅ Python 3.7+

---

## 🚀 Installation en 5 Étapes

### Étape 1: Configuration initiale (2 min)

```bash
cd bigdata-logs-analysis
chmod +x scripts/*.sh
./scripts/setup.sh
```

**Ce script va:**
- ✓ Vérifier Docker et Docker Compose
- ✓ Créer les répertoires nécessaires
- ✓ Générer 10,000 lignes de logs d'exemple

---

### Étape 2: Démarrage des services (3 min)

```bash
docker-compose up -d
```

**Attendre que tous les services démarrent (~2 minutes):**

```bash
# Vérifier l'état
docker-compose ps
```

**Vous devriez voir 7 conteneurs actifs:**
- ✓ namenode (HDFS)
- ✓ datanode (HDFS)
- ✓ spark-master
- ✓ spark-worker
- ✓ zookeeper
- ✓ kafka
- ✓ mongodb

---

### Étape 3: Préparation HDFS (1 min)

```bash
./scripts/prepare_hdfs.sh
```

**Ce script va:**
- ✓ Créer les répertoires HDFS
- ✓ Uploader les logs dans HDFS
- ✓ Vérifier l'upload

**Interface Web HDFS:** http://localhost:9870

---

### Étape 4: Lancer les analyses batch (2 min)

```bash
./scripts/run_batch.sh
```

**Ce script lance séquentiellement:**
1. ✓ Top 10 Produits (~30s)
2. ✓ Répartition des Codes HTTP (~30s)
3. ✓ Top 10 IPs Actives (~30s)

**Interface Web Spark:** http://localhost:8080

---

### Étape 5: Consulter les résultats (1 min)

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

## 🎉 Félicitations !

Vous avez maintenant une architecture Big Data distribuée fonctionnelle !

---

## 📊 Interfaces Web Disponibles

| Service | URL | Description |
|---------|-----|-------------|
| HDFS NameNode | http://localhost:9870 | Browse HDFS files |
| HDFS DataNode | http://localhost:9864 | DataNode status |
| Spark Master | http://localhost:8080 | Cluster overview |
| Spark Worker | http://localhost:8081 | Worker status |

---

## ⚡ Tester le Streaming (Optionnel)

### Terminal 1: Démarrer le producteur Kafka

```bash
docker exec -it kafka bash
cd /kafka-apps
python3 log_producer.py

# Dans le menu:
# 1. Choisir "2" pour mode ERRORS (pic d'erreurs)
# 2. Durée: 300 secondes (5 minutes)
```

### Terminal 2: Démarrer la détection d'erreurs

```bash
docker exec -it spark-master bash

spark-submit \
  --master spark://spark-master:7077 \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0,org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 \
  /spark-apps/streaming/error_detection.py
```

### Terminal 3: Voir les alertes en temps réel

```bash
docker exec -it mongodb mongo

use logs_analytics
# Rafraîchir toutes les 5 secondes
while true; do
  db.error_alerts.find().sort({detected_at: -1}).limit(5).pretty()
  sleep 5
done
```

---

## 🛑 Arrêter les Services

```bash
# Arrêt propre
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

## 🐛 Dépannage Rapide

### Erreur: "Cannot connect to Docker daemon"
```bash
# Démarrer Docker Desktop (Mac/Windows)
# OU sur Linux:
sudo systemctl start docker
```

### Erreur: "Port already in use"
```bash
# Trouver le processus utilisant le port (exemple: 9870)
lsof -i :9870
kill -9 <PID>

# OU changer les ports dans docker-compose.yml
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

## 📚 Aller Plus Loin

- **Architecture détaillée**: Voir [ARCHITECTURE.md](ARCHITECTURE.md)
- **Documentation complète**: Voir [README.md](README.md)
- **Justifications techniques**: Voir section "Méthode de Raisonnement" dans ARCHITECTURE.md

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

Avant de rendre le projet, vérifiez:

- [ ] Tous les conteneurs sont en état "Up"
- [ ] Les 3 analyses batch s'exécutent sans erreur
- [ ] Les résultats sont visibles dans MongoDB
- [ ] HDFS contient le fichier de logs
- [ ] Les interfaces web sont accessibles
- [ ] Le streaming fonctionne (optionnel)

---

## 🎓 Objectifs Pédagogiques Atteints

En complétant ce quickstart, vous avez:

✅ Déployé une architecture distribuée avec Docker  
✅ Configuré HDFS pour le stockage distribué  
✅ Exécuté des jobs Spark Batch  
✅ Testé Spark Structured Streaming (optionnel)  
✅ Intégré MongoDB pour les résultats  
✅ Compris le flux de données batch et streaming  

---

**Temps total: 10 minutes ⏱️**

Bon courage ! 🚀
