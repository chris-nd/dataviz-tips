# Dictionnaire des données - dataset `tips`

## 1. Vue d'ensemble

- Source : `seaborn.load_dataset("tips")`
- Jeu de données : `tips`
- Nombre de lignes : 244
- Nombre de colonnes : 7
- Unité d'observation : une facture de restaurant / un repas dans un groupe de clients
- Contexte : jeu de données de référence utilisé pour analyser les habitudes de paiement et de pourboire dans un restaurant.

## 2. Description du dataset

Le dataset contient des informations sur le montant total de la facture, le pourboire, les caractéristiques du client et le contexte du repas. Il ne comporte pas de variable d'identifiant unique. Les variables sont majoritairement numériques et catégorielles.

## 3. Dictionnaire des variables

| Variable | Type | Description | Unité | Valeurs / exemple | Rôle | Format technique / Transformation |
|---------|------|-------------|-------|------------------|------|----------------------------------|
| `total_bill` | Numérique continu | Montant total de la facture payé par le groupe | USD | 3.07 à 50.81 | Variable explicative / quantitative | Conservé en `float` |
| `tip` | Numérique continu | Montant du pourboire donné | USD | 1.00 à 10.00 | Variable cible ou explicative | Conservé en `float` |
| `sex` | Catégorielle nominale | Sexe du client ou du groupe de clients | - | `Female`, `Male` | Variable catégorielle | Convertie en `category` avec pandas/seaborn |
| `smoker` | Catégorielle nominale | Indique si le client est fumeur ou non | - | `Yes`, `No` | Variable catégorielle | Convertie en `category` avec pandas/seaborn |
| `day` | Catégorielle ordinale | Jour de la semaine du repas | - | `Sun`, `Sat`, `Thur`, `Fri` | Variable temporelle / catégorielle | Convertie en `category` avec pandas/seaborn |
| `time` | Catégorielle nominale | Moment de la journée du repas | - | `Dinner`, `Lunch` | Variable temporelle / catégorielle | Convertie en `category` avec pandas/seaborn |
| `size` | Numérique discret | Nombre de personnes dans le groupe | personnes | 1 à 6 | Variable quantitative discrète | Conservé en `int` |

## 4. Informations de qualité des données

### 4.1 Valeurs manquantes

- Nombre total de valeurs manquantes : 0
- Pourcentage moyen de valeurs manquantes : 0%
- Analyse : aucune colonne ne contient de donnée absente à première vue.

### 4.2 Doublons

- Nombre de lignes dupliquées : 1
- Constat : un doublon a été détecté sur une ligne du dataset.
- Décision : le doublon a été supprimé pour éviter un biais de répétition et préserver la qualité du jeu de données.
- Impact potentiel : très faible sur le volume total, mais il aurait pu introduire un biais mineur si le doublon correspondait à une saisie répétée.

### 4.3 Types de variables

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

Le dataset `tips` est un jeu de données simple, bien structuré et exploitable pour l'analyse exploratoire. Il comporte 7 variables, aucune valeur manquante, et un seul doublon détecté, ce qui le rend adapté à des analyses descriptives, de corrélation et de visualisation.
