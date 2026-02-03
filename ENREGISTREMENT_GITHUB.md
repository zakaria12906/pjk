# Enregistrement des tests sur GitHub (pjk)

Ce fichier explique comment **enregistrer tous les guides de test, réponses et fichiers** sur le dépôt **https://github.com/zakaria12906/pjk.git**.

---

## Fichiers à enregistrer

- `GUIDE_TEST_ETAPES.md` – Guide de test API / application
- `GUIDE_TEST_ETAPES_TP_BIGDATA.md` – Guide de test TP Big Data (étape par étape)
- `RESULTATS_TESTS.md` – Résultats des tests API
- `RESULTATS_TESTS_TP_BIGDATA.md` – Résultats des tests TP Big Data (à remplir puis commiter)
- `RESUME_API.md` – Résumé des endpoints API
- `README.md` – Description du dépôt et des tests
- `ENREGISTREMENT_GITHUB.md` – Ce fichier

---

## Étapes pour pousser sur GitHub

### 1. Ouvrir un terminal dans le dossier du dépôt

Le dossier doit contenir `.git`, `README.md`, les guides et les fichiers de résultats.

```bash
cd /chemin/vers/pjk
# Exemple : cd ~/Desktop/pjk  ou  cd /Users/zakariaeelouazzani/.cursor/worktrees/Projet_charazad/moo
```

### 2. Vérifier l’état des fichiers

```bash
git status
```

Vous devez voir les fichiers modifiés ou nouveaux (guides, résultats, README).

### 3. Ajouter tous les fichiers

```bash
git add .
```

Ou ajouter fichier par fichier :

```bash
git add GUIDE_TEST_ETAPES_TP_BIGDATA.md
git add RESULTATS_TESTS_TP_BIGDATA.md
git add README.md
git add ENREGISTREMENT_GITHUB.md
```

### 4. Créer un commit

```bash
git commit -m "Tests TP Big Data - guide étape par étape et résultats du $(date +%Y-%m-%d)"
```

Ou avec une date en texte libre :

```bash
git commit -m "Tests TP Big Data - guide et résultats du 03/02/2025"
```

### 5. Vérifier la branche et le remote

```bash
git branch
git remote -v
```

Le remote doit pointer vers `https://github.com/zakaria12906/pjk.git` (ou équivalent en SSH).

Si le remote n’est pas configuré :

```bash
git remote add origin https://github.com/zakaria12906/pjk.git
```

### 6. Pousser sur GitHub

```bash
git push origin main
```

*(Remplacer `main` par `master` si votre branche par défaut s’appelle `master`.)*

Si GitHub demande une authentification (utilisateur / mot de passe ou token), renseigner les identifiants.

### 7. Vérifier sur le site

Ouvrir **https://github.com/zakaria12906/pjk** et vérifier que les fichiers suivants sont présents :

- `GUIDE_TEST_ETAPES_TP_BIGDATA.md`
- `RESULTATS_TESTS_TP_BIGDATA.md`
- `README.md` (avec la section TP Big Data)
- `ENREGISTREMENT_GITHUB.md`

---

## Résumé des commandes (copier-coller)

```bash
cd /chemin/vers/pjk
git add .
git status
git commit -m "Tests TP Big Data - guide étape par étape et résultats"
git push origin main
```

---

## En cas de problème

- **Conflit ou refus de push :** faire d’abord `git pull origin main` puis corriger les conflits si nécessaire, et refaire `git push origin main`.
- **Authentification :** GitHub n’accepte plus le mot de passe ; utiliser un **Personal Access Token** (Settings → Developer settings → Personal access tokens) ou une clé SSH.
- **Dépôt vide ou nouveau :** la première fois, il est possible d’avoir à faire `git push -u origin main`.
