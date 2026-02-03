# Guide de test – TP Big Data (étape par étape)

Ce document décrit comment **tester que l’architecture Big Data** (HDFS, Spark, Kafka, MongoDB) et les **analyses batch et streaming** fonctionnent correctement.

**Projet :** Analyse de logs web – Architecture distribuée (Docker, HDFS, Spark, Kafka, MongoDB).

---

## Prérequis

- [ ] **Docker** installé et démarré (`docker --version`, `docker ps`)
- [ ] **Docker Compose** installé (`docker-compose --version`)
- [ ] **Python 3** (pour le producteur Kafka : `pip install kafka-python`)
- [ ] Au moins **8 Go RAM** et **20 Go** disque libres
- [ ] Projet TP Big Data présent (dossier contenant `docker-compose.yml`, `spark-apps/`, `data/`)

---

## Étape 1 : Vérifier Docker et lancer les services

**Objectif :** S’assurer que tous les conteneurs démarrent sans erreur.

1. Ouvrir un terminal et aller dans le **dossier du projet TP Big Data** (celui qui contient `docker-compose.yml`).

2. Lancer les services :
   ```bash
   docker-compose up -d
   ```

3. Attendre 1 à 2 minutes, puis vérifier l’état :
   ```bash
   docker-compose ps
   ```

4. **Résultat attendu :** Tous les services en état **Up** :
   - `namenode`
   - `datanode`
   - `spark-master`
   - `spark-worker`
   - `zookeeper`
   - `kafka`
   - `mongodb`

**À noter dans RESULTATS_TESTS_TP_BIGDATA.md :** Liste des conteneurs, état (Up/Exit), erreurs éventuelles.

---

## Étape 2 : Vérifier HDFS (NameNode et DataNode)

**Objectif :** Confirmer que HDFS répond et que les répertoires existent.

1. Créer les répertoires HDFS :
   ```bash
   docker exec namenode hdfs dfs -mkdir -p /logs
   docker exec namenode hdfs dfs -mkdir -p /output
   ```

2. Vérifier que le fichier de logs existe dans `data/` :
   ```bash
   ls -la data/web_server.log
   ```
   Si le fichier n’existe pas, le créer ou le copier (format Apache Common Log).

3. Copier les logs dans HDFS :
   ```bash
   docker exec namenode hdfs dfs -put -f /data/web_server.log /logs/
   ```
   *(Si le volume `./data` est monté sur `/data` dans le conteneur. Sinon : `docker cp data/web_server.log namenode:/tmp/` puis `docker exec namenode hdfs dfs -put /tmp/web_server.log /logs/`.)*

4. Lister le contenu de `/logs` :
   ```bash
   docker exec namenode hdfs dfs -ls /logs
   ```

5. **Optionnel :** Ouvrir l’interface web HDFS : **http://localhost:9870**  
   Vérifier que le fichier `web_server.log` apparaît sous `/logs`.

**À noter :** Commande exécutée, sortie de `hdfs dfs -ls /logs`, erreurs éventuelles.

---

## Étape 3 : Tester l’analyse Batch (produits les plus consultés)

**Objectif :** Vérifier que Spark lit depuis HDFS, traite les logs et écrit dans MongoDB.

1. Exécuter le job Spark batch :
   ```bash
   docker exec spark-master spark-submit \
     --master spark://spark-master:7077 \
     --packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 \
     /spark-apps/batch_top_products.py
   ```

2. **Résultat attendu :**
   - Pas d’exception Python/Spark
   - Affichage du tableau « Top 10 Produits » dans la console
   - Message du type « Résultats sauvegardés » ou « Analyze terminée avec succès »

3. Vérifier les résultats dans MongoDB :
   ```bash
   docker exec -it mongodb mongo
   ```
   Dans le shell MongoDB :
   ```javascript
   use logs_analytics
   show collections
   db.top_products.find().pretty()
   exit
   ```

4. **Résultat attendu :** La collection `top_products` existe et contient des documents avec `product_id`, `views`, `analyzed_at`.

**À noter :** Code de sortie du `spark-submit`, extrait de la sortie console, nombre de documents dans `top_products`, erreurs éventuelles.

---

## Étape 4 : Vérifier les interfaces web (Spark, HDFS)

**Objectif :** S’assurer que les UIs sont accessibles.

1. **Spark Master**  
   - URL : **http://localhost:8080**  
   - Vérifier : page « Spark Master » avec workers connectés.

2. **Spark Worker**  
   - URL : **http://localhost:8081**  
   - Vérifier : page du worker avec ressources (mémoire, cœurs).

3. **HDFS NameNode**  
   - URL : **http://localhost:9870**  
   - Vérifier : « Overview », « Datanodes », et présence du fichier sous « Utilities » → « Browse the file system » → `/logs`.

**À noter :** Pour chaque URL : accessible (Oui/Non), message d’erreur éventuel.

---

## Étape 5 : Tester l’analyse Streaming (détection d’erreurs)

**Objectif :** Vérifier que Spark consomme les logs depuis Kafka et écrit les alertes dans MongoDB.

### 5.1 Démarrer le producteur Kafka

1. Dans un **premier terminal**, aller dans le dossier du projet (où se trouve `data/kafka_producer.py`).

2. Installer le client Kafka si besoin :
   ```bash
   pip3 install kafka-python
   ```

3. Lancer le producteur (il envoie des logs vers le topic `web-logs`) :
   ```bash
   python3 data/kafka_producer.py
   ```
   Laisser tourner ; des lignes de log s’affichent toutes les ~2 secondes.

### 5.2 Démarrer le job Spark Streaming

4. Dans un **second terminal** :
   ```bash
   docker exec spark-master spark-submit \
     --master spark://spark-master:7077 \
     --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0,org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 \
     /spark-apps/streaming_error_detection.py
   ```

5. **Résultat attendu :**
   - Connexion à Kafka OK
   - Messages « Streaming démarré » puis micro-batches affichés dans la console (format console Spark)
   - Pas d’exception liée à Kafka ou MongoDB

6. Laisser tourner 1 à 2 minutes (producteur + streaming), puis arrêter le producteur (**Ctrl+C** dans le terminal du producteur).

7. Vérifier les alertes dans MongoDB :
   ```bash
   docker exec -it mongodb mongo
   ```
   ```javascript
   use logs_analytics
   db.error_alerts.find().pretty()
   exit
   ```

8. **Résultat attendu :** La collection `error_alerts` existe ; elle peut contenir des documents avec `window_start`, `window_end`, `error_type`, `http_code`, `error_count`, `alert_level`, `message`, `detected_at`.

**À noter :** Connexion Kafka (OK/Erreur), sortie console du streaming, présence de documents dans `error_alerts`, erreurs éventuelles.

---

## Étape 6 : Vérifier la communication entre services

**Objectif :** Confirmer que chaque composant atteint les autres.

| De → Vers    | Test rapide |
|-------------|-------------|
| Spark → HDFS | Déjà validé si l’étape 3 (batch) a réussi (lecture depuis `hdfs://namenode:9000/logs/...`) |
| Spark → MongoDB | Déjà validé si les collections `top_products` et `error_alerts` ont des données |
| Spark → Kafka | Déjà validé si le streaming (étape 5) affiche des micro-batches |
| HDFS interne | `docker exec namenode hdfs dfsadmin -report` doit montrer au moins 1 DataNode actif |

**À noter :** Pour chaque paire : OK / Erreur (avec message si possible).

---

## Étape 7 : Arrêt propre et récapitulatif

1. Arrêter le job Spark Streaming (**Ctrl+C** dans le terminal où il tourne).
2. Arrêter les conteneurs :
   ```bash
   docker-compose down
   ```

3. Remplir la **checklist finale** dans **RESULTATS_TESTS_TP_BIGDATA.md**.

---

## Checklist finale (TP Big Data)

- [ ] Tous les conteneurs Docker sont en état **Up** (étape 1)
- [ ] HDFS contient le fichier de logs sous `/logs` (étape 2)
- [ ] L’analyse **batch** (top produits) s’exécute sans erreur et écrit dans MongoDB (étape 3)
- [ ] Les interfaces web Spark (8080, 8081) et HDFS (9870) sont accessibles (étape 4)
- [ ] Le **producteur Kafka** envoie des logs (étape 5.1)
- [ ] L’analyse **streaming** (détection d’erreurs) consomme Kafka et écrit dans MongoDB (étape 5.2)
- [ ] Les collections `top_products` et `error_alerts` existent et contiennent des données (étapes 3 et 5)
- [ ] Communication entre services vérifiée (étape 6)
- [ ] Résultats reportés dans **RESULTATS_TESTS_TP_BIGDATA.md**

Si toutes les cases sont cochées et qu’il n’y a pas d’erreur bloquante, l’architecture et les deux analyses (batch + streaming) peuvent être considérées comme fonctionnelles.

---

## Enregistrement des réponses et push GitHub

Après avoir suivi les étapes et rempli **RESULTATS_TESTS_TP_BIGDATA.md** :

1. Dans le dossier du dépôt **pjk** (celui qui contient ce guide) :
   ```bash
   git add .
   git status
   git commit -m "Tests TP Big Data - résultats du [DATE]"
   git push origin main
   ```

2. Vérifier sur **https://github.com/zakaria12906/pjk** que les fichiers suivants sont bien présents :
   - `GUIDE_TEST_ETAPES_TP_BIGDATA.md`
   - `RESULTATS_TESTS_TP_BIGDATA.md`
   - `README.md` (mis à jour avec la section TP Big Data)

Voir aussi **README.md** et la section « Clone et mise à jour du dépôt ».
