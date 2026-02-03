# 🚀 COMMANDES DE TEST - VERSION CORRIGÉE

## ⚠️ PROBLÈME RÉSOLU

Les images Spark avec versions spécifiques n'existent pas.
**Solution**: Utilisation de `bitnami/spark:latest`

---

## ✅ ÉTAPES COMPLÈTES

### ÉTAPE 1 - Mise à jour et nettoyage

```bash
cd /Users/zakariaeelouazzani/Desktop/Projet_charazad

# Récupérer la version corrigée
git pull origin main

# Nettoyer les tentatives précédentes
docker-compose down -v
docker system prune -f
```

---

### ÉTAPE 2 - Démarrer les services

```bash
# Démarrer tous les services (téléchargement ~5-10 min la 1ère fois)
docker-compose up -d
```

**⏳ Attendez que toutes les images soient téléchargées...**

---

### ÉTAPE 3 - Attendre le démarrage complet

```bash
# Attendre 2 minutes
echo "⏳ Attente 2 minutes..."
sleep 120
```

---

### ÉTAPE 4 - Vérifier l'état

```bash
docker-compose ps
```

**Résultat attendu**: Tous affichent "Up" ou "running"

---

### ÉTAPE 5 - Vérifier les interfaces web

Ouvrir dans le navigateur:
- HDFS: http://localhost:9870
- Spark Master: http://localhost:8080
- Spark Worker: http://localhost:8081

---

### ÉTAPE 6 - Préparer HDFS

```bash
# Créer le répertoire
docker exec namenode hdfs dfs -mkdir -p /logs
docker exec namenode hdfs dfs -chmod -R 777 /logs

# Copier les logs
docker exec namenode hdfs dfs -put /data/web_server.log /logs/

# Vérifier
docker exec namenode hdfs dfs -ls /logs
docker exec namenode hdfs dfs -cat /logs/web_server.log | head -10
```

---

### ÉTAPE 7 - Test BATCH

```bash
docker exec spark-master spark-submit \
  --master spark://spark-master:7077 \
  --packages org.mongodb.spark:mongo-spark-connector_2.12:10.0.5 \
  /spark-apps/batch/top_products.py
```

**Vérifier les résultats**:
```bash
docker exec -it mongodb mongosh
```

Dans mongosh:
```javascript
use logs_analytics
db.top_products.find()
db.top_products.countDocuments()
exit
```

---

### ÉTAPE 8 - Test STREAMING

**Terminal 1 - Producteur**:
```bash
docker exec -it kafka bash
cd /kafka-apps
pip3 install -r requirements.txt
python3 log_producer.py
# Choisir: 2 (ERRORS)
# Durée: 300
```

**Terminal 2 - Spark Streaming**:
```bash
docker exec spark-master spark-submit \
  --master spark://spark-master:7077 \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.mongodb.spark:mongo-spark-connector_2.12:10.0.5 \
  /spark-apps/streaming/error_detection.py
```

**Terminal 3 - Résultats** (après 5-6 minutes):
```bash
docker exec -it mongodb mongosh
use logs_analytics
db.error_alerts.find().sort({detected_at: -1}).limit(5)
exit
```

---

### ÉTAPE 9 - Arrêter

```bash
docker-compose down
```

---

## 🐛 SI PROBLÈME

### Voir les logs
```bash
docker-compose logs -f
```

### Redémarrer un service
```bash
docker-compose restart spark-master
```

### Tout nettoyer et recommencer
```bash
docker-compose down -v
docker system prune -af
docker-compose up -d
```
