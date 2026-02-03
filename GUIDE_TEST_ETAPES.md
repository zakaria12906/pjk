# Guide de test – étape par étape

Ce document décrit comment vérifier que l’application (API + front) fonctionne correctement.

---

## Prérequis

- [ ] Serveur backend démarré (port à noter, ex. 3000 ou 8080)
- [ ] Frontend démarré si applicable (ex. `npm run dev`)
- [ ] Base de données accessible (si utilisée)
- [ ] Outil pour les requêtes HTTP : Postman, Insomnia, ou `curl`

---

## Étape 1 : Vérifier que le serveur répond

**Objectif :** S’assurer que le serveur web est bien lancé.

1. Ouvrir un terminal.
2. Lancer le serveur (commande selon votre projet, ex. `npm start` ou `python app.py`).
3. Dans un autre terminal ou dans Postman :
   - **Requête :** `GET http://localhost:PORT/` (remplacer PORT par le port utilisé).
   - **Résultat attendu :** Code 200 (ou 304) et une page ou un message de bienvenue.

**À noter dans RESULTATS_TESTS.md :** Code HTTP reçu, message d’erreur éventuel.

---

## Étape 2 : Tester l’inscription utilisateur

**Objectif :** Vérifier que l’endpoint d’inscription accepte un nouvel utilisateur.

1. Envoyer une requête **POST** vers l’URL d’inscription (ex. `POST /user/register`).
2. Corps de la requête (ex. JSON) :
   ```json
   {
     "email": "test@example.com",
     "password": "MotDePasse123",
     "name": "Utilisateur Test"
   }
   ```
3. **Résultat attendu :** Code 200 ou 201, et un message de succès ou un token.

**À noter :** Code HTTP, corps de la réponse, erreur éventuelle.

---

## Étape 3 : Tester la connexion (login)

**Objectif :** Vérifier que le login fonctionne.

1. Envoyer **POST** vers l’URL de login (ex. `POST /user/login`).
2. Corps (ex. JSON) :
   ```json
   {
     "email": "test@example.com",
     "password": "MotDePasse123"
   }
   ```
3. **Résultat attendu :** Code 200 et un token ou des infos utilisateur.

**À noter :** Code HTTP, présence d’un token, message d’erreur éventuel.

---

## Étape 4 : Tester les produits (catalogue)

**Objectif :** Vérifier que les endpoints produits répondent.

D’après les logs, les routes ressemblent à :

- `GET /products/eyeliner?id=1`
- `GET /products/lipstick?id=1`
- `GET /products/skincare/cream?id=1`
- `GET /products/skincare/serum?id=1`
- `GET /products/skincare/sunscreen?id=1`
- `GET /products/foundation?id=1`
- `GET /products/mascara?id=1`
- `GET /products/hair/shampoo?id=1`
- `GET /products/hair/conditioner?id=1`

1. Choisir une catégorie (ex. `eyeliner`).
2. Envoyer **GET** vers `http://localhost:PORT/products/eyeliner?id=1`.
3. **Résultat attendu :** Code 200 et des données produit (JSON ou HTML selon l’API).

Répéter pour 2–3 catégories différentes.

**À noter :** Code HTTP pour chaque requête, erreurs 404/500 éventuelles.

---

## Étape 5 : Tester le panier (cart)

**Objectif :** Vérifier ajout, lecture et suppression du panier.

1. **Ajouter au panier**  
   - **POST** vers `/cart` avec un body contenant l’ID produit et la quantité.  
   - **Résultat attendu :** Code 200.

2. **Voir le panier**  
   - **GET** vers `/cart`.  
   - **Résultat attendu :** Code 200 et liste des articles.

3. **Supprimer le panier (ou un article)**  
   - **DELETE** vers `/cart` (ou endpoint spécifique si vous en avez un).  
   - **Résultat attendu :** Code 200.

**À noter :** Codes HTTP et réponses pour chaque action.

---

## Étape 6 : Tester le checkout

**Objectif :** Vérifier que la validation de commande fonctionne.

1. S’assurer qu’il y a au moins un article dans le panier.
2. Envoyer **POST** vers `/checkout` (avec les données nécessaires : adresse, paiement, etc., selon votre API).
3. **Résultat attendu :** Code 200 et confirmation de commande (ID commande, message, etc.).

**À noter :** Code HTTP, message de confirmation ou erreur.

---

## Étape 7 : Tester l’API de recommandations (si applicable)

**Objectif :** Vérifier l’endpoint `/api/recommendations`.

1. Envoyer **GET** ou **POST** vers `http://localhost:PORT/api/recommendations` (avec ou sans paramètres selon votre doc).
2. **Résultat attendu :** Code 200 et une liste de recommandations (ou message explicite si non implémenté).

**À noter :** Code HTTP et extrait de la réponse.

---

## Étape 8 : Vérifier les logs serveur

**Objectif :** S’assurer qu’il n’y a pas d’erreurs critiques dans les logs.

1. Consulter le fichier de log du serveur (ex. `server_web.log.txt` ou sortie console).
2. Repérer les codes **500**, **403**, **404** et noter les lignes concernées.
3. Vérifier l’absence de stack traces ou de messages d’erreur non gérés.

**À noter :** Nombre approximatif d’erreurs 4xx/5xx sur les dernières requêtes.

---

## Étape 9 : Test rapide avec curl (récapitulatif)

Vous pouvez enregistrer ces commandes et les exécuter en remplaçant `PORT` et les chemins :

```bash
# 1. Santé du serveur
curl -s -o /dev/null -w "%{http_code}" http://localhost:PORT/

# 2. Login
curl -X POST http://localhost:PORT/user/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"MotDePasse123"}'

# 3. Un produit
curl -s -w "\nHTTP_CODE:%{http_code}" http://localhost:PORT/products/eyeliner?id=1

# 4. Panier
curl -X GET http://localhost:PORT/cart
```

**À noter :** Coller les sorties dans RESULTATS_TESTS.md.

---

## Checklist finale

- [ ] Serveur répond (étape 1)
- [ ] Inscription fonctionne (étape 2)
- [ ] Login fonctionne (étape 3)
- [ ] Au moins 2 endpoints produits retournent 200 (étape 4)
- [ ] Panier : ajout + GET + DELETE OK (étape 5)
- [ ] Checkout retourne 200 ou comportement attendu (étape 6)
- [ ] Recommandations testées (étape 7)
- [ ] Logs vérifiés (étape 8)
- [ ] Résultats reportés dans RESULTATS_TESTS.md

Si toutes les cases sont cochées et les codes HTTP sont conformes à ce que vous attendez, vous pouvez considérer que les tests principaux sont OK. Pour une mise en production, prévoir en plus des tests de charge et de sécurité.
