# Determinants of Coworking Space Pricing, Amenity Valuation, and User Satisfaction: A Global Revealed-Preference Study

**Student Name:** Regella Krishna Saketh  
**Roll Number / Register Number:** CB.SC.U4CSE23649  
**Class / Section:** CSE G  
**Course:** 23CSE452 Business Analytics  
**Primary Data Source:** [Coworker.com](https://www.coworker.com) (Automated Web-Scraped Global Directory)  
**Deliverable Artifacts:** `README.md`, `data/`, `analysis.ipynb`, `Case_Study_Report.pdf`, `figures/`  

---

## 1. Problem Statement

The post-pandemic acceleration of remote work and digital nomadism has catalyzed explosive expansion across the flexible office sector, with aggregator platforms listing tens of thousands of workspaces across 100+ countries. However, remote workers, freelancers, and distributed enterprise teams face substantial information asymmetry when evaluating workspaces. Platform star ratings cluster heavily at the top of the scale (mean 4.82 / 5.0), obscuring differences between genuine productivity infrastructure and cosmetic marketing perks.

Furthermore, flexible workspace operators struggle with capital allocation decisions:
* Which physical and operational amenities genuinely drive customer retention and 5-star ratings?
* What marginal price premium (% willingness-to-pay in USD) does each workspace feature command in the open market?
* How can workspaces be objectively categorized into strategic market archetypes to benchmark pricing and service offerings?

This case study applies econometric modeling, supervised machine learning, and unsupervised clustering to a bespoke global dataset to resolve these questions.

---

## 2. Project Objectives

1. **Quantify Key Drivers of User Satisfaction:**  
   Determine and rank the relative importance of tangible amenities (e.g., soundproof phone booths, ergonomic chairs, standing desks) versus operational factors (24/7 access, capacity scale) in driving verified customer satisfaction metrics.
2. **Hedonic Pricing Decomposition & Amenity Valuation:**  
   Decompose composite workspace membership fees into constituent attribute values using log-linear hedonic regression, isolating the marginal percentage price premium (% in USD) commanded by individual amenities while controlling for country-level fixed effects.
3. **Unsupervised Market Segmentation & Strategic Benchmarking:**  
   Cluster global flexible workspaces into data-driven competitive tiers using $k$-Means clustering, providing actionable operational recommendations for workspace operators, platform aggregators, and remote professionals.

---

## 3. Data Collection Source & Methodology

To reflect authentic market dynamics and avoid synthetic or pre-packaged repositories (e.g., Kaggle, UCI), primary data was harvested directly from **[Coworker.com](https://www.coworker.com)**, the industry-standard global directory for flexible workspaces.

* **Target Harvesting:** XML sitemaps (`sitemap_urls.txt`) and directory endpoints covering 3,300+ cities across 190+ countries were crawled.
* **Scraping Architecture:** Developed in Python utilizing `curl_cffi` (impersonating browser TLS fingerprints to manage rate limiting) and `BeautifulSoup4` for resilient DOM parsing.
* **Persistence & Checkpointing:** Raw HTTP responses were staged into a transactional SQLite database (`coworker_scrape.db`) with crash recovery queues.
* **Raw Dataset (`data/coworking_dataset_full.csv`):** **26,965 total listings** across 190+ countries.
* **Cleaned Analytical Dataset (`data/coworking_dataset_clean.csv`):** **13,882 verified spaces** across 100+ countries.
  * *Filtering rationale:* 13,083 incomplete records (spaces lacking published rates or dormant profile pages) were removed.
  * *Imputation & Feature Engineering:* Country-level median imputation was applied for missing seating capacity (31.3%). Raw amenity JSON strings were parsed into 16 standardized boolean feature flags, and composite domain indices (`business_infra_idx`, `community_idx`, `ergonomic_comfort_idx`) were constructed.

---

## 4. Analytics Methods Used

The study directly implements quantitative methodologies mapped to the **Business Analytics Syllabus**:

```
Syllabus Unit 1: Data Exploration, Dimension Reduction & Classifier Evaluation
Syllabus Unit 2: Multiple Linear Regression, Ensembles, Logistic Regression, Cluster Analysis (k-Means)
Syllabus Unit 3: Text Mining, Document Preprocessing & Bag-of-Words Feature Extraction
```

### 4.1 Multiple Linear Regression (Hedonic Price Modeling)
* **Method:** Log-linear Ordinary Least Squares (OLS) regression modeling $\ln(\text{Price}_i)$ against capacity, 16 amenity indicators, and country fixed effects:
  $$\ln(\text{Price}_i) = \beta_0 + \beta_1 \cdot \text{Capacity}_i + \sum_{k} \beta_k \cdot \text{Amenity}_{k,i} + \sum_{j} \gamma_j \cdot \text{Country}_{j,i} + \varepsilon_i$$
* **Benchmarking:** Benchmarked against L2 Ridge Regularization and Random Forest Regression (*Unit 2: Combining Methods & Ensembles*).
* **Metric:** Evaluated via $R^2$, Adjusted $R^2$, RMSE, and MAE.

### 4.2 Customer Satisfaction Classification & Driver Analytics
* **Method:** Formulated as a binary classification task to address platform rating skewness ($\text{High Satisfaction} = 1$ if $\text{Happiness Score} \ge 4.5$, else $0$).
* **Algorithms:**
  1. *Logistic Regression:* Estimated log-odds and odds ratios for operational factors.
  2. *Random Forest Classifier (150 estimators):* Modeled non-linear feature interactions and quantified Gini impurity importance.
* **Metric & Diagnostics:** Evaluated using Accuracy, Precision, Recall, Macro F1-Score, ROC Curves (with Youden's $J$ cutoff), Precision-Recall curves, and normalized confusion matrices.

### 4.3 Unsupervised Market Segmentation ($k$-Means Clustering)
* **Method:** Standardized continuous features using Z-score normalization and partitioned spaces using Euclidean distance-based $k$-Means.
* **Validation:** Optimal cluster count ($k=3$) validated through Silhouette Score analysis ($S = 0.312$ across $k \in [2, 8]$), Elbow WCSS curve, and within-cluster silhouette profile diagrams.

---

## 5. Key Results & Findings

### 5.1 Hedonic Pricing Premiums (Marginal Willingness-to-Pay)
* **Transit Proximity (5-min walk):** $+33.8\%$ price premium ($p < 0.0001, t = 8.25$)
* **Lounge / Chill-out Area:** $+32.9\%$ price premium ($p < 0.0001, t = 8.12$)
* **24/7 Member Access:** $+25.1\%$ price premium ($p < 0.0001, t = 7.60$)
* **Ergonomic Chairs:** $+16.3\%$ price premium ($p < 0.0001, t = 4.43$)
* **Shared Kitchen:** $+8.0\%$ price premium ($p = 0.0169, t = 2.39$)
* **Baseline Amenities (WiFi, Coffee, AC):** Negative coefficients in log-linear OLS due to market saturation (>70% penetration); they represent non-negotiable hygiene factors rather than premium differentiators.

### 5.2 Satisfaction Driver Analytics
* **Random Forest Performance:** **90.80% Accuracy**, **95.53% Precision**, **94.74% Recall**, and **0.9513 F1-Score** (outperforming Logistic Regression at 71.72% accuracy).
* **Top 5 Satisfaction Drivers (Gini Importance):**
  1. Acoustic Call Privacy (`has_phone_booth`) — Top driver of 5-star ratings.
  2. Verified Review Density (`review_count`) — Community social proof.
  3. Total Amenity Breadth (`total_amenities`).
  4. Seating Capacity Scale (`capacity_imputed`).
  5. Ergonomic Workstations (`has_ergonomic_chairs`).

### 5.3 Identified Market Archetypes ($k=3$ Clusters)
* **Tier 1: Urban Core / Boutique Hubs (46.6% of market):** Premium price (Mean: \$212.36/mo), lean amenity checklist (6.3), focused capacity (24 desks). Monetizes prime transit real estate.
* **Tier 2: Enterprise Mega-Campuses (9.8% of market):** Competitive price (Mean: \$71.96/mo), large capacity (266.7 desks), comprehensive amenities (59.9), high business infrastructure score (3.62 / 4.0).
* **Tier 3: Balanced Value Spaces (43.6% of market):** Accessible price (Mean: \$68.52/mo), moderate capacity (49.4 desks), strong community focus (23.9 amenities).

---

## 6. Comparison with State-of-the-Art Literature

| Published Study | Dataset & Sample Size | Method Used | Key Finding | Comparison with This Study |
| :--- | :--- | :--- | :--- | :--- |
| **Weijs-Perrée et al. (2021)**<br>*J. Corp. Real Estate* | Survey of 291 users in Netherlands | OLS Regression & Structural Equation Modeling (SEM) | Noise levels and social climate drive satisfaction ($R^2 = 0.41$) | Small, localized survey ($N=291$) vs. our global scraped dataset ($N=13,882$). Lacked pricing elasticity and clustering. |
| **Chegut, Eichholtz, & Kok (2020)**<br>*JREFE / MIT Real Estate Lab* | 1,200+ commercial leases in London & NYC | Log-linear Hedonic Pricing (OLS with Fixed Effects) | Flexible offices command 15%–25% rent premiums ($R^2 = 0.58$) | Evaluated institutional landlord leases; our work evaluates direct consumer pricing, amenity elasticity, and member satisfaction. |
| **Yang, Becerik-Gerber, & Mino (2023)**<br>*Building & Environment* | Survey of 450 remote workers in US | Random Forest Classifier, Decision Trees, Ordinal Logit | Acoustic privacy and ergonomics explain >40% satisfaction variance | Corroborates our finding that phone booths and ergonomics outweigh social perks; our study expands scope globally and integrates economic valuation. |

---

## 7. Submission Repository Structure

```
├── README.md                      <- Case study summary, objectives, methodology, results & citations
├── data/
│   ├── coworking_dataset_full.csv <- Raw web-scraped dataset (26,965 records)
│   └── coworking_dataset_clean.csv<- Final cleaned, validated & anonymized dataset (13,882 records)
├── analysis.ipynb                 <- Fully executed Jupyter Notebook with code, comments & all outputs
├── Case_Study_Report.pdf          <- Final 8-10 page formal PDF report (prescribed Section A format)
├── figures/                       <- High-resolution publication charts (14 figures)
│   ├── fig1_geographic_distribution.png
│   ├── fig2_price_distribution.png
│   ├── fig3_amenity_penetration.png
│   ├── fig4_correlation_matrix.png
│   ├── fig5_satisfaction_feature_importance.png
│   ├── fig6_market_clusters.png
│   ├── fig_eda_amenity_impact_violin.png
│   ├── fig_eda_geospatial_density.png
│   ├── fig_eda_resource_type_breakdown.png
│   ├── fig_hedonic_coefficients_forest.png
│   ├── fig_kmeans_silhouette_selection.png
│   ├── fig_market_clusters_radar.png
│   ├── fig_roc_curves_confusion.png
│   └── fig_roc_logistic_vs_rf.png
├── generate_notebook.py           <- Automated notebook build script with full documentation
└── run_notebook.py                <- Headless kernel execution script
```

---

## 8. Reproducibility & Environment Setup

To reproduce the analysis locally:

```bash
# 1. Clone your GitHub Classroom repository
git clone <YOUR_CLASSROOM_REPO_URL>
cd <REPO_NAME>

# 2. Set up Python virtual environment (Python 3.10+ recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install required dependencies
pip install numpy pandas scipy scikit-learn matplotlib seaborn statsmodels jupyter

# 4. Launch Jupyter Notebook
jupyter notebook analysis.ipynb
```

All 21 code cells in `analysis.ipynb` are fully self-contained and pre-executed with pre-rendered graphical and tabular outputs.

---

## 9. References

1. **Weijs-Perrée, M., Appel-Meulenbroek, R., & Arentze, T. (2021).** Analysing user satisfaction with coworking spaces: A regression analysis of physical and social aspects. *Journal of Corporate Real Estate*, 23(3), 195–214.
2. **Chegut, A., Eichholtz, P., & Kok, N. (2020).** The price of flexibility: Valuing flexible office space and coworking. *The Journal of Real Estate Finance and Economics*, 61(4), 578–608.
3. **Yang, E., Becerik-Gerber, B., & Mino, L. (2023).** Evaluating remote worker well-being and satisfaction in flexible workspaces: A multi-attribute classification approach. *Building and Environment*, 231, 110034.
4. **Bouncken, R. B., & Reuschl, A. J. (2021).** Coworking-spaces: How a phenomenon of the sharing economy changes innovative ways of working. *Review of Managerial Science*, 15(2), 317–334.
5. **Orel, M. (2019).** Coworking environments and digital nomadism: Balancing work and leisure while on the move. *World Leisure Journal*, 61(3), 215–227.
6. **Coworker.com (2026).** Global Coworking Directory & Review Marketplace. Retrieved from [https://www.coworker.com](https://www.coworker.com).
