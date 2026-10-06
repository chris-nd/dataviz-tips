# Rapport d'analyse exploratoire des données

## 1. Résumé exécutif

Ce rapport synthétise les constats des notebooks d'exploration, d'analyse statistique et de visualisation appliqués au jeu de données `tips` de Seaborn. Celui-ci décrit des factures de restaurant, les pourboires associés et le contexte des repas.

Principaux résultats :

- Le jeu de données source contient **244 lignes et 7 variables**, sans valeur manquante ni identifiant unique.
- L'exploration a repéré un doublon complet aux lignes d'index 198 et 202. Le notebook d'exploration supprime une occurrence, laissant **243 lignes** dans son objet de travail.
- Les statistiques et graphiques des deux autres notebooks sont calculés après un nouveau chargement du jeu source; ils portent donc sur les **244 lignes initiales**, doublon compris.
- Les factures et les pourboires présentent des distributions étirées vers les valeurs élevées. Avec la règle de l'écart interquartile (IQR), 9 factures et 9 pourboires dépassent leur borne supérieure respective; les observations sont conservées car elles ne sont pas reconnues comme erreurs.
- Sur les 244 lignes analysées, la corrélation de Pearson entre le montant de la facture et celui du pourboire est positive et forte (**r = 0,674**). Elle reste forte après exclusion exploratoire des valeurs au-dessus des seuils (**r = 0,605**).
- Les tables de deux personnes sont les plus fréquentes (**156 tables, environ 64 %**).

## 2. Périmètre et objectif

L'objectif est de décrire la structure et la qualité des données, d'examiner les principales distributions et de visualiser les relations entre les montants facturés, les pourboires et la taille des groupes.

Les notebooks répondent notamment aux questions suivantes :

- Quelles sont les dimensions, les variables et les valeurs présentes ?
- Les données comportent-elles des valeurs manquantes ou des doublons ?
- Quelles observations dépassent les seuils statistiques calculés par la règle IQR ?
- Le montant du pourboire évolue-t-il avec le montant de la facture ?
- Comment les factures se répartissent-elles selon le nombre de personnes à table ?

## 3. Description du jeu de données

### 3.1 Source et unité d'observation

- Source : `seaborn.load_dataset("tips")`
- Nom du jeu de données : `tips`
- Unité d'observation : une facture associée à un repas et à un groupe de clients
- Devise indiquée dans le dictionnaire : USD
- Identifiant : aucun identifiant client ou transaction n'est fourni

### 3.2 Variables

| Variable | Type | Description | Valeurs / étendue |
|---|---|---|---|
| `total_bill` | Quantitative continue (`float64`) | Montant total de la facture | 3,07 à 50,81 |
| `tip` | Quantitative continue (`float64`) | Montant du pourboire | 1,00 à 10,00 |
| `sex` | Catégorielle nominale (`category`) | Sexe indiqué dans le jeu de données | `Female`, `Male` |
| `smoker` | Catégorielle nominale (`category`) | Statut de fumeur indiqué | `Yes`, `No` |
| `day` | Catégorielle (`category`) | Jour du repas | `Thur`, `Fri`, `Sat`, `Sun` |
| `time` | Catégorielle nominale (`category`) | Moment du repas | `Lunch`, `Dinner` |
| `size` | Quantitative discrète (`int64`) | Nombre de personnes à table | 1 à 6 |

Les variables catégorielles sont chargées avec le type `category` de pandas. Le dataset source compte 244 observations et occupe environ 7,4 Ko en mémoire selon `info()`.

## 4. Qualité et préparation des données

### 4.1 Valeurs manquantes

Le contrôle de `isna()` ne détecte aucune valeur manquante : le taux moyen est de **0 %** et le nombre de valeurs manquantes est nul pour chacune des sept variables.

### 4.2 Doublon

L'exploration détecte une ligne dupliquée complète : les observations aux index 198 et 202 ont les mêmes valeurs (`total_bill` = 13,00, `tip` = 2,00, `sex` = `Female`, `smoker` = `Yes`, `day` = `Thur`, `time` = `Lunch`, `size` = 2).

Le notebook `01_exploration.ipynb` applique `drop_duplicates()` et vérifie que l'objet ainsi préparé ne contient plus de doublon. Une occurrence est donc supprimée dans cette étape, pour un total de **243 lignes après déduplication**. Sans identifiant unique, il reste impossible de déterminer si les deux repas identiques correspondent réellement à une erreur de saisie.

### 4.3 Cohérence entre les notebooks

Les notebooks `02_analyze.ipynb` et `03_visualization.ipynb` rechargent chacun `tips` directement depuis Seaborn. Ils ne reprennent pas l'objet dédupliqué créé dans le notebook d'exploration. En conséquence, leurs statistiques, seuils, corrélations et graphiques concernent le jeu source de **244 lignes et incluent le doublon**.

Les résultats numériques ci-dessous sont donc rapportés tels qu'ils apparaissent dans le notebook d'analyse, sans les présenter comme des calculs sur les 243 lignes dédupliquées. Pour assurer la cohérence du projet, il faudra réutiliser le même jeu de données préparé dans les étapes d'analyse et de visualisation, puis recalculer les indicateurs.

## 5. Analyse descriptive des variables numériques

Les statistiques descriptives ci-dessous proviennent de `tips.describe()` dans `02_analyze.ipynb` et portent sur 244 observations.

| Variable | Moyenne | Médiane | Écart-type | Q1 | Q3 | Minimum | Maximum |
|---|---:|---:|---:|---:|---:|---:|---:|
| `total_bill` | 19,79 | 17,80 | 8,90 | 13,35 | 24,13 | 3,07 | 50,81 |
| `tip` | 3,00 | 2,90 | 1,38 | 2,00 | 3,56 | 1,00 | 10,00 |
| `size` | 2,57 | 2,00 | 0,95 | 2,00 | 3,00 | 1 | 6 |

Pour `total_bill` et `tip`, la moyenne est supérieure à la médiane et les maxima sont éloignés du troisième quartile. Cela suggère une asymétrie vers les montants élevés, visible également dans les histogrammes du notebook de visualisation. Cette observation décrit la forme des distributions; elle ne signifie pas que les valeurs élevées sont erronées.

## 6. Valeurs extrêmes

Le notebook statistique utilise la règle de Tukey : les bornes sont calculées comme `Q1 − 1,5 × IQR` et `Q3 + 1,5 × IQR`. Les valeurs au-dessus de la borne supérieure sont considérées comme extrêmes selon cette règle.

| Variable | Borne inférieure | Borne supérieure | Observations au-dessus de la borne | Part des 244 lignes |
|---|---:|---:|---:|---:|
| `total_bill` | -2,82 | 40,30 | 9 | 3,69 % |
| `tip` | -0,34 | 5,91 | 9 | 3,69 % |

Trois observations dépassent simultanément les deux bornes; **15 lignes distinctes** dépassent au moins l'une des deux. Les 9 pourboires au-dessus de leur seuil sont associés à des factures supérieures à la médiane de `total_bill`.

Les notebooks de visualisation vérifient visuellement les bornes à l'aide de boîtes à moustaches. Les points au-delà des moustaches correspondent aux observations signalées par la règle IQR.

**Décision de traitement :** les valeurs extrêmes de facture et de pourboire sont conservées. Le notebook ne montre pas d'élément établissant qu'elles sont erronées; leur rareté seule ne justifie pas leur suppression. Les tailles de groupe de 1, 5 ou 6 personnes sont également peu fréquentes, mais plausibles, et sont conservées.

## 7. Relations entre variables

### 7.1 Facture et pourboire

Le coefficient de corrélation de Pearson entre `total_bill` et `tip` est de **0,674** sur les 244 observations. Le nuage de points du notebook de visualisation montre une relation positive : les factures plus élevées sont généralement associées à des pourboires plus élevés. Le montant brut du pourboire ne mesure donc pas uniquement la générosité; il est aussi lié à la taille de la facture.

### 7.2 Corrélations numériques

| Variables | Corrélation sur les 244 lignes | Après exclusion exploratoire des lignes dépassant au moins une des deux bornes | Intensité retenue dans le notebook |
|---|---:|---:|---|
| `total_bill` et `tip` | 0,674 | 0,605 | Forte |
| `total_bill` et `size` | 0,597 | 0,561 | Forte |
| `tip` et `size` | 0,488 | 0,413 | Moyenne |

L'analyse compare les corrélations calculées sur les 244 observations à celles d'un sous-ensemble de 229 lignes ne dépassant ni la borne de facture ni celle de pourboire. Les écarts absolus sont inférieurs à 0,1 pour les trois paires; le classement et le sens des relations restent les mêmes. Cela indique que les observations extrêmes ne pilotent pas à elles seules les corrélations observées. Le retrait de ces valeurs réduit cependant l'étendue des données et ne constitue pas la décision de nettoyage retenue.

Les intensités (« faible », « moyenne », « forte ») suivent les seuils conventionnels indiqués dans le notebook. Une corrélation décrit une association et ne démontre pas un lien de causalité.

### 7.3 Taille des groupes

| Personnes à table (`size`) | Nombre de tables | Part approximative |
|---:|---:|---:|
| 1 | 4 | 1,64 % |
| 2 | 156 | 63,93 % |
| 3 | 38 | 15,57 % |
| 4 | 37 | 15,16 % |
| 5 | 5 | 2,05 % |
| 6 | 4 | 1,64 % |

Les tables de deux personnes sont nettement majoritaires. Les groupes de trois et quatre personnes représentent chacun environ 15 % des observations, tandis que les groupes de une, cinq ou six personnes sont peu fréquents. La corrélation positive entre `size` et `total_bill` (r = 0,597) est cohérente avec des factures généralement plus élevées pour les groupes plus nombreux, sans établir de causalité.

## 8. Visualisations produites

Le notebook `03_visualization.ipynb` produit :

- des histogrammes pour les distributions de `total_bill` et de `tip` ;
- un nuage de points comparant le montant de la facture et le pourboire ;
- des boîtes à moustaches pour comparer les valeurs observées aux seuils IQR ;
- une visualisation des factures selon la taille du groupe ;
- une matrice de corrélation des variables numériques.

Les réponses documentées dans le notebook confirment la relation entre facture et pourboire, la correspondance entre les points isolés et les bornes IQR, ainsi que la prédominance des tables de deux personnes.

## 9. Limites de l'analyse

- L'absence d'identifiant empêche d'examiner les répétitions de transactions et de confirmer la nature du doublon.
- Les analyses statistiques et les visualisations rechargent actuellement le dataset source non dédupliqué; leurs résultats doivent être recalculés sur la version préparée pour être cohérents avec l'exploration.
- Le jeu de données ne fournit pas de métadonnées permettant d'évaluer sa représentativité ou de généraliser les constats à l'ensemble des restaurants.
- Les catégories de jour et les tailles de groupe ne sont pas uniformément réparties, ce qui rend les comparaisons entre groupes de tailles différentes moins équilibrées.
- Les valeurs identifiées par la règle IQR sont des valeurs statistiquement atypiques, pas nécessairement des erreurs.

## 10. Conclusion et recommandations

Le dataset `tips` est compact et ne comporte aucune valeur manquante. L'exploration identifie un doublon complet et le supprime de son objet de travail. L'analyse statistique met en évidence des distributions orientées vers les montants élevés, quelques valeurs dépassant les bornes IQR, et une association positive entre le montant de la facture et le pourboire. Les valeurs extrêmes et les tailles de groupe rares sont conservées, car aucune preuve d'erreur n'est établie.

Recommandations :

1. Centraliser le chargement et le nettoyage du dataset afin que les trois notebooks utilisent le même objet de 243 lignes après déduplication.
2. Recalculer les statistiques descriptives, les seuils IQR, les corrélations et les graphiques après cette harmonisation; indiquer explicitement l'effectif utilisé pour chaque résultat.
3. Conserver les valeurs extrêmes identifiées par l'IQR, tout en les signalant et en vérifiant leur influence dans les analyses.
4. Interpréter les corrélations comme des associations descriptives, sans conclure à une causalité.
5. Tenir compte de l'absence d'identifiant et de métadonnées de représentativité avant de généraliser les résultats.
