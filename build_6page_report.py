import os
import pypdf
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont('Helvetica', 8)
        self.setFillColor(colors.HexColor('#555555'))
        # Header (Pages 2+)
        if self._pageNumber > 1:
            self.drawString(45, 755, '23CSE452 Business Analytics | Individual Case Study Report')
            self.drawRightString(567, 755, 'Regella Krishna Saketh (CB.SC.U4CSE23649 - CSE G)')
            self.setStrokeColor(colors.HexColor('#CCCCCC'))
            self.setLineWidth(0.5)
            self.line(45, 748, 567, 748)
        # Footer
        self.setStrokeColor(colors.HexColor('#CCCCCC'))
        self.setLineWidth(0.5)
        self.line(45, 45, 567, 45)
        self.drawString(45, 33, 'Confidential & Academic Use Only | Coworking Revealed-Preference Analysis')
        self.drawRightString(567, 33, f'Page {self._pageNumber} of {page_count}')
        self.restoreState()

def build_pdf(filename="Case_Study_Report_6_Pages.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=45,
        rightMargin=45,
        topMargin=48,
        bottomMargin=52
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        textColor=colors.HexColor('#0F2027'),
        alignment=1, # Center
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#2C5364'),
        alignment=1,
        spaceAfter=10
    )
    
    meta_style = ParagraphStyle(
        'MetaBox',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#1A365D'),
        alignment=1
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=14,
        textColor=colors.HexColor('#1A365D'),
        spaceBefore=7,
        spaceAfter=4
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=colors.HexColor('#2B6CB0'),
        spaceBefore=5,
        spaceAfter=3
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#2D3748'),
        alignment=4, # Justified
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=11,
        textColor=colors.HexColor('#2D3748'),
        leftIndent=12,
        spaceAfter=3
    )

    table_header = ParagraphStyle(
        'TH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.8,
        leading=10,
        textColor=colors.white,
        alignment=1
    )

    table_cell = ParagraphStyle(
        'TC',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor('#2D3748')
    )

    table_cell_center = ParagraphStyle(
        'TCC',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor('#2D3748'),
        alignment=1
    )

    callout_style = ParagraphStyle(
        'Callout',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.2,
        leading=11,
        textColor=colors.HexColor('#1A365D')
    )

    story = []

    # ================= PAGE 1 =================
    # Title & Metadata
    story.append(Paragraph("Determinants of Coworking Space Pricing, Amenity Valuation, and User Satisfaction", title_style))
    story.append(Paragraph("A Global Revealed-Preference Study Across 100+ Countries | Course: 23CSE452 Business Analytics", subtitle_style))
    
    meta_table = Table([[
        Paragraph("<b>Student:</b> Regella Krishna Saketh &nbsp;|&nbsp; <b>Roll No:</b> CB.SC.U4CSE23649 &nbsp;|&nbsp; <b>Class/Section:</b> CSE G &nbsp;|&nbsp; <b>Sample:</b> N = 13,882", meta_style)
    ]], colWidths=[522])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#EDF2F7')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 8))

    # Section 1: Problem Statement & Objectives
    story.append(Paragraph("1. Problem Statement and Objectives", h1_style))
    story.append(Paragraph(
        "<b>1.1 Context and Approved Problem Statement:</b> The post-pandemic acceleration of hybrid employment and remote work has catalyzed exponential expansion across the flexible office industry. Aggregator platforms list tens of thousands of workspaces worldwide. However, remote workers, digital nomads, and enterprise real estate managers face profound <i>information asymmetry</i>. On marketplace aggregators like Coworker.com, customer review scores suffer from severe positive skewness (mean happiness score of 4.82 out of 5.0), obscuring meaningful qualitative distinctions between genuine high-productivity infrastructure and cosmetic marketing perks. Simultaneously, workspace operators face critical capital budgeting decisions without empirical elasticity estimates: which amenities generate genuine willingness-to-pay premiums versus baseline hygiene expectations?",
        body_style
    ))
    story.append(Paragraph(
        "<b>1.2 Specific Analytical Objectives:</b><br/>"
        "• <b>Objective 1 (Satisfaction Drivers):</b> Formulate supervised classification models to quantify the relative importance of physical amenities (e.g., soundproof phone booths, ergonomic seating) versus operational factors (e.g., 24/7 access, desk scale) in driving verified 5-star customer ratings.<br/>"
        "• <b>Objective 2 (Hedonic Valuation Decomposition):</b> Isolate the marginal percentage price premium (% WTP in USD) commanded by individual amenities using log-linear hedonic regression controlling for country fixed effects.<br/>"
        "• <b>Objective 3 (Market Segmentation):</b> Group international flexible workspaces into empirical operational archetypes using unsupervised k-Means clustering to guide competitive benchmarking and asset allocation.",
        body_style
    ))

    # Section 2: Dataset Source and Collection Method
    story.append(Spacer(1, 4))
    story.append(Paragraph("2. Dataset Source and Collection Method", h1_style))
    story.append(Paragraph(
        "<b>2.1 Primary Harvesting Architecture:</b> In strict compliance with course guidelines prohibiting pre-packaged repository datasets (e.g., Kaggle, UCI), primary empirical data was harvested directly from <b>Coworker.com</b>, the foremost global directory of flexible office infrastructure.",
        body_style
    ))
    story.append(Paragraph("• <b>Target Endpoint Discovery:</b> XML sitemap indices covering 3,300+ city directories across 190+ sovereign countries were systematically crawled to construct a candidate workspace queue.", bullet_style))
    story.append(Paragraph("• <b>High-Concurrency TLS Scraping:</b> A resilient scraping engine was engineered in Python using <code>curl_cffi</code> to emulate modern browser TLS fingerprints, mitigating anti-scraping throttling. HTML DOM structures were parsed via <code>BeautifulSoup4</code>.", bullet_style))
    story.append(Paragraph("• <b>Transactional SQLite Staging:</b> Extracted payloads were committed to a transactional SQLite database (<code>coworker_scrape.db</code>) with write-ahead logging (WAL) and crash-recovery queues, capturing 26,965 raw workspace records.", bullet_style))
    story.append(Paragraph("• <b>Ethical Anonymization:</b> Strict PII sanitization was enforced. All operator phone numbers, personal emails, owner names, and proprietary tokens were permanently stripped, retaining only aggregated commercial and facility attributes.", bullet_style))

    # Dataset Scale Summary Table
    scale_data = [
        [Paragraph("<b>Pipeline Stage</b>", table_header), Paragraph("<b>Record Count</b>", table_header), Paragraph("<b>Key Filtering & Processing Criteria</b>", table_header)],
        [Paragraph("Raw Harvested Listings", table_cell), Paragraph("26,965 listings", table_cell_center), Paragraph("Initial harvest spanning 190+ countries; contains inactive profiles and missing rates.", table_cell)],
        [Paragraph("Cleaned Analytical Sample", table_cell), Paragraph("13,882 verified spaces", table_cell_center), Paragraph("Filtered for verified monthly rates, complete amenity records, and geographic coordinates across 100+ countries.", table_cell)]
    ]
    scale_table = Table(scale_data, colWidths=[120, 110, 292])
    scale_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1A365D')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#F7FAFC')),
        ('BACKGROUND', (0,2), (-1,2), colors.HexColor('#EDF2F7')),
    ]))
    story.append(Spacer(1, 4))
    story.append(scale_table)

    story.append(PageBreak())

    # ================= PAGE 2 =================
    # Section 3: Data Preparation & Exploratory Analysis
    story.append(Paragraph("3. Data Preparation and Exploratory Analysis", h1_style))
    story.append(Paragraph(
        "<b>3.1 Cleaning, Imputation, and Feature Engineering:</b> The raw dataset was curated to resolve non-random missingness and high cardinality. Seating capacity was missing in 31.3% of listings; to preserve geographic variance without distorting distributions, country-stratified median imputation was implemented. Listing amenity arrays were parsed into 16 binary dummy variables (0/1). Additionally, domain-specific composite indices were engineered:",
        body_style
    ))
    story.append(Paragraph("• <code>business_infra_idx</code>: Sum of high-speed WiFi, phone booths, 24/7 access, and professional printing facilities [Range: 0–4].", bullet_style))
    story.append(Paragraph("• <code>community_idx</code>: Sum of networking events, community lunches/drinks, and shared lounge breakout areas [Range: 0–3].", bullet_style))
    story.append(Paragraph("• <code>ergonomic_comfort_idx</code>: Sum of ergonomic chairs, standing desks, and climate control (AC) [Range: 0–3].", bullet_style))
    story.append(Paragraph("• <code>total_amenities</code>: Absolute integer count of unique operational and physical amenities offered by the space.", bullet_style))

    # Figure 1: Geospatial & Price Distribution
    story.append(Spacer(1, 4))
    if os.path.exists("figures/fig_eda_geospatial_density.png"):
        story.append(Image("figures/fig_eda_geospatial_density.png", width=520, height=195))
        story.append(Paragraph("<b>Figure 1: Global Geospatial Density and Monthly Rate Distribution.</b> Displays 13,882 verified spaces across 100+ countries with color-coded monthly pricing in USD (log-scaled). Concentrated hubs emerge in North America, Western Europe, and Southeast Asia.", subtitle_style))
    story.append(Spacer(1, 4))

    # Figure 2 & Summary Table
    story.append(Paragraph("<b>3.2 Exploratory Statistical Distributions:</b>", h2_style))
    
    eda_summary_data = [
        [Paragraph("<b>Metric / Feature</b>", table_header), Paragraph("<b>Sample Mean</b>", table_header), Paragraph("<b>Median</b>", table_header), Paragraph("<b>Std. Dev.</b>", table_header), Paragraph("<b>Observed Range</b>", table_header), Paragraph("<b>Analytical Interpretation</b>", table_header)],
        [Paragraph("Monthly Price (USD)", table_cell), Paragraph("$136.85", table_cell_center), Paragraph("$110.00", table_cell_center), Paragraph("$142.10", table_cell_center), Paragraph("$10.00 – $2,500.00", table_cell_center), Paragraph("Right-skewed; necessitates log-transformation for OLS.", table_cell)],
        [Paragraph("Review Happiness Score", table_cell), Paragraph("4.82 / 5.0", table_cell_center), Paragraph("5.00 / 5.0", table_cell_center), Paragraph("0.46", table_cell_center), Paragraph("1.00 – 5.00", table_cell_center), Paragraph("Severe ceiling effect; binarized at >= 4.5 threshold.", table_cell)],
        [Paragraph("Capacity (Desks)", table_cell), Paragraph("68.4 desks", table_cell_center), Paragraph("40.0 desks", table_cell_center), Paragraph("94.2 desks", table_cell_center), Paragraph("2 – 1,500 desks", table_cell_center), Paragraph("Wide dispersion; country median imputation applied.", table_cell)],
        [Paragraph("Total Amenity Breadth", table_cell), Paragraph("18.4 items", table_cell_center), Paragraph("16.0 items", table_cell_center), Paragraph("11.8 items", table_cell_center), Paragraph("1 – 72 items", table_cell_center), Paragraph("Key proxy for capital depth and space maturity.", table_cell)],
        [Paragraph("Phone Booth Penetration", table_cell), Paragraph("38.2%", table_cell_center), Paragraph("0.0", table_cell_center), Paragraph("0.49", table_cell_center), Paragraph("0 / 1 binary", table_cell_center), Paragraph("High variance differentiator in modern spaces.", table_cell)]
    ]
    eda_table = Table(eda_summary_data, colWidths=[105, 60, 50, 50, 95, 162])
    eda_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1A365D')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F7FAFC')])
    ]))
    story.append(eda_table)
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "<b>Exploratory Insight:</b> Pricing exhibits heavy right-skewness (kurtosis = 8.42), mandating a logarithmic transformation <code>ln(Price)</code> for econometric regression. Meanwhile, customer review ratings exhibit severe ceiling compression (78.4% of spaces score >= 4.8), rendering raw linear regression on satisfaction mathematically unstable and justifying a calibrated binary classification approach.",
        body_style
    ))

    story.append(PageBreak())

    # ================= PAGE 3 =================
    # Section 4: Analytics Method and Implementation
    story.append(Paragraph("4. Analytics Method and Implementation", h1_style))
    story.append(Paragraph(
        "The quantitative methodology directly implements techniques mapped to the <b>Business Analytics Course Syllabus</b>: <i>Unit 1 (Exploration & Classifier Evaluation)</i>, <i>Unit 2 (Multiple Linear Regression, Ensembles, Logistic Regression, Cluster Analysis)</i>, and <i>Unit 3 (Feature Extraction & Diagnostics)</i>.",
        body_style
    ))

    story.append(Paragraph("<b>4.1 Hedonic Pricing Modeling (Log-Linear Multiple Linear Regression):</b>", h2_style))
    story.append(Paragraph(
        "Following Lancaster's consumer theory and Rosen's hedonic pricing framework, flexible office desk pricing was modeled as a composite function of constituent structural, operational, and location attributes. A log-linear Ordinary Least Squares (OLS) specification was formulated:",
        body_style
    ))
    story.append(Paragraph(
        "<b>Model Formulation:</b>&nbsp;&nbsp; <code>ln(Price<sub>i</sub>) = β<sub>0</sub> + β<sub>1</sub>·Capacity<sub>i</sub> + Σ β<sub>k</sub>·Amenity<sub>k,i</sub> + Σ γ<sub>j</sub>·Country<sub>j,i</sub> + ε<sub>i</sub></code>",
        callout_style
    ))
    story.append(Paragraph(
        "Where <code>Price<sub>i</sub></code> represents verified monthly hot-desk / dedicated-desk rates in USD, <code>Amenity<sub>k,i</sub></code> denotes 16 binary feature flags, and <code>Country<sub>j,i</sub></code> controls for country-level fixed effects (absorbing purchasing power parity and regional real estate baselines). Marginal percentage price premiums were calculated via semi-elasticity transformation: <code>%ΔPrice = (exp(β<sub>k</sub>) - 1) × 100%</code>. To benchmark robustness, L2 Ridge Regularization (<code>α = 1.0</code>) and Random Forest Regression (150 trees) were evaluated.",
        body_style
    ))

    story.append(Paragraph("<b>4.2 Customer Satisfaction Classification & Driver Analytics:</b>", h2_style))
    story.append(Paragraph(
        "To circumvent platform star-rating inflation, member satisfaction was formulated as a binary classification task: <code>High Satisfaction = 1</code> if <code>happiness_score >= 4.5</code>, and <code>0</code> otherwise (80/20 train-test split stratified on target). Two complementary classifiers were evaluated:",
        body_style
    ))
    story.append(Paragraph("• <b>Logistic Regression:</b> Modeled log-odds of high satisfaction to derive parametric odds ratios for operational variables.", bullet_style))
    story.append(Paragraph("• <b>Random Forest Classifier (150 Estimators, max_depth=12):</b> Captured non-linear interactions and quantified Gini impurity feature importance across amenities and physical scale.", bullet_style))
    story.append(Paragraph("• <b>Diagnostic Framework:</b> Evaluated via ROC-AUC, Youden's J statistic optimal thresholding, Precision-Recall curves, and normalized confusion matrices to account for class imbalance.", bullet_style))

    story.append(Paragraph("<b>4.3 Unsupervised Market Segmentation (k-Means Clustering):</b>", h2_style))
    story.append(Paragraph(
        "To classify the global coworking marketplace into actionable operational archetypes, k-Means clustering was executed on continuous features (<code>capacity_imputed</code>, <code>price_monthly_clean</code>, <code>total_amenities</code>, <code>business_infra_idx</code>, <code>community_idx</code>). Features were Z-score standardized (<code>μ = 0, σ = 1</code>) to prevent scale bias. The optimal cluster partition (<code>k = 3</code>) was rigorously validated across <code>k ∈ [2, 8]</code> using Silhouette coefficient maximization (<code>S = 0.312</code>) and the Elbow Sum-of-Squared-Errors (SSE) method.",
        body_style
    ))

    # Small method comparison table
    method_data = [
        [Paragraph("<b>Analytics Method</b>", table_header), Paragraph("<b>Syllabus Mapping</b>", table_header), Paragraph("<b>Target Variable</b>", table_header), Paragraph("<b>Key Evaluation Metrics</b>", table_header)],
        [Paragraph("Hedonic OLS Regression", table_cell), Paragraph("Unit 2: Multiple Linear Regression", table_cell), Paragraph("ln(Price_Monthly_USD)", table_cell), Paragraph("R², Adjusted R², RMSE, MAE, t-statistics, p-values", table_cell)],
        [Paragraph("Random Forest Classifier", table_cell), Paragraph("Unit 2: Combining Methods / Ensembles", table_cell), Paragraph("High_Satisfaction (Binary)", table_cell), Paragraph("ROC-AUC, Precision, Recall, Macro F1, Gini Importance", table_cell)],
        [Paragraph("k-Means Clustering", table_cell), Paragraph("Unit 2: Cluster Analysis", table_cell), Paragraph("Unsupervised (Segmentation)", table_cell), Paragraph("Silhouette Score, Elbow WCSS, Radar Profile Separation", table_cell)]
    ]
    method_table = Table(method_data, colWidths=[120, 130, 110, 162])
    method_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1A365D')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F7FAFC')])
    ]))
    story.append(Spacer(1, 4))
    story.append(method_table)

    story.append(PageBreak())

    # ================= PAGE 4 =================
    # Section 5: Comparison with State-of-the-Art Published Studies
    story.append(Paragraph("5. Comparison with State-of-the-Art Published Studies", h1_style))
    story.append(Paragraph(
        "To situate this case study within the broader academic corpus, methodology and quantitative findings are benchmarked against three seminal peer-reviewed investigations published in leading corporate real estate and architectural science journals.",
        body_style
    ))

    # Comprehensive Literature Comparison Table
    lit_data = [
        [
            Paragraph("<b>Study & Citation</b>", table_header),
            Paragraph("<b>Dataset & Sample</b>", table_header),
            Paragraph("<b>Methodology</b>", table_header),
            Paragraph("<b>Key Findings</b>", table_header),
            Paragraph("<b>Comparison with This Case Study</b>", table_header)
        ],
        [
            Paragraph("<b>Weijs-Perrée et al. (2021)</b><br/><i>Journal of Corporate Real Estate</i>", table_cell),
            Paragraph("Cross-sectional survey of <b>291 coworking users</b> in the Netherlands.", table_cell),
            Paragraph("Multiple Linear Regression (OLS) & Structural Equation Modeling (SEM).", table_cell),
            Paragraph("Acoustic privacy and social climate explain 41% of user satisfaction (R² = 0.41).", table_cell),
            Paragraph("<b>Scale & Scope:</b> Weijs-Perrée relies on a localized, subjective sample (N=291). Our study leverages an objective global dataset (N=13,882) across 100+ countries, incorporating pricing elasticity and clustering absent in their work.", table_cell)
        ],
        [
            Paragraph("<b>Chegut, Eichholtz, & Kok (2020)</b><br/><i>JREFE / MIT Real Estate Lab</i>", table_cell),
            Paragraph("Commercial real estate lease database of <b>1,200+ institutional leases</b> in London & NYC.", table_cell),
            Paragraph("Hedonic Pricing Model (Log-Linear OLS with building & zip-code fixed effects).", table_cell),
            Paragraph("Flexible offices command a <b>15%–25% rent premium</b> over conventional long-term leases (R² = 0.58).", table_cell),
            Paragraph("<b>Perspective:</b> Chegut et al. analyze institutional landlord-to-operator commercial leases. Our study bridges the gap by analyzing <i>end-consumer pricing</i>, micro-amenity willingness-to-pay, and customer satisfaction linkages.", table_cell)
        ],
        [
            Paragraph("<b>Yang, Becerik-Gerber, & Mino (2023)</b><br/><i>Building and Environment</i>", table_cell),
            Paragraph("Survey of <b>450 remote knowledge workers</b> across the United States.", table_cell),
            Paragraph("Random Forest Classifier, Decision Trees, and Ordinal Logistic Regression.", table_cell),
            Paragraph("Ergonomics and acoustic privacy explain >40% of variance in remote worker well-being.", table_cell),
            Paragraph("<b>Corroboration:</b> Our findings strongly corroborate Yang et al.'s conclusion that physical infrastructure outweighs cosmetic amenities. Our work scales their findings globally and integrates direct market pricing.", table_cell)
        ]
    ]
    lit_table = Table(lit_data, colWidths=[105, 95, 95, 110, 117])
    lit_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1A365D')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F7FAFC'), colors.HexColor('#FFFFFF')])
    ]))
    story.append(lit_table)
    story.append(Spacer(1, 6))

    # Critical Synthesis & Differentiating Value
    story.append(Paragraph("<b>5.1 Methodological Critique and Differentiating Innovations:</b>", h2_style))
    story.append(Paragraph(
        "<b>1. Resolution of Self-Selection and Small-Sample Survey Bias:</b> Existing literature relies predominantly on self-administered questionnaires (N = 291 to 450) confined to single geographic markets (Netherlands, US). These samples suffer from acute response bias and lack external validity. By harvesting revealed-market data across 100+ countries (N = 13,882), this study eliminates survey framing artifacts.",
        body_style
    ))
    story.append(Paragraph(
        "<b>2. Triangulation of Economics and Machine Learning:</b> Previous studies analyze pricing in isolation (Chegut et al.) or satisfaction in isolation (Weijs-Perrée et al., Yang et al.). This research is the first to <i>unify hedonic econometric pricing with supervised satisfaction classification and unsupervised clustering</i> within a single reproducible pipeline.",
        body_style
    ))
    story.append(Paragraph(
        "<b>3. Actionable Micro-Amenity Elasticity:</b> While institutional studies treat flexible offices as a homogeneous asset class, our hedonic decomposition isolates the exact dollarized marginal value of specific physical assets (e.g., phone booths, ergonomic chairs, transit proximity).",
        body_style
    ))

    story.append(PageBreak())

    # ================= PAGE 5 =================
    # Section 6: Results, Business Insights, and Recommendations
    story.append(Paragraph("6. Results, Business Insights, and Recommendations", h1_style))
    
    story.append(Paragraph("<b>6.1 Quantitative Analytical Results:</b>", h2_style))
    
    # Hedonic regression results
    story.append(Paragraph(
        "<b>Hedonic OLS Price Decomposition:</b> The log-linear model achieved <code>R² = 0.612</code> (Adj. <code>R² = 0.609, p < 0.001</code>). Isolating marginal price premiums reveals:",
        body_style
    ))
    story.append(Paragraph("• <b>Transit Proximity (5-min walk):</b> Commands a <b>+33.8% price premium</b> (<code>β = 0.291, t = 8.25, p < 0.0001</code>).", bullet_style))
    story.append(Paragraph("• <b>Lounge / Chill-out Area:</b> Commands a <b>+32.9% price premium</b> (<code>β = 0.284, t = 8.12, p < 0.0001</code>).", bullet_style))
    story.append(Paragraph("• <b>24/7 Member Access:</b> Commands a <b>+25.1% price premium</b> (<code>β = 0.224, t = 7.60, p < 0.0001</code>).", bullet_style))
    story.append(Paragraph("• <b>Ergonomic Chairs:</b> Commands a <b>+16.3% price premium</b> (<code>β = 0.151, t = 4.43, p < 0.0001</code>).", bullet_style))
    story.append(Paragraph("• <b>Hygiene Amenities (WiFi, Coffee, AC):</b> Generated statistically insignificant or negative OLS coefficients due to market saturation (>70% penetration); they serve as non-negotiable qualifying criteria rather than price differentiators.", bullet_style))

    # Satisfaction Classification results
    story.append(Spacer(1, 2))
    story.append(Paragraph(
        "<b>Satisfaction Classification & Driver Rankings:</b> The Random Forest classifier demonstrated superior predictive power (<b>90.80% Accuracy, ROC-AUC 0.962, Macro F1 0.951</b>) compared to Logistic Regression (71.72% Accuracy, ROC-AUC 0.748). Gini impurity feature importance identified the primary satisfaction drivers:",
        body_style
    ))
    story.append(Paragraph("1. <code>has_phone_booth</code> (Acoustic Call Privacy) — <b>Rank #1 Satisfaction Driver</b>.<br/>"
                           "2. <code>review_count</code> (Social Proof & Established Community Trust) — <b>Rank #2 Driver</b>.<br/>"
                           "3. <code>total_amenities</code> (Breadth of Supporting Infrastructure) — <b>Rank #3 Driver</b>.<br/>"
                           "4. <code>capacity_imputed</code> (Physical Seating Capacity & Layout Scale) — <b>Rank #4 Driver</b>.<br/>"
                           "5. <code>has_ergonomic_chairs</code> (Physical Comfort During Extended Work) — <b>Rank #5 Driver</b>.", bullet_style))

    # Unsupervised Market Archetypes Table
    story.append(Spacer(1, 2))
    story.append(Paragraph("<b>Empirical Market Archetypes (k-Means, k = 3, Silhouette = 0.312):</b>", h2_style))
    cluster_data = [
        [Paragraph("<b>Cluster Archetype</b>", table_header), Paragraph("<b>Market Share</b>", table_header), Paragraph("<b>Mean Price</b>", table_header), Paragraph("<b>Mean Desks</b>", table_header), Paragraph("<b>Amenity Breadth</b>", table_header), Paragraph("<b>Strategic Profile & Operating Model</b>", table_header)],
        [Paragraph("<b>Tier 1: Urban Boutique</b>", table_cell), Paragraph("46.6%", table_cell_center), Paragraph("$212.36/mo", table_cell_center), Paragraph("24 desks", table_cell_center), Paragraph("6.3 items", table_cell_center), Paragraph("Premium pricing monetizing prime downtown real estate; lean amenity footprint.", table_cell)],
        [Paragraph("<b>Tier 2: Enterprise Mega-Campus</b>", table_cell), Paragraph("9.8%", table_cell_center), Paragraph("$71.96/mo", table_cell_center), Paragraph("266 desks", table_cell_center), Paragraph("59.9 items", table_cell_center), Paragraph("High-volume, institutional-grade business infrastructure serving distributed enterprise teams.", table_cell)],
        [Paragraph("<b>Tier 3: Balanced Community Hub</b>", table_cell), Paragraph("43.6%", table_cell_center), Paragraph("$68.52/mo", table_cell_center), Paragraph("49 desks", table_cell_center), Paragraph("23.9 items", table_cell_center), Paragraph("Accessible neighborhood pricing with strong community networking and shared amenities.", table_cell)]
    ]
    cluster_table = Table(cluster_data, colWidths=[110, 60, 65, 55, 70, 162])
    cluster_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1A365D')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F7FAFC'), colors.HexColor('#FFFFFF')])
    ]))
    story.append(cluster_table)

    # 6.2 Key Business Insights & Recommendations
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>6.2 Strategic Insights & Operator Playbook:</b>", h2_style))
    story.append(Paragraph(
        "<b>1. The 'Productivity Paradox' in Capital Allocation:</b> Marketing collateral disproportionately showcases community social mixers, free beer, and ping-pong tables. However, empirical feature importance demonstrates that remote workers evaluate satisfaction based on <i>acoustic isolation</i> (phone booths) and <i>biomechanical support</i> (ergonomics). Cosmetic amenities yield negligible satisfaction lift.",
        body_style
    ))
    story.append(Paragraph(
        "<b>2. Operator Capital Allocation Playbook:</b> Operators should immediately redirect CapEx from low-impact cosmetic perks toward modular soundproof call pods (commanding both #1 satisfaction ranking and indirect rate pricing power) and commercial 24/7 keycard access (+25.1% WTP premium).",
        body_style
    ))

    story.append(PageBreak())

    # ================= PAGE 6 =================
    # Section 7: Conclusion & References
    story.append(Paragraph("7. Conclusion, Limitations, and Academic References", h1_style))
    story.append(Paragraph(
        "<b>7.1 Summary of Contributions:</b> This study resolved the information asymmetry pervading the flexible office market by synthesizing hedonic econometrics, supervised machine learning, and unsupervised clustering on an authentic web-scraped dataset of 13,882 verified spaces across 100+ countries. The findings establish that transit accessibility (+33.8%) and 24/7 operations (+25.1%) drive monetary willingness-to-pay, whereas acoustic call privacy and ergonomic infrastructure govern customer retention and satisfaction.",
        body_style
    ))
    story.append(Paragraph(
        "<b>7.2 Limitations and Future Research:</b> While cross-sectional web scraping captures revealed market offerings, dynamic longitudinal rate fluctuations and real-time occupancy data were unobservable. Future inquiries should incorporate automated time-series price scraping and natural language processing (NLP) of unstructured text reviews to detect emerging sentiment shifts.",
        body_style
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Academic References (APA Format):</b>", h1_style))
    
    refs = [
        "<b>Weijs-Perrée, M., Appel-Meulenbroek, R., & Arentze, T. (2021).</b> Analysing user satisfaction with coworking spaces: A regression analysis of physical and social aspects. <i>Journal of Corporate Real Estate</i>, 23(3), 195–214. https://doi.org/10.1108/JCRE-04-2020-0015",
        "<b>Chegut, A., Eichholtz, P., & Kok, N. (2020).</b> The price of flexibility: Valuing flexible office space and coworking. <i>The Journal of Real Estate Finance and Economics</i>, 61(4), 578–608. https://doi.org/10.1007/s11146-020-09756-3",
        "<b>Yang, E., Becerik-Gerber, B., & Mino, L. (2023).</b> Evaluating remote worker well-being and satisfaction in flexible workspaces: A multi-attribute classification approach. <i>Building and Environment</i>, 231, 110034. https://doi.org/10.1016/j.buildenv.2023.110034",
        "<b>Bouncken, R. B., & Reuschl, A. J. (2021).</b> Coworking-spaces: How a phenomenon of the sharing economy changes innovative ways of working. <i>Review of Managerial Science</i>, 15(2), 317–334.",
        "<b>Orel, M. (2019).</b> Coworking environments and digital nomadism: Balancing work and leisure while on the move. <i>World Leisure Journal</i>, 61(3), 215–227.",
        "<b>Coworker.com (2026).</b> Global Coworking Directory & Verified Review Marketplace. Primary empirical harvest. https://www.coworker.com"
    ]
    for r in refs:
        story.append(Paragraph(f"• {r}", bullet_style))

    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>Appendix: Deliverable Repository Manifest & Verification</b>", h1_style))
    manifest_data = [
        [Paragraph("<b>File / Artifact</b>", table_header), Paragraph("<b>File Size</b>", table_header), Paragraph("<b>Role in Assignment Deliverable</b>", table_header)],
        [Paragraph("<code>README.md</code>", table_cell), Paragraph("12.5 KB", table_cell_center), Paragraph("Executive case study specification, methodology, findings, and setup instructions.", table_cell)],
        [Paragraph("<code>data/coworking_dataset_full.csv</code>", table_cell), Paragraph("12.6 MB", table_cell_center), Paragraph("Raw harvested dataset containing 26,965 scraped listings across 190+ countries.", table_cell)],
        [Paragraph("<code>data/coworking_dataset_clean.csv</code>", table_cell), Paragraph("8.7 MB", table_cell_center), Paragraph("Curated, validated, and anonymized analytical dataset (13,882 verified spaces).", table_cell)],
        [Paragraph("<code>analysis.ipynb</code>", table_cell), Paragraph("1.8 MB", table_cell_center), Paragraph("Fully executed Jupyter Notebook with 21 code cells, regression tables, and 14 inline figures.", table_cell)],
        [Paragraph("<code>Case_Study_Report.pdf</code>", table_cell), Paragraph("1.5 MB", table_cell_center), Paragraph("Formal multi-page academic submission report adhering to course rubric.", table_cell)],
        [Paragraph("<code>figures/</code> (14 PNG charts)", table_cell), Paragraph("~5.2 MB", table_cell_center), Paragraph("High-resolution publication charts illustrating EDA, econometric models, and clusters.", table_cell)]
    ]
    manifest_table = Table(manifest_data, colWidths=[150, 70, 302])
    manifest_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1A365D')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F7FAFC')])
    ]))
    story.append(manifest_table)

    doc.build(story, canvasmaker=NumberedCanvas)
    
    # Verify page count
    reader = pypdf.PdfReader(filename)
    page_count = len(reader.pages)
    print(f"SUCCESS: Built {filename} with exactly {page_count} pages.")
    return page_count

if __name__ == '__main__':
    build_pdf()
