# ANALYSE DES EXIGENCES DU SUJET

## ✅ CE QUI EST DEMANDÉ

### Analyses
- **Au moins 2 analyses** en combinant batch ET stream
- Exemples donnés (non obligatoires):
  - Batch: Produits consultés, codes HTTP, IPs actives, temps réponse
  - Stream: Détection erreurs, produits tendance, surveillance IP

### Architecture
- **HDFS** pour stocker les logs
- **Apache Spark** pour traitements (batch et/ou stream)
- **Docker** pour déploiement
- Le sujet mentionne aussi: **Kafka**, **MongoDB**

### Livrables
1. Code source des traitements Spark (batch et/ou stream)
2. Fichier docker-compose.yml

---

## ❌ CE QUI EST ACTUELLEMENT EN TROP

### Documentation excessive (NON DEMANDÉE)
- ❌ ARCHITECTURE.md (514 lignes)
- ❌ QUICKSTART.md (279 lignes)
- ❌ LIVRABLE.md (318 lignes)
- ❌ INDEX.md (271 lignes)
- ❌ README_BIGDATA.md (doublon)
- ❌ PROJET_COMPLET.md

### Scripts d'automatisation (NON DEMANDÉS)
- ❌ scripts/setup.sh
- ❌ scripts/prepare_hdfs.sh
- ❌ scripts/run_batch.sh
- ❌ scripts/run_streaming.sh
- ❌ scripts/stop.sh
- ❌ scripts/clean.sh

### Analyses supplémentaires (SUJET DIT "AU MOINS 2")
**Actuellement: 5 analyses (3 batch + 2 stream)**

Batch:
- ✅ top_products.py (GARDER - exemple explicite du sujet)
- ❌ http_codes.py (SUPPRIMER - analyse en trop)
- ❌ top_ips.py (SUPPRIMER - analyse en trop)

Stream:
- ✅ error_detection.py (GARDER - exemple explicite du sujet)
- ❌ trending_products.py (SUPPRIMER - analyse en trop)

### Utilitaires non demandés
- ❌ data/generate_logs.py (pas demandé)
- ❌ server_web.log.txt (fichier mal formaté)
- ❌ web_server (2) (1).log.txt (fichier mal formaté)

---

## ✅ CE QUI DOIT RESTER

### Fichiers obligatoires
1. **docker-compose.yml** ✅ (demandé dans livrables)
2. **spark/batch/top_products.py** ✅ (1 analyse batch)
3. **spark/streaming/error_detection.py** ✅ (1 analyse stream)
4. **data/web_server.log** ✅ (40 lignes, format correct)
5. **kafka/log_producer.py** ✅ (nécessaire pour streaming)
6. **spark/requirements.txt** ✅
7. **kafka/requirements.txt** ✅
8. **README.md** ✅ (simplifié avec instructions essentielles)
9. **.gitignore** ✅

### Fichiers de test (déjà présents avant)
- GUIDE_TEST_ETAPES.md ✅ (documentait l'API avant)
- RESUME_API.md ✅
- RESULTATS_TESTS.md ✅

---

## 📊 RÉSUMÉ

**Avant nettoyage:** 27 fichiers  
**Après nettoyage:** 12 fichiers  
**Réduction:** -55% de fichiers

**Analyses:**
- Avant: 5 analyses (3 batch + 2 stream)
- Après: 2 analyses (1 batch + 1 stream) ✅ CONFORME
