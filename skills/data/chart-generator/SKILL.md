---
name: chart-generator
description: Creates text-based visualizations and reports showing the relationship between spelling errors and semantic distance. Use when you need to visualize experimental results.
allowed-tools: Read, Write
---

# Chart Generator Skill

This skill creates text-based visualizations and structured reports for displaying experimental results, particularly for the translation semantic drift experiment.

## Instructions

To generate visualizations:
1. Accept experimental data (typo rates and semantic distances)
2. Use Claude's native text formatting to create visualizations
3. Save reports to markdown or text files
4. Create ASCII art charts if needed

## Visualization Types

### 1. Text-Based Results Table
Tabular display of typo rates vs semantic distances in markdown format.

### 2. ASCII Bar Chart
Simple bar chart representation using text characters.

### 3. Line Chart (for Automated Experiments)
ASCII art line chart showing progression of semantic distance across typo percentages.

### 4. Summary Report
Comprehensive markdown report with analysis and interpretation.

## Implementation

Use Claude's native text processing to:
- Format data into readable tables
- Create ASCII art visualizations
- Generate markdown reports with proper structure
- Add interpretive commentary and insights

## Usage Examples

### Example 1: Single Run Report
For a single sentence experiment, create a concise report with translation chain and distance.

### Example 2: Automated Experiments Chart
Input data:
- Typo rates: [0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50]
- Average distances: [0.45, 0.52, 0.58, 0.63, 0.70, 0.75, 0.81]

Output (markdown table):
```
| Typo Rate | Avg Semantic Distance | Interpretation        |
|-----------|----------------------|-----------------------|
| 20%       | 0.45                 | Moderate drift        |
| 25%       | 0.52                 | Moderate drift        |
| 30%       | 0.58                 | Moderate-high drift   |
| 35%       | 0.63                 | Moderate-high drift   |
| 40%       | 0.70                 | High drift            |
| 45%       | 0.75                 | High drift            |
| 50%       | 0.81                 | Severe drift          |
```

ASCII Line Chart:
```
Average Semantic Distance vs Typo Error Rate

0.90 |
0.80 |                                    ●  (50%)
0.70 |                              ●        (45%)
0.60 |                        ●              (40%)
0.50 |                  ●                    (35%)
0.40 |            ●                          (30%)
0.30 |      ●                                (25%)
0.20 | ●                                     (20%)
0.10 |
     +----+----+----+----+----+----+----+
      20%  25%  30%  35%  40%  45%  50%
                Typo Error Rate
```

ASCII Bar Chart:
```
Average Semantic Distance by Typo Rate
20%  █████████░░░░░░ 0.45
25%  ██████████░░░░░ 0.52
30%  ███████████░░░░ 0.58
35%  ████████████░░░ 0.63
40%  █████████████░░ 0.70
45%  ██████████████░ 0.75
50%  ███████████████ 0.81
```

## Output Format

Save results to markdown files in `results/` directory with:
- Title and timestamp
- Experimental parameters (typo rates, number of sentences, etc.)
- Data tables
- ASCII visualizations (bar charts, line charts)
- Summary statistics
- Interpretation and insights

For automated experiments specifically include:
- Sample sentences with typos at each level
- Average distances per typo percentage
- Trend analysis (linear, exponential, etc.)
- Observations about translation robustness

## Notes

- **NO PYTHON CODE** - Use Claude's native text formatting only
- Save all final results to `results/` directory
- Intermediate working files can go to `tmp/`
- Markdown format for easy viewing and conversion
- Suitable for terminal display and documentation
- Support both single-run reports and automated experiment charts
