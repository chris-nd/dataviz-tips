# Dictionnaire des données - dataset `tips`

## 1. Vue d'ensemble

- Source : `seaborn.load_dataset("tips")`
- Jeu de données : `tips`
- Nombre de lignes à la source : 244
- Nombre de lignes après suppression du doublon : 243
- Nombre de colonnes : 7
- Contexte : jeu de données de référence utilisé pour analyser les habitudes de paiement et de pourboire dans un restaurant.

## 2. Description du dataset

Le dataset contient des informations sur le montant total de la facture, le pourboire, les caractéristiques du client et le contexte du repas. Il ne comporte pas de variable d'identifiant unique. Les variables sont majoritairement numériques et catégorielles.

## 3. Dictionnaire de données

| Variable     | Type                  | Description                                        | Unité     | Valeurs / exemple           | Rôle                                | Format / Transformation                                                                  |
| ------------ | --------------------- | -------------------------------------------------- | --------- | --------------------------- | ----------------------------------- | ---------------------------------------------------------------------------------------- |
| `total_bill` | Numérique continu     | Montant total de la facture payé par le groupe     |           | 3.07 à 50.81                | Variable explicative / quantitative | Conservé en `float`                                                                      |
| `tip`        | Numérique continu     | Montant du pourboire donné                         |           | 1.00 à 10.00                | Variable cible ou explicative       | Conservé en `float`                                                                      |
| `sex`        | Catégorielle nominale | Sexe indiqué dans le jeu de données pour le client | -         | `Female`, `Male`            | Variable catégorielle               | Type `category` fourni au chargement par Seaborn                                         |
| `smoker`     | Catégorielle nominale | Indique si le client est fumeur ou non             | -         | `Yes`, `No`                 | Variable catégorielle               | Type `category` fourni au chargement par Seaborn                                         |
| `day`        | Catégorielle          | Jour de la semaine du repas                        | -         | `Sun`, `Sat`, `Thur`, `Fri` | Variable temporelle / catégorielle  | Type `category` fourni au chargement par Seaborn; catégories non ordonnées techniquement |
| `time`       | Catégorielle nominale | Moment de la journée du repas                      | -         | `Dinner`, `Lunch`           | Variable temporelle / catégorielle  | Type `category` fourni au chargement par Seaborn                                         |
| `size`       | Numérique discret     | Nombre de personnes dans le groupe                 | personnes | 1 à 6                       | Variable quantitative discrète      | Conservé en `int`                                                                        |

## 4. Informations sur la qualité des données

### 4.1 Valeurs manquantes

- Nombre total de valeurs manquantes : 0
- Pourcentage moyen de valeurs manquantes : 0%
- Analyse : aucune colonne ne contient de donnée absente à première vue.

### 4.2 Doublons

- Nombre de lignes dupliquées : 1
- Constat : un doublon a été détecté sur une ligne du dataset.
- Décision : le doublon a été supprimé pour éviter un biais de répétition et préserver la qualité du jeu de données.
- Effectif préparé : 243 lignes après suppression d'une des deux observations identiques.
- Impact potentiel : très faible sur le volume total, mais il aurait pu introduire un biais mineur si le doublon correspondait à une saisie répétée.

### 4.3 Types de données

- Numériques : `total_bill`, `tip`, `size`
- Catégorielles : `sex`, `smoker`, `day`, `time`

## 5. Interprétation métier

Les variables du dataset permettent d'explorer les relations entre :

- le montant total de la facture,
- le pourboire,
- la composition du groupe,
- le jour et le moment du repas,
- le fait d'être fumeur ou non,
- et le sexe du client.

Ce type de structure est particulièrement utile pour analyser les facteurs qui influencent le montant du pourboire et les habitudes de dépense dans un contexte de restauration.

## 6. Synthèse

Le dataset `tips` est un jeu de données simple, bien structuré et exploitable pour l'analyse exploratoire. Il comporte 7 variables, aucune valeur manquante et un doublon détecté puis supprimé. L'effectif est de 244 lignes à la source et de 243 lignes après préparation, ce qui le rend adapté à des analyses descriptives, de corrélation et de visualisation.
