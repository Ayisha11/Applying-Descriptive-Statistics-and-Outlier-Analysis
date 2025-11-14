import pandas as pd
from pathlib import Path
import sys

downloads = Path.home() / "Downloads"

candidates = []
for p in downloads.rglob("*.csv"):
    name = p.name.lower()
    if any(k in name for k in ("customer", "purchase", "purchasing", "behav", "behavior", "behaviour")):
        candidates.append(p)

if not candidates:
    print("No likely dataset found under ~/Downloads. Here are the top-level files in ~/Downloads:")
    for p in sorted(downloads.iterdir()):
        print(" -", p.name)
    sys.exit(1)

print("Found the following candidate CSV files:")
for i, p in enumerate(candidates):
    print(f"[{i}] {p}  (size: {p.stat().st_size} bytes)")

choice_index = 0
file_path = candidates[choice_index]
print(f"\nUsing candidate [{choice_index}]: {file_path}\n")


try:
    data = pd.read_csv(file_path)
except Exception as e:
    print("Failed to read CSV. Error:", e)
    sys.exit(1)

print("FIRST 5 ROWS")
print(data.head())

print("\n COLUMNS ")
print(data.columns.tolist())

print("\n DATAFRAME INFO")
print(data.info())

print("\n MISSING VALUES")
print(data.isnull().sum())

print("\n DESCRIPTIVE STATISTICS ")
desc_stats = data.describe()
print(desc_stats)

print("\n MODE OF EACH COLUMN ")
for column in ['age', 'annual_income', 'purchase_amount', 'loyalty_score', 'purchase_frequency']:
    mode_val = data[column].mode()[0]
    print(f"{column}: {mode_val}")

print("\n CORRELATION BETWEEN NUMERICAL VARIABLES")
print(data.corr(numeric_only=True))

print("\n INSIGHTS ")

print(f"Average customer age: {data['age'].mean():.1f} years")
print(f"Average annual income: ₹{data['annual_income'].mean():.0f}")
print(f"Average purchase amount: ₹{data['purchase_amount'].mean():.0f}")
print(f"Average loyalty score: {data['loyalty_score'].mean():.2f}")

region_avg = data.groupby('region')['purchase_amount'].mean().sort_values(ascending=False)
print("\nAverage Purchase Amount by Region:")
print(region_avg)

print("\n OUTLIER DETECTION USING IQR ")
numeric_cols = ['age', 'annual_income', 'purchase_amount', 'loyalty_score', 'purchase_frequency']

for column in numeric_cols:
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_limit = Q1 - 1.5 * IQR
    upper_limit = Q3 + 1.5 * IQR

    outliers = data[(data[column] < lower_limit) | (data[column] > upper_limit)]
    print(f"\nColumn: {column}")
    print(f"Lower limit: {lower_limit:.2f}, Upper limit: {upper_limit:.2f}")
    print(f"Number of outliers: {len(outliers)}")


