---
name: data-analysis
description: Data processing, analysis, and visualization with Python/JavaScript. Use for data exploration, pandas operations, chart generation, and insights extraction.
---

# 📊 Data Analysis Skill

## Python Data Processing

### Pandas Basics
```python
import pandas as pd
import numpy as np

# Read data
df = pd.read_csv('data.csv')
df = pd.read_json('data.json')
df = pd.read_excel('data.xlsx')

# Basic exploration
df.head()        # First 5 rows
df.info()        # Column types
df.describe()    # Statistics
df.shape         # (rows, cols)
```

### Data Cleaning
```python
# Handle missing values
df.dropna()                    # Drop rows with NaN
df.fillna(0)                   # Fill NaN with value
df['col'].fillna(df['col'].mean())  # Fill with mean

# Remove duplicates
df.drop_duplicates()

# Type conversion
df['date'] = pd.to_datetime(df['date'])
df['price'] = df['price'].astype(float)
```

### Aggregations
```python
# Group by
df.groupby('category')['sales'].sum()
df.groupby(['year', 'month']).agg({
    'sales': 'sum',
    'quantity': 'mean',
    'price': ['min', 'max']
})

# Pivot tables
pd.pivot_table(df, values='sales', index='category', columns='year')
```

---

## Visualization

### Matplotlib/Seaborn
```python
import matplotlib.pyplot as plt
import seaborn as sns

# Basic line chart
plt.figure(figsize=(10, 6))
plt.plot(df['date'], df['sales'])
plt.title('Sales Over Time')
plt.xlabel('Date')
plt.ylabel('Sales')
plt.savefig('chart.png')

# Seaborn heatmap
sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
```

### Chart.js (JavaScript)
```javascript
new Chart(ctx, {
  type: 'bar',
  data: {
    labels: ['Jan', 'Feb', 'Mar'],
    datasets: [{
      label: 'Sales',
      data: [12, 19, 3],
      backgroundColor: 'rgba(99, 102, 241, 0.5)'
    }]
  }
});
```

---

## Common Analysis Patterns

| Task | Code |
|------|------|
| Top N items | `df.nlargest(10, 'sales')` |
| Date filtering | `df[df['date'] >= '2024-01-01']` |
| Rolling average | `df['sales'].rolling(7).mean()` |
| Year-over-year | `df.groupby(df['date'].dt.year)` |
| Percentiles | `df['sales'].quantile([0.25, 0.5, 0.75])` |

---

## Analysis Checklist

- [ ] Load and inspect data
- [ ] Handle missing values
- [ ] Clean and transform
- [ ] Exploratory analysis
- [ ] Create visualizations
- [ ] Extract insights
- [ ] Document findings
