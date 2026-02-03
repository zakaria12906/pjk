# Projet Charazad – Documentation et tests

Ce dépôt contient la **documentation de test** et les **résumés d’API** pour vérifier que l’application fonctionne correctement, ainsi que le **guide de test du TP Big Data**.

Dépôt GitHub : **https://github.com/zakaria12906/pjk.git**

---

## Contenu du dépôt

| Fichier | Description |
|---------|-------------|
| **GUIDE_TEST_ETAPES.md** | Guide de test étape par étape (serveur, inscription, login, produits, panier, checkout, recommandations, logs) |
| **GUIDE_TEST_ETAPES_TP_BIGDATA.md** | Guide de test étape par étape pour le **TP Big Data** (Docker, HDFS, Spark, Kafka, MongoDB, analyses batch et streaming) |
| **RESUME_API.md** | Résumé des endpoints API déduits des logs (user, cart, checkout, products, recommendations) |
| **RESULTATS_TESTS.md** | Modèle pour noter les résultats de chaque étape de test (API / app) |
| **RESULTATS_TESTS_TP_BIGDATA.md** | Modèle pour noter les résultats des tests du **TP Big Data** |
| **README.md** | Ce fichier |

Les fichiers de log du serveur (`server_web.log.txt`, `web_server (2) (1).log.txt`) restent en local et ne sont pas versionnés (voir `.gitignore`) car ils peuvent être très volumineux.

---

## Comment tester – API / application

1. Lire **GUIDE_TEST_ETAPES.md**.
2. Démarrer le serveur et le frontend.
3. Suivre les étapes 1 à 9 (santé, inscription, login, produits, panier, checkout, recommandations, logs).
4. Remplir **RESULTATS_TESTS.md** au fur et à mesure.
5. Vérifier la checklist finale dans le guide.

---

## Comment tester – TP Big Data

1. Lire **GUIDE_TEST_ETAPES_TP_BIGDATA.md**.
2. Avoir le projet TP Big Data (avec `docker-compose.yml`, `spark-apps/`, `data/`) sur votre machine.
3. Suivre les étapes 1 à 7 (Docker, HDFS, analyse batch, interfaces web, analyse streaming, communication, arrêt).
4. Remplir **RESULTATS_TESTS_TP_BIGDATA.md** au fur et à mesure.
5. Vérifier la checklist finale dans le guide.
6. Enregistrer les réponses et pousser sur ce dépôt (voir ci‑dessous).

---

## Prérequis pour les tests

**API / application :**
- Serveur backend lancé (port connu).
- Outil HTTP : Postman, Insomnia ou `curl`.
- (Optionnel) Frontend lancé pour tests navigateur.

**TP Big Data :**
- Docker et Docker Compose installés et démarrés.
- Python 3 (pour le producteur Kafka).
- Projet TP Big Data avec les fichiers décrits dans le guide.

---

## Enregistrer les réponses et pousser sur GitHub

Après avoir exécuté les tests et rempli les fichiers de résultats :

```bash
# Dans le dossier du dépôt pjk
git add .
git status
git commit -m "Tests TP Big Data - résultats du [DATE]"
git push origin main
```

Vérifier sur **https://github.com/zakaria12906/pjk** que les fichiers sont bien présents (guides, résultats, README).

---

## Clone et mise à jour du dépôt

```bash
git clone https://github.com/zakaria12906/pjk.git
cd pjk
# après modifications (ex. résultats des tests)
git add .
git commit -m "Résultats des tests du [date]"
git push origin main
```
