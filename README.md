# Projet Charazad – Documentation et tests

Ce dépôt contient la **documentation de test** et les **résumés d’API** pour vérifier que l’application fonctionne correctement.

Dépôt GitHub : **https://github.com/zakaria12906/pjk.git**

---

## Contenu du dépôt

| Fichier | Description |
|---------|-------------|
| **GUIDE_TEST_ETAPES.md** | Guide de test étape par étape (serveur, inscription, login, produits, panier, checkout, recommandations, logs) |
| **RESUME_API.md** | Résumé des endpoints API déduits des logs (user, cart, checkout, products, recommendations) |
| **RESULTATS_TESTS.md** | Modèle pour noter les résultats de chaque étape de test |
| **README.md** | Ce fichier |

Les fichiers de log du serveur (`server_web.log.txt`, `web_server (2) (1).log.txt`) restent en local et ne sont pas versionnés (voir `.gitignore`) car ils peuvent être très volumineux.

---

## Comment tester – résumé

1. Lire **GUIDE_TEST_ETAPES.md**.
2. Démarrer le serveur et le frontend.
3. Suivre les étapes 1 à 9 (santé, inscription, login, produits, panier, checkout, recommandations, logs).
4. Remplir **RESULTATS_TESTS.md** au fur et à mesure.
5. Vérifier la checklist finale dans le guide.

---

## Prérequis pour les tests

- Serveur backend lancé (port connu).
- Outil HTTP : Postman, Insomnia ou `curl`.
- (Optionnel) Frontend lancé pour tests navigateur.

---

## Clone et mise à jour du dépôt

```bash
git clone https://github.com/zakaria12906/pjk.git
cd pjk
# après modifications
git add .
git commit -m "Résultats des tests du [date]"
git push origin main
```
