#  Automatisation des Ventes — Projet de Fin d'Année

> **Matière :** Logiciels  
> **Auteur :** Med Firas Dhahri  
> **Année :** 2025-2026

---

##  Description

Script Python qui automatise l'analyse des données de ventes d'une entreprise e-commerce.  
Il lit un fichier CSV, effectue tous les calculs financiers (CA Brut, CA Net, TVA), affiche un résumé et exporte les résultats.

---

##  Structure du projet

```
pfa_ventes/
├── ventes.py              # Script principal
├── ventes.csv             # Données de ventes (généré automatiquement)
├── resultats_final.csv    # Résultats exportés (généré à l'exécution)
├── graphiques_ventes.png  # Graphiques Matplotlib (bonus)
├── requirements.txt       # Dépendances Python
└── README.md              # Ce fichier
```

---

##  Installation & Configuration

### 1. Prérequis

- Python **3.10+** installé sur votre machine
- Git installé

### 2. Cloner le dépôt

```bash
git clone https://github.com/firas-doctor/automatisation-ventes
cd pfa_ventes
```

### 3. Créer et activer l'environnement virtuel

**Windows (PowerShell) :**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (CMD) :**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

>  Votre terminal affichera `(venv)` devant le prompt une fois activé.

### 4. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

##  Utilisation

### Exécution standard (génère `ventes.csv` automatiquement)

```bash
python ventes.py
```

### Bonus — Lecture dynamique d'un autre fichier CSV

```bash
python ventes.py mon_fichier_custom.csv
```

Le fichier custom doit respecter le format :

```
ID,Prix,Quantite,Remise
101,15.0,3,10
...
```

---

##  Formules utilisées

| Colonne     | Formule                            |
|-------------|------------------------------------|
| CA Brut     | `Prix × Quantité`                  |
| CA Net      | `CA Brut × (1 - Remise / 100)`     |
| TVA (20 %)  | `CA Net × 0.20`                    |
| CA TTC      | `CA Net + TVA`                     |

---

##  Fichiers générés

| Fichier                | Description                                          |
|------------------------|------------------------------------------------------|
| `ventes.csv`           | Données brutes de départ                             |
| `resultats_final.csv`  | Résultats avec CA Brut, CA Net, TVA, CA TTC          |
| `graphiques_ventes.png`| Graphiques bar + camembert (si Matplotlib installé) |

---

##  Dépendances

Voir `requirements.txt` :

```
matplotlib>=3.8
```

> Les modules `csv`, `os`, `sys` sont inclus dans la bibliothèque standard Python.

---

##  Workflow Git recommandé

```bash
# Initialiser (première fois)
git init
git add .
git commit -m "Initial commit - PFA Automatisation des Ventes"

# Pousser sur GitHub
git remote add origin https://github.com/<votre-username>/pfa_ventes.git
git branch -M main
git push -u origin main

# Cycle de travail quotidien
git add .
git commit -m "feat: description de la modification"
git push
```

### Branches suggérées

```bash
git checkout -b feature/graphiques    # pour le bonus Matplotlib
git checkout -b feature/export-excel  # pour une future extension
```

---

##  Exemple de sortie console

```
[OK] Fichier 'ventes.csv' généré avec 8 produits.

   ID     Prix   Qté   Rem%    CA Brut     CA Net      TVA     CA TTC
-------------------------------------------------------------------
  101    15.00     3    10.0      45.00      40.50     8.10      48.60
  102    25.00     2     5.0      50.00      47.50     9.50      57.00
  ...

=============================================
  CA Total (TTC) de l'entreprise : 623.52 €
=============================================

[TOP] Produit avec le plus gros bénéfice :
       ID=108  |  CA Net=112.50 €  |  CA TTC=135.00 €

[OK] Résultats exportés dans 'resultats_final.csv'.
[OK] Graphique sauvegardé dans 'graphiques_ventes.png'.
```

---

##  Licence

Projet académique — Faculté des Sciences de Tunis.