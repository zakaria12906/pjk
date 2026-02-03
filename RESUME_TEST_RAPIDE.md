# 🚀 RÉSUMÉ RAPIDE - Comment Tester le Projet

## ⚡ Version Express (10 minutes)

Si vous voulez tester rapidement, suivez ces commandes:

### 1️⃣ Démarrer (2 min)

```bash
cd /Users/zakariaeelouazzani/Desktop/Projet_charazad
docker-compose up -d
sleep 120  # Attendre 2 minutes
```

### 2️⃣ Préparer HDFS (1 min)

```bash
docker exec namenode hdfs dfs -mkdir -p /logs
docker exec namenode hdfs dfs -chmod -R 777 /logs
docker exec namenode hdfs dfs -put /data/web_server.log /logs/
docker exec namenode hdfs dfs -ls /logs
```

### 3️⃣ Test BATCH (2 min)

```bash
docker exec spark-master spark-submit \
  --master spark://spark-master:7077 \
  --packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 \
  /spark-apps/batch/top_products.py
```

**Voir résultats**:
```bash
docker exec -it mongodb mongo
> use logs_analytics
> db.top_products.find().pretty()
> exit
```

### 4️⃣ Test STREAMING (5 min)

**Terminal 1** - Producteur:
```bash
docker exec -it kafka bash
cd /kafka-apps
pip3 install -r requirements.txt
python3 log_producer.py
# Choisir: 2 (ERRORS)
# Durée: 300
```

**Terminal 2** - Spark Streaming:
```bash
docker exec spark-master spark-submit \
  --master spark://spark-master:7077 \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0,org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 \
  /spark-apps/streaming/error_detection.py
```

**Après 5-6 minutes**, vérifier les alertes:
```bash
docker exec -it mongodb mongo
> use logs_analytics
> db.error_alerts.find().pretty()
> exit
```

### 5️⃣ Arrêter

```bash
docker-compose down
```

---

## 📊 Interfaces Web à Vérifier

Pendant que les services tournent, ouvrez:

- **HDFS**: http://localhost:9870
- **Spark Master**: http://localhost:8080
- **Spark Worker**: http://localhost:8081

---

## ✅ Résultats Attendus

### Batch (MongoDB - `top_products`)
```json
{
  "product_id": "105",
  "product_category": "lipstick",
  "request_count": 12
}
```
→ **10 produits** au total

### Streaming (MongoDB - `error_alerts`)
```json
{
  "alert_type": "HIGH_500_ERRORS",
  "error_code": 500,
  "error_count": 15,
  "threshold": 10,
  "severity": "CRITICAL"
}
```
→ **Au moins 1 alerte** générée

---

## 📖 Guide Complet

Pour un guide détaillé avec toutes les vérifications, consultez: **`GUIDE_TEST.md`**

Il contient:
- ✅ 11 étapes détaillées
- ✅ Résultats attendus pour chaque commande
- ✅ Tests de robustesse
- ✅ Section dépannage
- ✅ Checklist de validation

**Durée totale du guide complet**: 30-45 minutes

---

## 🐛 Problèmes Fréquents

### Port déjà utilisé
```bash
lsof -i :9870
kill -9 <PID>
```

### HDFS en safe mode
```bash
docker exec namenode hdfs dfsadmin -safemode leave
```

### Voir les logs d'un service
```bash
docker logs -f spark-master
docker logs -f kafka
docker logs -f mongodb
```

---

**Bon test ! 🎉**
