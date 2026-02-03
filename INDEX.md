# 📚 INDEX DU PROJET - Navigation Rapide

## 🎯 Par Où Commencer ?

### 🚀 Vous voulez démarrer rapidement ?
👉 **[QUICKSTART.md](QUICKSTART.md)** - Démarrage en 10 minutes

### 📖 Vous voulez comprendre l'architecture ?
👉 **[ARCHITECTURE.md](ARCHITECTURE.md)** - Justifications techniques complètes

### 📋 Vous voulez la documentation complète ?
👉 **[README.md](README.md)** - Guide complet du projet

### 📦 Vous préparez le rendu ?
👉 **[LIVRABLE.md](LIVRABLE.md)** - Document de livraison académique

---

## 📁 Structure du Projet

```
bigdata-logs-analysis/
│
├── 📄 README.md                    # Documentation principale
├── 📄 ARCHITECTURE.md              # Justifications techniques
├── 📄 QUICKSTART.md                # Guide démarrage rapide
├── 📄 LIVRABLE.md                  # Document de rendu
├── 📄 INDEX.md                     # Ce fichier
│
├── 🐳 docker-compose.yml           # Orchestration des services
├── 📝 .gitignore                   # Fichiers à ignorer
│
├── 📂 data/                        # Données
│   ├── generate_logs.py           # Générateur de logs
│   └── web_server.log             # Logs générés (10k lignes)
│
├── 📂 spark/                       # Applications Spark
│   ├── requirements.txt           # Dépendances Python
│   │
│   ├── 📂 batch/                  # Analyses Batch
│   │   ├── top_products.py        # Analyse #1: Top produits
│   │   ├── http_codes.py          # Analyse #2: Codes HTTP
│   │   └── top_ips.py             # Analyse #3: Top IPs
│   │
│   └── 📂 streaming/              # Analyses Streaming
│       ├── error_detection.py     # Streaming #1: Erreurs
│       └── trending_products.py   # Streaming #2: Tendances
│
├── 📂 kafka/                       # Kafka
│   ├── requirements.txt           # Dépendances Python
│   └── log_producer.py            # Producteur Kafka
│
└── 📂 scripts/                     # Scripts utilitaires
    ├── setup.sh                   # Configuration initiale
    ├── prepare_hdfs.sh            # Préparation HDFS
    ├── run_batch.sh               # Lancer analyses batch
    ├── run_streaming.sh           # Guide streaming
    ├── stop.sh                    # Arrêter les services
    └── clean.sh                   # Nettoyage complet
```

---

## 🎓 Parcours d'Apprentissage Recommandé

### Niveau 1: Débutant
1. Lire **[QUICKSTART.md](QUICKSTART.md)**
2. Exécuter `./scripts/setup.sh`
3. Lancer `docker-compose up -d`
4. Voir les résultats dans MongoDB

**Temps estimé**: 15 minutes

---

### Niveau 2: Intermédiaire
1. Comprendre l'architecture dans **[ARCHITECTURE.md](ARCHITECTURE.md)**
2. Étudier le code des analyses batch
3. Modifier les seuils et relancer
4. Explorer les interfaces web

**Temps estimé**: 1 heure

---

### Niveau 3: Avancé
1. Lire la section "Méthode de Raisonnement"
2. Tester le streaming en conditions réelles
3. Implémenter une nouvelle analyse
4. Optimiser les performances Spark

**Temps estimé**: 2-3 heures

---

## 🔍 Trouver une Information

### Je cherche...

#### ...comment démarrer le projet
→ [QUICKSTART.md](QUICKSTART.md) - Section "Installation en 5 Étapes"

#### ...les justifications techniques
→ [ARCHITECTURE.md](ARCHITECTURE.md) - Section "Justifications Techniques"

#### ...comment exécuter les analyses batch
→ [README.md](README.md) - Section "Exécution des Analyses"

#### ...comment tester le streaming
→ [QUICKSTART.md](QUICKSTART.md) - Section "Tester le Streaming"

#### ...le format des données en entrée
→ [README.md](README.md) - Section "Description du Dataset"

#### ...les résultats MongoDB
→ [README.md](README.md) - Section "Consultation des Résultats"

#### ...les interfaces web disponibles
→ [QUICKSTART.md](QUICKSTART.md) - Section "Interfaces Web Disponibles"

#### ...comment dépanner une erreur
→ [QUICKSTART.md](QUICKSTART.md) - Section "Dépannage Rapide"

#### ...les technologies utilisées
→ [LIVRABLE.md](LIVRABLE.md) - Section "Architecture Technique"

#### ...les compétences démontrées
→ [LIVRABLE.md](LIVRABLE.md) - Section "Compétences Démontrées"

---

## 📊 Analyses Disponibles

### Batch (Données Historiques)

| # | Nom | Fichier | Objectif |
|---|-----|---------|----------|
| 1 | Top Produits | `spark/batch/top_products.py` | Identifier les 10 produits les plus consultés |
| 2 | Codes HTTP | `spark/batch/http_codes.py` | KPIs de santé du serveur (succès, erreurs) |
| 3 | Top IPs | `spark/batch/top_ips.py` | Détecter utilisateurs actifs et bots |

### Streaming (Temps Réel)

| # | Nom | Fichier | Objectif |
|---|-----|---------|----------|
| 1 | Détection Erreurs | `spark/streaming/error_detection.py` | Alertes sur pics d'erreurs 404/500 |
| 2 | Produits Tendance | `spark/streaming/trending_products.py` | Identifier produits populaires (>20 vues/min) |

---

## 🛠️ Technologies & Ports

| Service | Technologie | Version | Port(s) | Interface Web |
|---------|------------|---------|---------|---------------|
| HDFS NameNode | Hadoop | 3.2.1 | 9870, 9000 | ✅ http://localhost:9870 |
| HDFS DataNode | Hadoop | 3.2.1 | 9864 | ✅ http://localhost:9864 |
| Spark Master | Spark | 3.3.0 | 8080, 7077 | ✅ http://localhost:8080 |
| Spark Worker | Spark | 3.3.0 | 8081 | ✅ http://localhost:8081 |
| Kafka | Kafka | 7.3.0 | 9092, 9093 | ❌ CLI uniquement |
| Zookeeper | Zookeeper | 7.3.0 | 2181 | ❌ CLI uniquement |
| MongoDB | MongoDB | 6.0 | 27017 | ❌ CLI uniquement |

---

## 📝 Commandes Essentielles

### Démarrage
```bash
./scripts/setup.sh              # Configuration initiale
docker-compose up -d            # Démarrer les services
./scripts/prepare_hdfs.sh       # Préparer HDFS
./scripts/run_batch.sh          # Lancer analyses batch
```

### Vérification
```bash
docker-compose ps               # État des conteneurs
docker logs -f spark-master     # Logs Spark
docker exec -it mongodb mongo   # Shell MongoDB
```

### Arrêt
```bash
./scripts/stop.sh               # Arrêter proprement
./scripts/clean.sh              # Nettoyage complet
```

---

## 🎯 Checklist de Validation

Avant de rendre le projet, vérifiez:

- [ ] Tous les conteneurs sont "Up" (`docker-compose ps`)
- [ ] HDFS contient les logs (`docker exec namenode hdfs dfs -ls /logs`)
- [ ] Les 3 analyses batch s'exécutent sans erreur
- [ ] Les résultats sont dans MongoDB (`db.top_products.find()`)
- [ ] Les interfaces web sont accessibles
- [ ] La documentation est complète (4 fichiers MD)
- [ ] Le code est commenté et propre
- [ ] Les scripts sont exécutables (`chmod +x`)

---

## 📚 Ressources Complémentaires

### Documentation Officielle
- [Apache Spark](https://spark.apache.org/docs/latest/) - Documentation Spark
- [Apache Kafka](https://kafka.apache.org/documentation/) - Documentation Kafka
- [HDFS](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsUserGuide.html) - Guide HDFS
- [MongoDB](https://docs.mongodb.com/) - Documentation MongoDB

### Tutoriels
- [Spark RDD Programming Guide](https://spark.apache.org/docs/latest/rdd-programming-guide.html)
- [Structured Streaming Guide](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html)
- [Kafka Quickstart](https://kafka.apache.org/quickstart)

---

## 💡 Astuces

### Performance
- Augmenter `SPARK_WORKER_MEMORY` pour gros volumes
- Ajuster `spark.sql.shuffle.partitions` pour optimiser les shuffles
- Utiliser `.cache()` sur les DataFrames réutilisés

### Debugging
- Activer les logs détaillés: `spark.sparkContext.setLogLevel("INFO")`
- Vérifier les jobs dans Spark UI: http://localhost:4040
- Monitorer HDFS dans NameNode UI: http://localhost:9870

### Production
- Augmenter le facteur de réplication HDFS à 3
- Ajouter des Workers Spark pour parallélisme
- Implémenter des checkpoints pour fault-tolerance
- Mettre en place un monitoring (Prometheus/Grafana)

---

## 🤝 Contribution

Ce projet est académique. Pour des améliorations:
1. Forker le projet
2. Créer une branche (`git checkout -b feature/amelioration`)
3. Commiter les changements (`git commit -m 'Ajout fonctionnalité'`)
4. Pusher (`git push origin feature/amelioration`)
5. Créer une Pull Request

---

## 📞 Support

Problème rencontré ?
1. Consulter [QUICKSTART.md](QUICKSTART.md) - Section "Dépannage"
2. Vérifier les logs: `docker logs -f <service>`
3. Redémarrer: `docker-compose restart <service>`
4. Nettoyage complet: `./scripts/clean.sh` puis recommencer

---

## 🎉 Félicitations !

Vous avez maintenant accès à une architecture Big Data complète et fonctionnelle.

**Bon courage pour votre projet ! 🚀**

---

*Document généré le 28 Janvier 2025*  
*Projet académique - Architecture Big Data Distribuée*
