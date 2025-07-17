# ORBS7030 Business Statistics with Python: Marking Scheme for Individual Case Study

## Overview
This marking scheme outlines the rubric for the ORBS7030 Individual Case Study (25% of total assessment). Students conduct exploratory data analysis on an assigned dataset and submit a single zipped Jupyter Notebook with code and Markdown cells. The report includes six sections: Introduction (15 marks), Numerical Descriptive Statistics (15 marks), Data Visualization (25 marks), Hypothesis Testing (30 marks), Role of Human and Generative AI (10 marks), and References (5 marks), totaling 100 marks.

## Rubric

### 1. Introduction (15 Marks)
| Criteria | Marks | Description |
|----------|-------|-------------|
| Inclusion of at Least Three Valid Research Questions | 6 | **6 Marks**: Lists ≥3 valid, specific, numbered/bulleted research questions tied to dataset focus (e.g., churn, satisfaction), answerable via analysis, visualization, or testing (e.g., "Does gender show different churn tendencies?"). **4–5 Marks**: 3 questions, but one lacks clarity or alignment. **2–3 Marks**: 1–2 valid questions or vague/misaligned. **0–1 Mark**: No/irrelevant questions. **Common Mistakes**: Vague questions, misalignment (e.g., points vs. churn), unclear listing, data query type of question. |
| Context and Purpose of the Dataset | 5 | **5 Marks**: Explains dataset purpose and relevance, linking to stakeholders (e.g., "Hotel dataset optimizes staffing"). **3–4 Marks**: Some context, lacks depth. **1–2 Marks**: Minimal/vague context. **0 Marks**: No context. **Common Mistakes**: Generic/missing context. |
| Description of Basic Dataset Information | 4 | **4 Marks**: States observations, variable counts/types, missing values (e.g., "100,000 observations, 10 numerical variables"). **2–3 Marks**: Partial information. **0–1 Mark**: Minimal/no description. **Common Mistakes**: Omitting counts, types, or missing values; misinterpreting variables (e.g., room type). |

### 2. Numerical Descriptive Statistics (15 Marks)
| Criteria | Marks | Description |
|----------|-------|-------------|
| Numerical Descriptive Statistics | 15 | **15 Marks**: Comprehensive statistics (mean, median, standard deviation, mode, quartiles) for key variables, tied to 2–3 research questions, clearly presented. Addresses dataset-specific needs (e.g., filtering churned customers). **11–14 Marks**: Misses minor measures or lacks clarity. **6–10 Marks**: Incomplete or unrelated statistics. **0–5 Marks**: Minimal/incorrect statistics. **Common Mistakes**: Missing metrics, no filtering, duplicated statistics， using inappropriate metrics for variable types, such as applying the Pearson correlation coefficient to a continuous variable and a categorical variable, or between two categorical variables, leads to misleading results.|

### 3. Data Visualization (25 Marks)
| Criteria | Marks | Description |
|----------|-------|-------------|
| Chart Type Appropriateness | 8 | **8 Marks**: Uses appropriate chart types for data/purpose (e.g., bar charts for binary variables like cancellation, line graphs for time trends). Aligns with variable types (e.g., bar charts for binary outcomes). **6–7 Marks**: Minor issues (e.g., bar vs. pie for proportions). **3–5 Marks**: Significant issues (e.g., time-based axes for non-temporal relationships). **0–2 Marks**: Inappropriate/missing visualizations. **Common Mistakes**: Scatter plots for distributions, time-based axes for relationships, bar charts for trends. |
| Informativeness and Title Consistency | 7 | **7 Marks**: Informative visualizations address 2–3 research questions, use suitable scales (e.g., log scales). Titles reflect purpose (e.g., "Relationship between ADR and Cancellation Rate" for bar charts). **5–6 Marks**: Minor title misalignment or limited informativeness. **3–4 Marks**: Single-variable focus or misaligned titles. **0–2 Marks**: Not informative, irrelevant titles. **Common Mistakes**: Titles implying relationships but showing trends, single-variable focus, misleading scales. |
| Clarity and Interpretation | 10 | **10 Marks**: Clear visualizations with no overlapping labels, correct axes, accurate legends. Descriptions quantify findings (e.g., tested correlations) and tie to questions. Combine related plots. **7–9 Marks**: Minor clarity issues, less detailed descriptions. **4–6 Marks**: Significant clarity issues (e.g., non-English labels). **0–3 Marks**: Unclear, no interpretations. **Common Mistakes**: Overlapping labels, missing legends, untested claims, regard the horizontal bar in the boxplot as mean, the range of x or y axis is set unreasonable, without proper transformation e.g.log transformation when the scales are so different, mess up box-wisker plot and bar plot, id included in the heatmap. |

### 4. Hypothesis Testing (30 Marks)
| Criteria | Marks | Description |
|----------|-------|-------------|
| Proposal of Relevant Hypothesis Tests | 10 | **10 Marks**: Proposes 2–3 relevant tests tied to dataset and research questions (e.g., z-tests for proportions, t-tests for means). **7–9 Marks**: One test less relevant/inappropriate. **4–6 Marks**: One/irrelevant tests. **0–3 Marks**: No/irrelevant tests. **Common Mistakes**: Fewer than 2 tests, incorrect tests (e.g., t-test for proportions). |
| Clarity of Hypotheses and Test Statistics | 10 | **10 Marks**: States null (H₀) and alternative (H₁) hypotheses with correct notation (e.g., p for proportions, μ for means). Null includes equal sign (e.g., μ₀ = μ, μ₀ ≤ μ), alternative excludes it (e.g., μ ≠ μ₀, μ > μ₀). Specifies test statistic, formula, preliminary tests (e.g., Levene’s), sample statistics. **7–9 Marks**: Minor notation errors (e.g., equal sign in alternative). **4–6 Marks**: Unclear/reversed hypotheses, incorrect notation. **0–3 Marks**: Missing/incorrect hypotheses. **Common Mistakes**: Equal sign in alternative, reversed hypotheses, no Levene’s test, missing 'alternative' parameter for one-sided test. |
| Results and Conclusions | 10 | **10 Marks**: Accurate results (test statistic, p-value) using scipy.stats. Conclusions state reject/fail to reject H₀ at α = 0.05, interpret findings, adjust for multiple testing. **7–9 Marks**: Minor errors, incomplete conclusions. **4–6 Marks**: Significant errors (e.g., NaNs). **0–3 Marks**: Missing/uninterpretable results. **Common Mistakes**: No multiple test adjustment, misinterpreting p-values, model fitting issues. |

### 5. Role of Human and Generative AI (10 Marks)
| Criteria | Marks | Description |
|----------|-------|-------------|
| Authenticity and Word Count | 6 | **6 Marks**: Student-written reflection ≥150 words, no plagiarism/AI-generated text. **4–5 Marks**: Meets 150 words, minor generic phrasing. **2–3 Marks**: 100–149 words or moderate external influence. **0–1 Mark**: <100 words, AI-generated, or missing. **Common Mistakes**: Missing reflections, unmet word count. |
| Content and Reflection Quality | 4 | **4 Marks**: Discusses student/AI roles, opportunities (e.g., code debugging), challenges (e.g., interpreting outputs) in project or studies. **3 Marks**: Lacks specific examples. **1–2 Marks**: Vague/partial reflection. **0 Marks**: Irrelevant/missing. **Common Mistakes**: Generic reflections, not project-specific. |

### 6. References (5 Marks)
| Criteria | Marks | Description |
|----------|-------|-------------|
| Presence and Appropriateness of References | 5 | **5 Marks**: Lists ≥1 relevant reference (e.g., Kaggle, textbook) clearly presented, no plagiarism. **3–4 Marks**: Marginally relevant or minor formatting issues. **1–2 Marks**: Incomplete/irrelevant references. **0 Marks**: No/plagiarized references. **Common Mistakes**: Missing references, irrelevant citations. |

## Common Observations Across Sections
- **Completeness**: Missing sections (e.g., References, AI reflection) or unmet word counts noted.
- **Clarity and Structure**: Most reports praised for clarity, but some lacked explicit question listing or hypothesis clarity.
- **Relevance**: Misalignment with dataset focus (e.g., points vs. churn) in Introduction and Hypothesis Testing.
- **Statistical Rigor**: Inappropriate chart types (e.g., time-based axes for relationships), missing preliminary tests (e.g., Levene’s), untested visualization claims, incorrect hypothesis notation.
- **Plagiarism and Authenticity**: Strict prohibition on plagiarism requires student-written reflections and cited references.

## Notes for Evaluators
- **File Naming**: Deduct 20 marks for incorrect naming (e.g., not "StudentNumber_Name_Major").
- **Plagiarism**: Any plagiarism results in 0 marks.
- **Jupyter Notebook**: Submission must be a single zipped Jupyter Notebook.
- **Encouragement**: Focus on effort and completeness, addressing specific errors.
- **Visualization Titles**: Ensure titles match chart purpose (e.g., relationship-focused titles use bar charts for binary variables).
- **Hypothesis Notation**: Null hypotheses include equal sign (e.g., μ₀ = μ, μ₀ ≤ μ), alternative excludes it (e.g., μ ≠ μ₀).