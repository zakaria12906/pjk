# 🧪 GUIDE DE TEST - Étape par Étape

## Prérequis

Avant de commencer, assurez-vous d'avoir:
- Docker installé (version ≥ 20.10)
- Docker Compose installé (version ≥ 2.0)
- Au moins 8GB de RAM disponible
- Ports libres: 9870, 9000, 8080, 8081, 9092, 27017

---

## 📋 ÉTAPE 1 - Vérifier les Prérequis

```bash
# Vérifier Docker
docker --version
# Attendu: Docker version 20.10.x ou supérieur

# Vérifier Docker Compose
docker-compose --version
# Attendu: Docker Compose version 2.x.x ou supérieur

# Vérifier l'espace disque
df -h
# Attendu: Au moins 10GB disponible

# Aller dans le répertoire du projet
cd /Users/zakariaeelouazzani/Desktop/Projet_charazad
```

**✅ Résultat attendu**: Toutes les commandes s'exécutent sans erreur

---

## 📋 ÉTAPE 2 - Démarrer l'Architecture Big Data

```bash
# Démarrer tous les services en arrière-plan
docker-compose up -d

# Attendre que tous les services démarrent (environ 2 minutes)
echo "⏳ Attente du démarrage des services (2 minutes)..."
sleep 120
```

**✅ Résultat attendu**: 
```
Creating network "projet_charazad_default" with the default driver
Creating namenode   ... done
Creating datanode   ... done
Creating zookeeper  ... done
Creating spark-master ... done
Creating spark-worker ... done
Creating kafka      ... done
Creating mongodb    ... done
```

---

## 📋 ÉTAPE 3 - Vérifier l'État des Services

```bash
# Voir tous les conteneurs en cours d'exécution
docker-compose ps
```

**✅ Résultat attendu**: Tous les services affichent "Up"

```
NAME                COMMAND                  SERVICE             STATUS
datanode           "/entrypoint.sh /run…"   datanode            Up
kafka              "/etc/confluent/dock…"   kafka               Up
mongodb            "docker-entrypoint.s…"   mongodb             Up
namenode           "/entrypoint.sh /run…"   namenode            Up
spark-master       "/opt/bitnami/script…"   spark-master        Up
spark-worker       "/opt/bitnami/script…"   spark-worker        Up
zookeeper          "/etc/confluent/dock…"   zookeeper           Up
```

### Vérifier les logs de chaque service

```bash
# Vérifier HDFS NameNode
docker logs namenode | tail -20

# Vérifier Spark Master
docker logs spark-master | tail -20

# Vérifier Kafka
docker logs kafka | tail -20

# Vérifier MongoDB
docker logs mongodb | tail -20
```

**✅ Résultat attendu**: Aucun message d'erreur critique

---

## 📋 ÉTAPE 4 - Vérifier les Interfaces Web

Ouvrez votre navigateur et accédez aux URLs suivantes:

### 4.1 HDFS NameNode
**URL**: http://localhost:9870

**✅ Résultat attendu**:
- Page "Overview" d'HDFS
- Section "Summary" montrant:
  - Configured Capacity: > 0 GB
  - DFS Used: quelques MB
  - Live Nodes: 1

### 4.2 Spark Master
**URL**: http://localhost:8080

**✅ Résultat attendu**:
- Page "Spark Master"
- Section "Workers": 1 worker actif
- Status: ALIVE
- Cores: 2 ou plus
- Memory: plusieurs GB

### 4.3 Spark Worker
**URL**: http://localhost:8081

**✅ Résultat attendu**:
- Page "Spark Worker"
- Status: ALIVE
- Master URL: spark://spark-master:7077

---

## 📋 ÉTAPE 5 - Préparer HDFS

```bash
# Se connecter au conteneur NameNode
docker exec -it namenode bash

# Créer le répertoire pour les logs
hdfs dfs -mkdir -p /logs

# Donner les permissions
hdfs dfs -chmod -R 777 /logs

# Copier le fichier de logs dans HDFS
hdfs dfs -put /data/web_server.log /logs/

# Vérifier que le fichier est présent
hdfs dfs -ls /logs

# Afficher les premières lignes du fichier
hdfs dfs -cat /logs/web_server.log | head -10

# Quitter le conteneur
exit
```

**✅ Résultat attendu**:
```
Found 1 items
-rw-r--r--   3 root supergroup      XXXX 2025-02-03 21:00 /logs/web_server.log
```

Vous devriez voir les 10 premières lignes des logs affichées.

---

## 📋 ÉTAPE 6 - Test de l'Analyse BATCH (Top 10 Produits)

### 6.1 Lancer l'analyse

```bash
# Exécuter l'analyse batch
docker exec spark-master spark-submit \
  --master spark://spark-master:7077 \
  --packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 \
  /spark-apps/batch/top_products.py
```

**✅ Résultat attendu**:
- Le job Spark démarre
- Affichage des logs de traitement
- Message final: "Job terminé avec succès" ou similaire
- Durée: environ 30-60 secondes

**📊 Surveillez**:
- http://localhost:8080 → Section "Running Applications"
- Vous devriez voir votre application en cours

### 6.2 Vérifier les résultats dans MongoDB

```bash
# Se connecter à MongoDB
docker exec -it mongodb mongo

# Utiliser la base de données
use logs_analytics

# Afficher les collections
show collections

# Afficher les résultats
db.top_products.find().pretty()
```

**✅ Résultat attendu**:
```json
{
    "_id" : ObjectId("..."),
    "product_id" : "105",
    "product_category" : "lipstick",
    "request_count" : 12,
    "analysis_date" : "2025-02-03",
    "data_source" : "hdfs:///logs/web_server.log"
}
```

Vous devriez voir **10 produits** classés par nombre de requêtes (décroissant).

### 6.3 Compter les résultats

```bash
# Dans MongoDB (toujours connecté)
db.top_products.count()
```

**✅ Résultat attendu**: `10` (exactement 10 produits)

```bash
# Quitter MongoDB
exit
```

---

## 📋 ÉTAPE 7 - Test de l'Analyse STREAMING (Détection d'Erreurs)

Cette étape nécessite **3 terminaux** en parallèle.

### 7.1 Terminal 1 - Démarrer le Producteur Kafka

```bash
# Terminal 1
cd /Users/zakariaeelouazzani/Desktop/Projet_charazad

# Se connecter au conteneur Kafka
docker exec -it kafka bash

# Aller dans le répertoire des applications Kafka
cd /kafka-apps

# Installer les dépendances Python
pip3 install -r requirements.txt

# Lancer le producteur
python3 log_producer.py
```

**Menu du producteur**:
```
=== Simulateur de Logs Web ===
1. NORMAL - Trafic normal
2. ERRORS - Pic d'erreurs (500/404)
3. TRENDING - Produit en tendance
4. Quitter

Choix:
```

**👉 Choisissez**: `2` (ERRORS)

**Durée d'envoi en secondes**: `300` (5 minutes)

**✅ Résultat attendu**:
```
🚀 Démarrage du mode ERRORS
⏱️  Durée: 300 secondes
📊 Envoi de logs avec erreurs...

✅ Log envoyé (1/300): 192.168.x.x - 500
✅ Log envoyé (2/300): 192.168.x.x - 404
...
```

**⚠️ Laissez ce terminal ouvert et actif**

---

### 7.2 Terminal 2 - Démarrer Spark Streaming

```bash
# Terminal 2
cd /Users/zakariaeelouazzani/Desktop/Projet_charazad

# Lancer l'analyse streaming
docker exec spark-master spark-submit \
  --master spark://spark-master:7077 \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0,org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 \
  /spark-apps/streaming/error_detection.py
```

**✅ Résultat attendu**:
```
Starting Spark Streaming Job...
Consuming from Kafka topic: web-logs
Window duration: 5 minutes
...
Batch: 0
-------------------------------------------
Batch: 1
-------------------------------------------
+---+-------+
|code|count |
+---+-------+
|500 |15    |
|404 |42    |
+---+-------+
```

**⚠️ Laissez ce terminal ouvert et actif**

---

### 7.3 Terminal 3 - Surveiller les Alertes MongoDB

```bash
# Terminal 3
cd /Users/zakariaeelouazzani/Desktop/Projet_charazad

# Se connecter à MongoDB
docker exec -it mongodb mongo

# Utiliser la base de données
use logs_analytics

# Surveiller les nouvelles alertes (rafraîchir toutes les 10 secondes)
while true; do
  clear
  echo "=== ALERTES D'ERREURS (rafraîchi toutes les 10s) ==="
  echo ""
  db.error_alerts.find().sort({detected_at: -1}).limit(5).pretty()
  sleep 10
done
```

**✅ Résultat attendu**:

Après **5-6 minutes**, vous devriez voir des alertes apparaître:

```json
{
    "_id" : ObjectId("..."),
    "alert_type" : "HIGH_500_ERRORS",
    "error_code" : 500,
    "error_count" : 15,
    "threshold" : 10,
    "window_start" : ISODate("2025-02-03T21:00:00Z"),
    "window_end" : ISODate("2025-02-03T21:05:00Z"),
    "detected_at" : ISODate("2025-02-03T21:05:30Z"),
    "severity" : "CRITICAL"
}
{
    "_id" : ObjectId("..."),
    "alert_type" : "HIGH_404_ERRORS",
    "error_code" : 404,
    "error_count" : 42,
    "threshold" : 30,
    "window_start" : ISODate("2025-02-03T21:00:00Z"),
    "window_end" : ISODate("2025-02-03T21:05:00Z"),
    "detected_at" : ISODate("2025-02-03T21:05:30Z"),
    "severity" : "WARNING"
}
```

**📊 Vérifications**:
- `error_code`: 404 ou 500
- `error_count` > `threshold`
- `alert_type`: HIGH_500_ERRORS ou HIGH_404_ERRORS

---

### 7.4 Arrêter les processus de streaming

**Terminal 1** (Producteur Kafka):
- Attendez que les 300 secondes soient écoulées OU
- Appuyez sur `Ctrl+C` puis `exit`

**Terminal 2** (Spark Streaming):
- Appuyez sur `Ctrl+C` (peut prendre 10-20 secondes)

**Terminal 3** (MongoDB):
- Appuyez sur `Ctrl+C`
- Tapez `exit`

---

## 📋 ÉTAPE 8 - Vérifier les Résultats Finaux

### 8.1 Vérifier MongoDB

```bash
# Se connecter à MongoDB
docker exec -it mongodb mongo

# Utiliser la base de données
use logs_analytics

# Lister toutes les collections
show collections
```

**✅ Résultat attendu**:
```
error_alerts
top_products
```

### 8.2 Statistiques Batch

```bash
# Dans MongoDB (toujours connecté)

# Nombre total de produits analysés
db.top_products.count()
# Attendu: 10

# Top 3 produits
db.top_products.find().sort({request_count: -1}).limit(3).pretty()
```

### 8.3 Statistiques Streaming

```bash
# Nombre total d'alertes
db.error_alerts.count()
# Attendu: ≥ 1 (dépend de la durée du test)

# Alertes par type
db.error_alerts.aggregate([
  { $group: { _id: "$alert_type", count: { $sum: 1 } } }
])

# Alertes critiques (500)
db.error_alerts.find({ error_code: 500 }).count()

# Alertes warning (404)
db.error_alerts.find({ error_code: 404 }).count()

# Quitter MongoDB
exit
```

---

## 📋 ÉTAPE 9 - Vérifier les Logs Spark

```bash
# Logs du dernier job batch
docker logs spark-master | grep "top_products"

# Logs du job streaming
docker logs spark-master | grep "error_detection"

# Voir toutes les applications Spark
docker exec spark-master curl -s http://localhost:8080/json/ | grep -o '"id":"[^"]*"' | head -5
```

---

## 📋 ÉTAPE 10 - Tests de Robustesse (Optionnel)

### 10.1 Test: Vérifier la tolérance aux pannes

```bash
# Arrêter le DataNode
docker stop datanode

# Vérifier HDFS (devrait encore fonctionner en mode dégradé)
docker exec namenode hdfs dfs -ls /logs

# Redémarrer le DataNode
docker start datanode
```

### 10.2 Test: Vérifier Kafka

```bash
# Lister les topics Kafka
docker exec kafka kafka-topics --list --bootstrap-server localhost:9092

# Décrire le topic web-logs
docker exec kafka kafka-topics --describe --topic web-logs --bootstrap-server localhost:9092
```

**✅ Résultat attendu**:
```
Topic: web-logs
PartitionCount: 1
ReplicationFactor: 1
```

### 10.3 Test: Consommer un message Kafka manuellement

```bash
# Lire les derniers messages du topic
docker exec kafka kafka-console-consumer \
  --bootstrap-server localhost:9092 \
  --topic web-logs \
  --from-beginning \
  --max-messages 5
```

**✅ Résultat attendu**: 5 lignes de logs au format standard

---

## 📋 ÉTAPE 11 - Nettoyage et Arrêt

### 11.1 Arrêt propre

```bash
cd /Users/zakariaeelouazzani/Desktop/Projet_charazad

# Arrêter tous les services
docker-compose down
```

**✅ Résultat attendu**:
```
Stopping mongodb      ... done
Stopping kafka        ... done
Stopping spark-worker ... done
Stopping spark-master ... done
Stopping zookeeper    ... done
Stopping datanode     ... done
Stopping namenode     ... done
Removing mongodb      ... done
Removing kafka        ... done
...
```

### 11.2 Nettoyage complet (si besoin)

```bash
# Supprimer aussi les volumes (⚠️ SUPPRIME LES DONNÉES)
docker-compose down -v

# Supprimer les images non utilisées
docker system prune -f
```

---

## 📊 CHECKLIST DE VALIDATION FINALE

Cochez chaque test réussi:

### Infrastructure
- [ ] Docker et Docker Compose installés
- [ ] 7 conteneurs démarrés avec succès
- [ ] HDFS accessible (http://localhost:9870)
- [ ] Spark Master accessible (http://localhost:8080)
- [ ] HDFS contient le fichier `/logs/web_server.log`

### Analyse Batch
- [ ] Job Spark batch exécuté sans erreur
- [ ] 10 produits présents dans MongoDB (`top_products`)
- [ ] Produits triés par `request_count` décroissant
- [ ] Chaque document contient: product_id, product_category, request_count

### Analyse Streaming
- [ ] Producteur Kafka envoie des logs
- [ ] Job Spark Streaming consomme depuis Kafka
- [ ] Alertes générées dans MongoDB (`error_alerts`)
- [ ] Alertes contiennent: alert_type, error_code, error_count, threshold
- [ ] Alertes 500 (CRITICAL) et 404 (WARNING) présentes

### Performance
- [ ] Job batch terminé en < 2 minutes
- [ ] Job streaming traite les logs en temps réel (latence < 10s)
- [ ] Aucune erreur critique dans les logs Docker

---

## 🐛 DÉPANNAGE

### Problème: Port déjà utilisé

```bash
# Trouver le processus utilisant le port 9870
lsof -i :9870

# Tuer le processus
kill -9 <PID>
```

### Problème: HDFS en safe mode

```bash
docker exec namenode hdfs dfsadmin -safemode leave
```

### Problème: Spark ne trouve pas le fichier HDFS

```bash
# Vérifier la connexion HDFS depuis Spark
docker exec spark-master curl http://namenode:9870/jmx?qry=Hadoop:service=NameNode,name=NameNodeStatus
```

### Problème: Kafka ne démarre pas

```bash
# Vérifier Zookeeper d'abord
docker logs zookeeper | tail -50

# Redémarrer Kafka
docker restart kafka
```

### Problème: MongoDB n'a pas de données

```bash
# Vérifier que MongoDB est accessible depuis Spark
docker exec spark-master nc -zv mongodb 27017
```

---

## 📈 RÉSULTATS ATTENDUS - RÉSUMÉ

| Test | Métrique | Valeur Attendue | Statut |
|------|----------|-----------------|--------|
| Services Docker | Conteneurs actifs | 7 | ⬜ |
| HDFS | Fichiers stockés | 1 (`web_server.log`) | ⬜ |
| Batch | Produits dans MongoDB | 10 | ⬜ |
| Batch | Durée exécution | < 2 min | ⬜ |
| Streaming | Alertes générées | ≥ 1 | ⬜ |
| Streaming | Latence traitement | < 10s | ⬜ |
| MongoDB | Collections créées | 2 | ⬜ |

---

## ✅ CONCLUSION

Si tous les tests passent, votre projet Big Data fonctionne parfaitement ! 🎉

**Prochaines étapes**:
1. Documentez vos résultats de test dans `RESULTATS_TESTS.md`
2. Prenez des captures d'écran des interfaces web
3. Exportez les données MongoDB pour le rapport

---

**Document créé le**: 3 Février 2026  
**Projet**: TP Avancé - Analyse de Logs Web  
**Durée totale des tests**: ~30-45 minutes
