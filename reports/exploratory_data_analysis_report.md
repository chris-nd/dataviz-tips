# Rapport d'analyse exploratoire des données

## 1. Résumé exécutif

Ce rapport synthétise l'exploration, l'analyse statistique et les visualisations du jeu de données `tips` de Seaborn, ainsi que les fonctions de tracé du projet. Le dataset source comprend 244 lignes et 7 variables. Le chargement applicatif via `load_tips()` supprime le doublon complet détecté et fournit 243 lignes aux analyses et visualisations.

Principaux résultats calculés sur ces 243 lignes préparées :

- Aucune valeur manquante n'a été détectée.
- Une occurrence du doublon complet a été supprimée.
- Avec la règle de l'écart interquartile (IQR), 9 factures et 8 pourboires dépassent leur borne supérieure respective. Ces valeurs sont conservées, car aucun élément ne montre qu'elles sont erronées.
- La corrélation de Pearson entre le montant de la facture et le pourboire est positive et forte (**r = 0,675**). Elle reste forte (**r = 0,605**) après exclusion exploratoire des valeurs au-dessus des seuils.
- Les tables de deux personnes sont les plus fréquentes (**155 tables, environ 64 %**).

## 2. Périmètre et objectif

L'objectif est de décrire la structure et la qualité des données, d'examiner les distributions numériques et de visualiser les relations entre montants facturés, pourboires et taille des groupes.

Les notebooks répondent notamment aux questions suivantes :

- Quelles sont les dimensions et les variables du dataset ?
- Existe-t-il des valeurs manquantes ou des doublons ?
- Quelles observations dépassent les seuils statistiques calculés par la règle IQR ?
- Le montant du pourboire varie-t-il avec celui de la facture ?
- Comment les factures et les groupes se répartissent-ils selon le nombre de personnes à table ?

## 3. Description du jeu de données

### 3.1 Source et unité d'observation

- Source : `seaborn.load_dataset("tips")`
- Nom du jeu de données : `tips`
- Unité d'observation : une facture associée à un repas et à un groupe de clients
- Unité monétaire indiquée dans le dictionnaire : USD
- Identifiant : aucun identifiant client ou transaction n'est fourni
- Effectif : 244 lignes à la source, 243 après déduplication

### 3.2 Variables

| Variable     | Type                               | Description                                        | Valeurs / étendue           |
| ------------ | ---------------------------------- | -------------------------------------------------- | --------------------------- |
| `total_bill` | Quantitative continue (`float64`)  | Montant total de la facture                        | 3,07 à 50,81                |
| `tip`        | Quantitative continue (`float64`)  | Montant du pourboire                               | 1,00 à 10,00                |
| `sex`        | Catégorielle nominale (`category`) | Sexe indiqué dans le jeu de données pour le client | `Female`, `Male`            |
| `smoker`     | Catégorielle nominale (`category`) | Statut de fumeur indiqué                           | `Yes`, `No`                 |
| `day`        | Catégorielle (`category`)          | Jour du repas; catégorie pandas non ordonnée       | `Thur`, `Fri`, `Sat`, `Sun` |
| `time`       | Catégorielle nominale (`category`) | Moment du repas                                    | `Lunch`, `Dinner`           |
| `size`       | Quantitative discrète (`int64`)    | Nombre de personnes à table                        | 1 à 6                       |

Seaborn fournit les variables catégorielles avec le type pandas `category`. Le chargement source occupe environ 7,4 Ko en mémoire selon `DataFrame.info()`.

## 4. Qualité et préparation des données

### 4.1 Valeurs manquantes

Le contrôle de `isna()` ne détecte aucune valeur manquante : le taux est de **0 %** pour chacune des sept variables.

### 4.2 Doublon

L'exploration détecte un doublon complet entre les observations d'index 198 et 202 : `total_bill` = 13,00, `tip` = 2,00, `sex` = `Female`, `smoker` = `Yes`, `day` = `Thur`, `time` = `Lunch` et `size` = 2.

La fonction `drop_duplicate_rows()` supprime une occurrence et réinitialise l'index. La fonction `load_tips()` applique ce nettoyage au chargement de la source. L'effectif transmis aux analyses et visualisations est ainsi de **243 lignes**. Sans identifiant unique, il n'est pas possible de confirmer si les deux repas identiques sont une répétition accidentelle ou deux transactions distinctes.

## 5. Analyse descriptive des variables numériques

Les statistiques suivantes sont calculées sur les 243 lignes fournies par `load_tips()`.

| Variable     | Moyenne | Médiane | Écart-type |    Q1 |    Q3 | Minimum | Maximum |
| ------------ | ------: | ------: | ---------: | ----: | ----: | ------: | ------: |
| `total_bill` |   19,81 |   17,81 |       8,91 | 13,38 | 24,18 |    3,07 |   50,81 |
| `tip`        |    3,00 |    2,92 |       1,39 |  2,00 |  3,58 |    1,00 |   10,00 |
| `size`       |    2,57 |    2,00 |       0,95 |  2,00 |  3,00 |       1 |       6 |

Pour `total_bill` et `tip`, la moyenne dépasse la médiane et les maxima sont éloignés du troisième quartile. Cela suggère des distributions étirées vers les montants élevés, également visibles dans les histogrammes. Une valeur élevée n'est pas pour autant une erreur.

## 6. Valeurs extrêmes

Les notebooks appliquent la règle de Tukey : les bornes sont définies par `Q1 − 1,5 × IQR` et `Q3 + 1,5 × IQR`. Les valeurs strictement supérieures à la borne haute sont comptées ci-dessous.

| Variable     | Borne inférieure | Borne supérieure | Observations au-dessus de la borne | Part des 243 lignes |
| ------------ | ---------------: | ---------------: | ---------------------------------: | ------------------: |
| `total_bill` |            -2,81 |            40,37 |                                  9 |              3,70 % |
| `tip`        |            -0,36 |             5,94 |                                  8 |              3,29 % |

Trois observations dépassent simultanément les deux bornes; **14 lignes distinctes** dépassent au moins l'une d'elles. Les huit pourboires au-dessus de leur seuil sont associés à des factures supérieures à la médiane de `total_bill`.

Les boîtes à moustaches permettent de repérer visuellement les points au-delà des moustaches. Elles illustrent les seuils IQR calculés; ces points sont des observations atypiques au regard de cette règle, pas nécessairement des erreurs.

**Décision :** conserver les valeurs extrêmes de facture et de pourboire, faute d'indice qu'elles soient incorrectes. Les tailles de groupe 1, 5 ou 6 sont également rares mais plausibles et sont conservées.

## 7. Relations entre variables

### 7.1 Facture et pourboire

La corrélation de Pearson entre `total_bill` et `tip` est de **0,675** sur les 243 observations préparées. Le nuage de points montre une relation positive : les factures plus élevées sont généralement associées à des pourboires plus élevés. Le montant brut du pourboire dépend donc aussi du montant de la facture et ne mesure pas à lui seul la générosité.

### 7.2 Corrélations numériques

| Variables              | Corrélation sur les 243 lignes | Après exclusion exploratoire des valeurs dépassant au moins une borne | Intensité retenue |
| ---------------------- | -----------------------------: | --------------------------------------------------------------------: | ----------------- |
| `total_bill` et `tip`  |                          0,675 |                                                                 0,605 | Forte             |
| `total_bill` et `size` |                          0,598 |                                                                 0,562 | Forte             |
| `tip` et `size`        |                          0,488 |                                                                 0,413 | Moyenne           |

La comparaison porte sur les 243 observations préparées et sur un sous-ensemble de **229 lignes** qui ne dépassent ni le seuil de facture ni celui du pourboire. Les écarts absolus des trois corrélations sont inférieurs à 0,1; leur sens et leur classement sont conservés. Cela indique que les valeurs extrêmes ne pilotent pas à elles seules les associations observées. Leur retrait réduit toutefois l'étendue des données et ne constitue pas la décision de nettoyage retenue.

Les niveaux d'intensité suivent les conventions indiquées dans le notebook d'analyse. Une corrélation décrit une association, pas un lien de causalité.

### 7.3 Taille des groupes

| Personnes à table (`size`) | Nombre de tables | Part approximative |
| -------------------------: | ---------------: | -----------------: |
|                          1 |                4 |             1,65 % |
|                          2 |              155 |            63,79 % |
|                          3 |               38 |            15,64 % |
|                          4 |               37 |            15,23 % |
|                          5 |                5 |             2,06 % |
|                          6 |                4 |             1,65 % |

Les tables de deux personnes sont largement majoritaires. Les groupes de trois et quatre personnes représentent chacun environ 15 % des observations; ceux de une, cinq ou six personnes sont peu fréquents. La corrélation positive entre `size` et `total_bill` (**r = 0,598**) est cohérente avec des factures généralement plus élevées pour les groupes plus nombreux, sans établir de causalité.

## 8. Visualisations et fonctions du projet

Les notebooks `03_visualization_matplotlib.ipynb` et `03_visualization_seaborn.ipynb` présentent les visualisations avec les deux bibliothèques. Ils comprennent notamment :

- des histogrammes de `total_bill` et `tip` ;
- un nuage de points comparant facture et pourboire ;
- des boîtes à moustaches illustrant les valeurs extrêmes ;
- le comptage des tables par taille de groupe ;
- une matrice de corrélation des variables numériques.

Le module `src/dataviz_tips/plots.py` fournit les fonctions de tracé Matplotlib et Seaborn associées, ainsi que des fonctions pour calculer et afficher une matrice de corrélation et enregistrer les figures.

## 9. Limites

- L'absence d'identifiant empêche de confirmer la nature du doublon.
- Les données ne comportent pas de métadonnées permettant d'évaluer leur représentativité ou de généraliser les constats à l'ensemble des restaurants.
- Les effectifs des tailles de groupe sont déséquilibrés; les comparaisons entre groupes doivent tenir compte de ces différences.
- Les seuils IQR signalent des valeurs atypiques au sens statistique, pas nécessairement des erreurs.
- Les corrélations et visualisations présentées sont descriptives et ne permettent pas d'inférer une causalité.

## 10. Conclusion et recommandations

Le jeu `tips` est compact, ne présente aucune valeur manquante et contient un doublon complet supprimé par `load_tips()`. Les 243 lignes préparées montrent des distributions étirées vers les montants élevés, quelques valeurs au-dessus des bornes IQR et une association positive forte entre facture et pourboire. Les observations atypiques et les tailles de groupe rares sont conservées, car rien ne prouve qu'elles soient erronées.

Recommandations :

1. Utiliser `load_tips()` comme point d'entrée commun dans les notebooks d'analyse et de visualisation; conserver le chargement brut dans le notebook d'exploration pour documenter le doublon avant son traitement.
2. Régénérer les sorties des notebooks après toute modification du chargement ou des calculs afin que les résultats affichés reflètent bien le code exécuté.
3. Conserver les valeurs extrêmes identifiées par l'IQR, les signaler et vérifier leur influence selon la question étudiée.
4. Interpréter les corrélations comme des associations descriptives et éviter toute conclusion causale.
5. Tenir compte de l'absence d'identifiant et de métadonnées de représentativité avant de généraliser les résultats.
