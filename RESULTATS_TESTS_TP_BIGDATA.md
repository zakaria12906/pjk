# Résultats des tests – TP Big Data

À remplir lors de l’exécution du guide **GUIDE_TEST_ETAPES_TP_BIGDATA.md**.  
**Date des tests :** _______________  
**Environnement :** _______________ (ex. macOS, Docker Desktop, 16 Go RAM)

---

## Étape 1 – Services Docker

| Conteneur     | État attendu | État obtenu | Remarque |
|---------------|--------------|-------------|----------|
| namenode      | Up           |             |          |
| datanode      | Up           |             |          |
| spark-master  | Up           |             |          |
| spark-worker  | Up           |             |          |
| zookeeper     | Up           |             |          |
| kafka         | Up           |             |          |
| mongodb       | Up           |             |          |

**Sortie de `docker-compose ps` (coller ou résumer) :**
```
(à remplir)
```

**Erreurs éventuelles :**
```
(à remplir)
```

---

## Étape 2 – HDFS

| Vérification              | Résultat | Remarque |
|---------------------------|----------|----------|
| Création /logs et /output | OK / KO  |          |
| Upload web_server.log     | OK / KO  |          |
| `hdfs dfs -ls /logs`     |          |          |

**Sortie de `hdfs dfs -ls /logs` :**
```
(à remplir)
```

**Interface web HDFS (http://localhost:9870) :** Accessible Oui / Non

---

## Étape 3 – Analyse Batch (Top Produits)

| Vérification                    | Résultat | Remarque |
|---------------------------------|----------|----------|
| spark-submit batch_top_products | OK / KO  |          |
| Pas d’exception Spark           | Oui / Non|          |
| Collection top_products créée   | Oui / Non|          |
| Documents avec product_id, views| Oui / Non|          |

**Code de sortie du spark-submit :** _______________

**Extrait de la sortie console (Top 10) :**
```
(à remplir)
```

**Extrait de `db.top_products.find().pretty()` :**
```javascript
(à remplir)
```

**Nombre de documents dans top_products :** _______________

**Erreurs éventuelles :**
```
(à remplir)
```

---

## Étape 4 – Interfaces web

| URL                        | Accessible | Remarque |
|----------------------------|------------|----------|
| http://localhost:8080 (Spark Master) | Oui / Non |          |
| http://localhost:8081 (Spark Worker)| Oui / Non |          |
| http://localhost:9870 (HDFS)        | Oui / Non |          |

---

## Étape 5 – Analyse Streaming (Détection d’erreurs)

### 5.1 Producteur Kafka

| Vérification           | Résultat | Remarque |
|-------------------------|----------|----------|
| python3 kafka_producer.py | OK / KO |          |
| Logs envoyés visibles   | Oui / Non|          |

**Erreur de connexion Kafka (si oui, message) :** _______________

### 5.2 Job Spark Streaming

| Vérification                | Résultat | Remarque |
|-----------------------------|----------|----------|
| spark-submit streaming_error_detection | OK / KO |          |
| Connexion Kafka             | OK / KO  |          |
| Micro-batches affichés      | Oui / Non|          |
| Collection error_alerts     | Oui / Non|          |

**Extrait de la sortie console (streaming) :**
```
(à remplir)
```

**Extrait de `db.error_alerts.find().pretty()` :**
```javascript
(à remplir)
```

**Nombre de documents dans error_alerts :** _______________

**Erreurs éventuelles :**
```
(à remplir)
```

---

## Étape 6 – Communication entre services

| De        → Vers   | Statut | Remarque |
|--------------------|--------|----------|
| Spark    → HDFS    | OK / KO|          |
| Spark    → MongoDB | OK / KO|          |
| Spark    → Kafka   | OK / KO|          |
| HDFS (DataNode)    | OK / KO|          |

**Sortie de `hdfs dfsadmin -report` (résumé) :**
```
(à remplir si pertinent)
```

---

## Checklist finale

- [ ] Tous les conteneurs sont Up
- [ ] HDFS contient web_server.log sous /logs
- [ ] Analyse batch exécutée avec succès, résultats dans MongoDB
- [ ] Interfaces web Spark et HDFS accessibles
- [ ] Producteur Kafka envoie des logs
- [ ] Analyse streaming consomme Kafka et écrit dans MongoDB
- [ ] top_products et error_alerts contiennent des données
- [ ] Communication entre services vérifiée

---

## Conclusion

- **Tous les tests critiques passent :** Oui / Non  
- **Problèmes restants :** _______________  
- **Commentaire libre :** _______________

---

## Enregistrement sur GitHub

- [ ] Fichiers ajoutés : `git add .`
- [ ] Commit : `git commit -m "Tests TP Big Data - résultats du [DATE]"`
- [ ] Push : `git push origin main`
- [ ] Vérification sur https://github.com/zakaria12906/pjk
