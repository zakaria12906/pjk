# 📦 PROJET COMPLET - Organisation et Démarrage

## ✅ Organisation Terminée

Tous les fichiers ont été organisés dans le projet `Projet_charazad`.

---

## 📁 Structure Complète

```
Projet_charazad/
│
├── 📄 README.md                      # Documentation principale (NOUVEAU)
├── 📄 ARCHITECTURE.md                # Justifications techniques détaillées
├── 📄 QUICKSTART.md                  # Guide démarrage rapide (10 min)
├── 📄 LIVRABLE.md                    # Document de livraison académique
├── 📄 INDEX.md                       # Navigation dans le projet
├── 📄 PROJET_COMPLET.md              # Ce fichier
│
├── 🐳 docker-compose.yml             # Orchestration des 7 services
├── 📝 .gitignore                     # Fichiers à ignorer (mis à jour)
│
├── 📂 data/                          # Données
│   ├── web_server.log               # Logs d'exemple (40 lignes)
│   └── generate_logs.py             # Générateur de logs (10k lignes)
│
├── 📂 spark/                         # Applications Spark
│   ├── requirements.txt             # pyspark==3.3.0, pymongo==4.3.3
│   │
│   ├── 📂 batch/                    # Analyses Batch
│   │   ├── top_products.py          # ✅ Top 10 produits
│   │   ├── http_codes.py            # ✅ Codes HTTP + KPIs
│   │   └── top_ips.py               # ✅ Top 10 IPs + détection bots
│   │
│   └── 📂 streaming/                # Analyses Streaming
│       ├── error_detection.py       # ✅ Détection erreurs temps réel
│       └── trending_products.py     # ✅ Produits en tendance
│
├── 📂 kafka/                         # Kafka
│   ├── requirements.txt             # kafka-python==2.0.2
│   └── log_producer.py              # Producteur Kafka (simulation)
│
└── 📂 scripts/                       # Scripts utilitaires
    ├── setup.sh                     # ✅ Configuration initiale
    ├── prepare_hdfs.sh              # ✅ Préparation HDFS
    ├── run_batch.sh                 # ✅ Lancer analyses batch
    ├── run_streaming.sh             # ✅ Guide streaming
    ├── stop.sh                      # ✅ Arrêter services
    └── clean.sh                     # ✅ Nettoyage complet
```

**Total**: 27 fichiers organisés

---

## 🚀 Comment Démarrer le Projet ?

### Option 1: Démarrage Rapide (10 minutes)

Suivez le guide **[QUICKSTART.md](QUICKSTART.md)** qui vous guide étape par étape.

### Option 2: Commandes Directes

```bash
# 1. Se placer dans le projet
cd /Users/zakariaeelouazzani/Desktop/Projet_charazad

# 2. Configuration initiale
chmod +x scripts/*.sh
./scripts/setup.sh

# 3. Démarrer les services Docker
docker-compose up -d

# 4. Attendre ~2 minutes, puis préparer HDFS
./scripts/prepare_hdfs.sh

# 5. Lancer les analyses batch
./scripts/run_batch.sh

# 6. Consulter les résultats
docker exec -it mongodb mongo
> use logs_analytics
> db.top_products.find().pretty()
```

---

## 📊 Services Disponibles

Une fois démarré, vous avez accès à :

| Service | URL | Description |
|---------|-----|-------------|
| **HDFS NameNode** | http://localhost:9870 | Interface web HDFS |
| **HDFS DataNode** | http://localhost:9864 | État DataNode |
| **Spark Master** | http://localhost:8080 | Interface Spark Master |
| **Spark Worker** | http://localhost:8081 | État Worker |
| **MongoDB** | localhost:27017 | Base de données (CLI) |
| **Kafka** | localhost:9092 | Broker Kafka (CLI) |
| **Zookeeper** | localhost:2181 | Coordination (CLI) |

---

## 🎯 Analyses Disponibles

### Batch (Données Historiques)

| # | Analyse | Fichier | Objectif | Temps |
|---|---------|---------|----------|-------|
| 1 | Top Produits | `spark/batch/top_products.py` | 10 produits les plus consultés | ~30s |
| 2 | Codes HTTP | `spark/batch/http_codes.py` | KPIs santé serveur | ~30s |
| 3 | Top IPs | `spark/batch/top_ips.py` | IPs actives + détection bots | ~30s |

### Streaming (Temps Réel)

| # | Analyse | Fichier | Objectif | Fenêtre |
|---|---------|---------|----------|---------|
| 1 | Détection Erreurs | `spark/streaming/error_detection.py` | Alertes erreurs 404/500 | 5 min |
| 2 | Produits Tendance | `spark/streaming/trending_products.py` | Produits populaires (>20/min) | 1 min |

---

## 📚 Documentation

### Pour Démarrer
- **[README.md](README.md)** - Documentation principale avec instructions complètes
- **[QUICKSTART.md](QUICKSTART.md)** - Démarrage en 10 minutes

### Pour Approfondir
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Justifications techniques, flux de données, algorithmes
- **[LIVRABLE.md](LIVRABLE.md)** - Document de livraison académique
- **[INDEX.md](INDEX.md)** - Navigation et index complet

### Pour Tester
- **[GUIDE_TEST_ETAPES.md](GUIDE_TEST_ETAPES.md)** - Tests de l'application web
- **[RESUME_API.md](RESUME_API.md)** - Résumé des endpoints API
- **[RESULTATS_TESTS.md](RESULTATS_TESTS.md)** - Template résultats

---

## 🔧 Technologies Utilisées

### Stockage et Traitement
- **HDFS** 3.2.1 - Stockage distribué
- **Apache Spark** 3.3.0 - Traitement batch et streaming
- **Apache Kafka** 7.3.0 - Streaming de données
- **Zookeeper** 7.3.0 - Coordination

### Stockage Résultats
- **MongoDB** 6.0 - Base NoSQL

### Infrastructure
- **Docker** & **Docker Compose** - Orchestration

### Langages
- **Python** 3.7+ - PySpark, scripts

---

## 🎓 Compétences Démontrées

✅ Architecture distribuée Lambda (Batch + Streaming)  
✅ HDFS pour stockage distribué  
✅ Spark RDD et DataFrame  
✅ Spark Structured Streaming  
✅ Kafka pour messaging  
✅ MongoDB pour NoSQL  
✅ Docker pour containerization  
✅ Windowing et Watermarking  
✅ Parsing et regex  
✅ Agrégations et transformations  

---

## 💾 Enregistrer sur GitHub

Le projet est déjà initialisé avec Git et configuré pour le repo :
**https://github.com/zakaria12906/pjk.git**

Pour pousser les nouveaux fichiers Big Data :

```bash
cd /Users/zakariaeelouazzani/Desktop/Projet_charazad

# Ajouter les fichiers Big Data
git add docker-compose.yml
git add data/ spark/ kafka/ scripts/
git add ARCHITECTURE.md QUICKSTART.md LIVRABLE.md INDEX.md
git add README.md

# Commit
git commit -m "Ajout architecture Big Data complète avec Spark, HDFS, Kafka, MongoDB"

# Push
git push origin main
```

---

## ✅ Checklist de Validation

Avant de commencer à utiliser le projet :

- [ ] Docker Desktop est installé et démarré
- [ ] Au moins 8GB RAM disponible
- [ ] Ports 9870, 9864, 8080, 8081, 27017, 9092, 2181 libres
- [ ] Scripts rendus exécutables (`chmod +x scripts/*.sh`)

Pour valider que tout fonctionne :

- [ ] `docker-compose ps` montre 7 conteneurs "Up"
- [ ] http://localhost:9870 accessible (HDFS)
- [ ] http://localhost:8080 accessible (Spark)
- [ ] Les 3 analyses batch s'exécutent sans erreur
- [ ] Les résultats apparaissent dans MongoDB

---

## 🐛 En Cas de Problème

### Ports déjà utilisés
```bash
# Trouver le processus
lsof -i :9870

# Tuer le processus
kill -9 <PID>
```

### Conteneurs qui ne démarrent pas
```bash
# Voir les logs
docker logs -f <nom_conteneur>

# Redémarrer
docker-compose restart <nom_conteneur>
```

### Nettoyage complet
```bash
./scripts/clean.sh
# Puis recommencer depuis le début
```

### Besoin d'aide
1. Consulter [QUICKSTART.md](QUICKSTART.md) - Section "Dépannage"
2. Vérifier les logs : `docker logs -f <service>`
3. Consulter [ARCHITECTURE.md](ARCHITECTURE.md) pour comprendre le fonctionnement

---

## 🎉 Félicitations !

Vous avez maintenant un projet Big Data complet et opérationnel avec :

✅ 7 services distribués orchestrés  
✅ 5 analyses (3 batch + 2 streaming)  
✅ Documentation complète (6 fichiers MD)  
✅ Scripts d'automatisation (6 scripts)  
✅ Intégration GitHub configurée  

**Prêt pour la production et les tests ! 🚀**

---

*Document créé le 3 Février 2026*  
*Projet: Architecture Big Data Distribuée*
