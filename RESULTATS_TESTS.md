# Résultats des tests

À remplir lors de l’exécution du guide de test (GUIDE_TEST_ETAPES.md).  
Date des tests : _______________  
Environnement : _______________ (ex. local, port 3000)

---

## Étape 1 – Serveur répond

| Requête | Code HTTP | Remarque |
|---------|-----------|-----------|
| GET / |  |  |

---

## Étape 2 – Inscription

| Requête | Code HTTP | Remarque |
|---------|-----------|-----------|
| POST /user/register |  |  |

---

## Étape 3 – Login

| Requête | Code HTTP | Token reçu ? | Remarque |
|---------|-----------|--------------|----------|
| POST /user/login |  | Oui / Non |  |

---

## Étape 4 – Produits

| Endpoint | Code HTTP | Remarque |
|----------|-----------|----------|
| GET /products/eyeliner?id=1 |  |  |
| GET /products/lipstick?id=1 |  |  |
| GET /products/skincare/cream?id=1 |  |  |
| (autres…) |  |  |

---

## Étape 5 – Panier

| Action | Requête | Code HTTP | Remarque |
|--------|---------|-----------|----------|
| Ajout | POST /cart |  |  |
| Lecture | GET /cart |  |  |
| Suppression | DELETE /cart |  |  |

---

## Étape 6 – Checkout

| Requête | Code HTTP | Remarque |
|---------|-----------|----------|
| POST /checkout |  |  |

---

## Étape 7 – Recommandations

| Requête | Code HTTP | Remarque |
|---------|-----------|----------|
| GET ou POST /api/recommendations |  |  |

---

## Étape 8 – Logs

- Erreurs 5xx remarquées : _______________
- Erreurs 4xx remarquées : _______________
- Autre : _______________

---

## Sortie curl (optionnel)

Coller ici les sorties des commandes curl du guide :

```
(à remplir)
```

---

## Conclusion

- [ ] Tous les tests critiques passent.
- [ ] Problèmes restants : _______________
