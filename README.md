# P7 : Résoudre des problèmes en utilisant des algorithmes en Python

## Description

Ce projet, réalisé pour **AlgoInvest&Trade**, consiste à développer et optimiser des algorithmes pour 
l’investissement. Il inclut une solution **brute-force** explorant toutes les combinaisons possibles 
d’actions, ainsi qu’une **version optimisée** capable de traiter rapidement un grand nombre d’actions 
tout en respectant les contraintes du problème :

- chaque action ne peut être achetée qu’une seule fois ;
- nous ne pouvons pas acheter une fraction d'action ;
- nous pouvons dépenser au maximum 500 euros par client.

## Pré-requis

Avant de commencer, assurez-vous d'utiliser les versions suivantes de Python et pip :

- Python 3.12.8
- pip 25.1.1

## Installation

1. **Clonez le dépôt** sur votre machine locale :

``` 
git clone https://github.com/myriamdesporte/P7.git
```

2. **Créez un environnement virtuel** :

```
python -m venv env
```

3. **Activez l'environnement virtuel** :

- Sur Linux/macOS :
  ```
  source env/bin/activate
  ```
- Sur Windows :
  ```
  .\env\Scripts\activate
  ```

4. **Installez les dépendances** à partir du fichier `requirements.txt`:

```
pip install -r requirements.txt
```

## Lancer les programmes

Une fois l'environnement virtuel activé et les dépendances installées,
exécutez les commandes suivantes depuis la racine du projet :

#### Algorithme bruteforce
```
python bruteforce_itertools.py
```
ou
```
python bruteforce_recursive.py
```
#### Algorithme optimisé
```
python optimized.py
```

Au démarrage, le programme vous demandera de choisir un jeu de données en entrant 1, 2 ou 3 :

1. Dataset1 (1000 actions)
2. Dataset2 (1000 actions)
3. Liste initiale de 20 actions

Le script utilisera alors le jeu de données correspondant pour l’optimisation.

## Vérification de la syntaxe avec Flake8

Pour assurer la qualité du code et sa conformité à la norme **PEP 8**, ce projet utilise `flake8` 
avec le plugin `flake8-html`, tous les deux inclus dans `requirements.txt` déjà installés précédemment.

Cela permet de générer automatiquement un rapport HTML à chaque exécution de la commande `flake8 .`
Ce rapport est disponible dans le dossier `flake8_report/`.

### Génération du rapport HTML flake8

Voici les étapes pour générer un nouveau rapport **flake8**: 

1. Exécutez la commande suivante depuis la racine du projet :
```
python -m flake8 .
 ```
2. Ouvrez le rapport généré dans votre navigateur :

- Sur Linux/macOS :
```
open flake8_report/index.html
```

- Sur Windows :
```
start flake8-report\index.html
```
