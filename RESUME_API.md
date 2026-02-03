# Résumé des endpoints API (d’après les logs)

Ce document liste les routes observées dans les fichiers de log du serveur. À adapter selon votre implémentation réelle (base URL, port, paramètres).

---

## Utilisateur

| Méthode | Route            | Exemple de code dans les logs |
|---------|------------------|-------------------------------|
| GET     | /user/login      | 200                           |
| POST    | /user/login      | 200, 500                      |
| PUT     | /user/login      | 301, 500                      |
| DELETE  | /user/login      | 404                           |
| DELETE  | /user/register   | 404                           |

À implémenter / tester : **POST /user/register** pour l’inscription.

---

## Panier

| Méthode | Route | Exemple de code dans les logs |
|---------|--------|-------------------------------|
| GET     | /cart | 200, 403                      |
| POST    | /cart | 200                           |
| DELETE  | /cart | 200, 404                      |

---

## Checkout

| Méthode | Route     | Exemple de code dans les logs |
|---------|-----------|-------------------------------|
| GET     | /checkout | 403                           |
| POST    | /checkout | 200, 500                      |

---

## Produits (par catégorie)

Format observé : `/products/<categorie>?id=<id>`.

| Catégorie              | Méthodes vues   | Codes observés      |
|------------------------|-----------------|---------------------|
| eyeliner               | GET, PUT, POST, DELETE, OPTIONS | 200, 301, 403, 404, 500 |
| lipstick               | GET, POST, OPTIONS     | 200, 404, 500       |
| skincare/cream         | GET, PUT, DELETE, OPTIONS | 200, 301, 403, 404, 500 |
| skincare/serum         | GET, PUT, POST  | 200, 301, 404, 500  |
| skincare/sunscreen     | GET, PUT, POST, DELETE | 200, 403, 404, 500  |
| foundation             | GET, PUT, DELETE, OPTIONS | 200, 301, 403, 404, 500 |
| mascara                | GET, PUT, POST, DELETE, OPTIONS | 200, 301, 404, 500 |
| hair/shampoo           | GET, PUT, POST  | 200, 403, 500       |
| hair/conditioner       | POST, DELETE, OPTIONS  | 301, 403, 404       |

---

## Recommandations

| Méthode | Route                 | Exemple de code dans les logs |
|---------|------------------------|-------------------------------|
| GET     | /api/recommendations   | 404                           |
| POST    | /api/recommendations   | 500                           |
| PUT     | /api/recommendations   | 403                           |
| OPTIONS | /api/recommendations   | 404                           |

---

## Fichiers de log du projet

- `server_web.log.txt` : format condensé (IP, méthode, chemin, code, taille).
- `web_server (2) (1).log.txt` : format type Combined Log (avec date complète et protocole HTTP).

Utiliser ces fichiers pour vérifier les codes de réponse réels après vos tests et pour analyser les 404/500.
