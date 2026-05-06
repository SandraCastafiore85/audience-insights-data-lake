 


## Data Mart (Marché de données) d’engagement de l’audience

## Produit de Données pour l’Analyse de la consommation des médias

## Vue d’ensemble

Comprendre comment les audiences interagissent avec le contenu est essentiel. Il s’agit ici d’un produit de données conçu pour offrir une vision fiable du comportement des consommateurs, dans le respect de leurs données personnelles, permettant aux parties prenantes de suivre la performance et d’identifier des opportunités d’optimisation.

Cette implémentation démontre :

* La gestion de produit appliquée aux plateformes de données (équilibrage des compromis).
* L’ingénierie des données moderne via une architecture Medallion (Bronze/Argent/Or).
* L’utilisation responsable des données grâce à une approche « privacy-by-design » et à l’exclusion des données personnelles identifiables (PII).

---

## Problématique & Stratégie

Les données d’audience sont généralement fragmentées, coûteuses à traiter et sensibles. Ce produit cible les équipes marketing et éditoriales qui doivent répondre aux questions suivantes :

* Comment l’engagement évolue-t-il dans le temps ?
* Quelles catégories de contenu génèrent le plus de temps de visionnage ?
* Où devons-nous prioriser les ressources éditoriales ?

## Décisions stratégiques de conception

1. Niveau d’agrégation (quotidien) : Choisi stratégiquement plutôt que le temps réel afin de réduire significativement les coûts d’infrastructure tout en répondant aux besoins d’analyse hebdomadaire et mensuelle.
2. Métriques pré-agrégées : Sacrifie la flexibilité des événements bruts pour garantir aux utilisateurs non techniques un accès immédiat aux indicateurs dont ils ont besoin.
3. Traitement par lots ("batch) plutôt que streaming : Priorise la fiabilité et des ressources adaptées pour une facturation cloud prévisible.

---

## 🚀 Architecture technique

Le pipeline suit un modèle Lakehouse, automatisant le flux de données depuis l’exploration locale jusqu’à la visualisation à l’échelle du cloud.

* Source : fichiers Parquet locaux (simulation d’événements multiplateformes).
  ** Données sources : F. Maxwell Harper et Joseph A. Konstan. 2015. The MovieLens Datasets: History and Context. ACM Transactions on Interactive Intelligent Systems (TiiS) 5, 4, Article 19 (décembre 2015), 19 pages. DOI=[http://dx.doi.org/10.1145/2827872](http://dx.doi.org/10.1145/2827872)
* Bronze (stockage) : ingestion brute dans Google Cloud Storage (GCS).
* Argent/Or (entrepôt) : Google BigQuery utilisant une stratégie de tables externes. Cela permet une architecture « Zero-Copy » où BigQuery interroge directement GCS, minimisant les coûts de stockage.
* Couche BI : Looker Studio pour les tableaux de bord exécutifs.

## 🛠️ Stack technologique

* Langage : Python 3.12 (environnement virtuel isolé .venv).
* Plateforme cloud : Google Cloud (GCP).
* Région : northamerica-northeast1 (Montréal, Canada), en supposant un besoin de conformité en matière de résidence des données.
* Automatisation : SDK Python google-cloud-storage & CLI gcloud.

---

## 🔧 Implémentation & Configuration

## 1. Ingestion Cloud (Python)

J’ai développé `src/cloud_storage_setup.py` pour automatiser :

* Authentification ADC : liaison sécurisée des environnements locaux à GCP sans clés codées en dur.
* Provisionnement régional : création programmatique de buckets à Montréal.
* Téléversement automatisé : mapping des fichiers locaux `data_processed` vers des objets cloud (blobs).

## 2. Entrepôt de données (BigQuery)

Pour permettre l’utilisation de Looker Studio, j’ai associé les fichiers Parquet de la couche Gold à un schéma BigQuery :

```
bq mk --external_table_definition=PARQUET=gs://[BUCKET_NAME]/*.parquet \
audience_insights_dataset_2026.daily_engagement
```

---

## 🐞 Debugging

La construction de ce produit a nécessité la résolution de plusieurs défis d’infrastructure réels :

* Gestion de la facturation et des quotas : résolution d’erreurs 403 en liant programmatiquement le projet à un compte de facturation via la CLI — un obstacle courant dans les nouveaux environnements cloud.
* Gestion des permissions : correction de conflits CLI spécifiques à macOS dans `~/.config/gcloud` via des ajustements de propriété (chown) et de permissions (chmod).
* Alignement régional : gestion de la contrainte selon laquelle les buckets GCS et les datasets BigQuery doivent être co-localisés (Montréal) pour éviter les échecs d’exécution des requêtes.

---

## 📁 Structure du repository

```
├── dashboards          # Exports PDF / liens Looker Studio (en cours)
├── data
│   ├── 01_raw          # Fichiers sources bruts (CSV)
│   ├── 02_bronze       # Couches Medallion (Parquet)
│   ├── 03_silver
│   └── 04_gold         # Source finale du « produit de données »
├── notebooks           # Logique de transformation
├── requirements.txt    # Dépendances du projet
└── README.md   
```

---

## 📈 Améliorations futures

* Intégration Airflow : refactoriser l’ingestion Python et la configuration BigQuery en DAG Apache Airflow pour une orchestration robuste.
* Analyse de sentiment : intégrer le dataset `tags.csv` pour analyser le sentiment des retours utilisateurs en joignant les tags générés par les utilisateurs avec les métriques d’engagement.
* Fondations ML : intégrer des modèles de scoring d’engagement directement dans la transformation Silver vers Gold.


## Audience Engagement Mart
Data Product for Cross-Platform Media Analytics
------------------------------
## 🎯 Overview
In a fragmented digital media ecosystem, understanding how audiences engage with content across platforms is critical. This is a Data Product designed to provide a reliable, privacy-conscious, and cost-efficient view of behavior, enabling stakeholders to monitor performance and identify optimization opportunities.
This implementation demonstrates:

* Product Management of data platforms (balancing trade-offs).
* Modern Data Engineering via a Medallion architecture (Bronze/Silver/Gold).
* Responsible Data Use through privacy-by-design and PII exclusion.

------------------------------
## 📋 Problem Statement & Strategy
Audience data is typically fragmented, expensive to process, and sensitive. This product targets marketing and editorial stakeholders who need to answer:

* How is engagement evolving over time?
* Which content categories drive the most watch time?
* Where should we prioritize editorial resources?

## Strategic Design Decisions

   1. Aggregation Level (Daily): Strategically chosen over real-time to significantly reduce infrastructure costs while still meeting weekly/monthly strategy needs.
   2. Pre-Aggregated Metrics: Sacrifices raw-event flexibility to ensure non-technical users have "instant-on" access to cthe metrics they need.
   3. Batch over Streaming: Prioritizes reliability and right-sized compute clusters for predictable cloud billing.

------------------------------
## 🚀 Technical Architecture
The pipeline follows a Lakehouse pattern, automating the movement of data from local discovery to cloud-scale visualization.

* Source: Local Parquet files (simulating cross-platform events).
** Source data: F. Maxwell Harper and Joseph A. Konstan. 2015. The MovieLens Datasets: History and Context. ACM Transactions on Interactive Intelligent Systems (TiiS) 5, 4, Article 19 (December 2015), 19 pages. DOI=<http://dx.doi.org/10.1145/2827872>
* Bronze (Storage): Raw ingestion into Google Cloud Storage (GCS).
* Silver/Gold (Warehouse): Google BigQuery utilizing an External Table strategy. This allows for a "Zero-Copy" architecture where BigQuery queries GCS directly, minimizing storage costs.
* BI Layer: Looker Studio for executive dashboards.

## 🛠️ Tech Stack

* Language: Python 3.12 (Isolated .venv).
* Cloud Platform: Google Cloud (GCP).
* Region: northamerica-northeast1 (Montreal, Canada), supposing a need for data residency compliance.
* Automation: Python google-cloud-storage SDK & GCloud CLI.

------------------------------
## 🔧 Implementation & Setup## 1. Cloud Ingestion (Python)
I developed src/cloud_storage_setup.py to automate:

* ADC Authentication: Securely linking local environments to GCP without hardcoded keys.
* Regional Provisioning: Programmatically creating buckets in Montreal.
* Automated Upload: Mapping local data_processed files to cloud blobs.

## 2. Warehousing (BigQuery)
To enable Looker Studio, I mapped the Gold-layer Parquet files to a BigQuery schema:

bq mk --external_table_definition=PARQUET=gs://[BUCKET_NAME]/*.parquet \
audience_insights_dataset_2026.daily_engagement

------------------------------
## 🐞 Critical Debugging & Lessons Learned
Building this product required resolving several real-world infrastructure hurdles:

* Billing & Quota Management: Resolved 403 errors by programmatically linking the project to a billing account via CLI—a common hurdle in new cloud environments.
* Permission Orchestration: Fixed macOS-specific CLI conflicts in ~/.config/gcloud using ownership (chown) and permission (chmod) adjustments.
* Regional Alignment: Navigated the constraint that GCS Buckets and BigQuery Datasets must be co-located (Montreal) to prevent query execution failures.

------------------------------
## 📁 Repository Structure

├── dashboards          # Looker Studio PDF exports/links (under construction)
├── data
│   ├── 01_raw          # Raw source files (CSV)
│   ├── 02_bronze       # Medallion Layers (Parquet)
│   ├── 03_silver
│   └── 04_gold         # Final 'Data Product' source
├── notebooks           # logic for transformations
├── requirements.txt    # Project dependencies
└── README.md   
------------------------------
## 📈 Future Enhancements

* Airflow Integration: Refactor the Python ingestion and BigQuery setup into an Apache Airflow DAG for robust scheduling.
* Sentiment analysis: Integrate the tags.csv dataset to perform Sentiment Analysis on audience feedback by joining user-generated tags with engagement metrics.
* ML Foundations: Integrating engagement scoring models directly into the Silver-to-Gold transformation.

