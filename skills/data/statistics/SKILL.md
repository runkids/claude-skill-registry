---
name: statistics
description: Statistical analysis methods, hypothesis testing, and probability for data analytics
version: "2.0.0"
sasmp_version: "2.0.0"
bonded_agent: 03-statistical-analysis-expert
bond_type: PRIMARY_BOND

# Skill Configuration
config:
  atomic: true
  retry_enabled: true
  max_retries: 3
  backoff_strategy: exponential
  numerical_precision: high

# Parameter Validation
parameters:
  skill_level:
    type: string
    required: true
    enum: [beginner, intermediate, advanced]
    default: beginner
  focus_area:
    type: string
    required: false
    enum: [descriptive, inferential, probability, regression, experiments, all]
    default: all
  tool_preference:
    type: string
    required: false
    enum: [python, r, excel, all]
    default: python

# Observability
observability:
  logging_level: info
  metrics: [calculation_accuracy, test_validity, model_fit]
---

# Statistics Skill

## Overview
Master statistical concepts and methods essential for data analysis, from descriptive statistics to advanced inferential techniques.

## Core Topics

### Descriptive Statistics
- Measures of central tendency (mean, median, mode)
- Measures of dispersion (variance, standard deviation, IQR)
- Data distributions and skewness
- Percentiles and quartiles

### Inferential Statistics
- Sampling methods and sample size determination
- Confidence intervals
- Hypothesis testing (t-tests, chi-square, ANOVA)
- P-values and statistical significance

### Probability
- Basic probability rules
- Probability distributions (normal, binomial, Poisson)
- Bayes' theorem
- Expected value and variance

### Regression Analysis
- Linear regression
- Multiple regression
- Logistic regression
- Model validation and diagnostics

## Learning Objectives
- Apply descriptive statistics to summarize data
- Conduct hypothesis tests for business decisions
- Build and interpret regression models
- Communicate statistical findings effectively

## Error Handling

| Error Type | Cause | Recovery |
|------------|-------|----------|
| Sample too small | Insufficient data | Increase sample or use bootstrap |
| Assumption violated | Data doesn't fit test | Use non-parametric alternative |
| Multicollinearity | Correlated predictors | Remove or combine variables |
| Outliers | Extreme values | Investigate or use robust methods |
| P-hacking | Multiple testing | Apply Bonferroni correction |

## Related Skills
- programming (for implementing statistical models)
- visualization (for presenting statistical insights)
- advanced (for machine learning)
