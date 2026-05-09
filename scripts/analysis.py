import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------- LOAD DATA ----------------
df = pd.read_csv("data/car_prices.csv", low_memory=False)

# ---------------- CLEAN COLUMN NAMES ----------------
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

print("\nColumns in dataset:\n", df.columns)

# ---------------- AUTO-DETECT COLUMNS ----------------
price_col = None
brand_col = None
fuel_col = None
trans_col = None

for col in df.columns:
    if "price" in col:
        price_col = col
    if "brand" in col or "make" in col:
        brand_col = col
    if "fuel" in col or "engine" in col:
        fuel_col = col
    if "trans" in col:
        trans_col = col

print("\nDetected Columns:")
print("Price:", price_col)
print("Brand:", brand_col)
print("Fuel:", fuel_col)
print("Transmission:", trans_col)

# ---------------- VALIDATION ----------------
if price_col is None:
    raise Exception("❌ Price column not found")

# ---------------- CLEAN DATA ----------------
df = df.drop_duplicates()
df[price_col] = pd.to_numeric(df[price_col], errors='coerce')
df = df.dropna(subset=[price_col])

# ---------------- KPIs ----------------
avg_price = df[price_col].mean()
total_cars = df.shape[0]

print("\nKPIs:")
print("Average Price:", avg_price)
print("Total Cars:", total_cars)

# ---------------- DEEP ANALYSIS ----------------
if fuel_col:
    print("\nAverage Price by Fuel:")
    print(df.groupby(fuel_col)[price_col].mean())

if brand_col:
    print("\nAverage Price by Brand:")
    print(df.groupby(brand_col)[price_col].mean())

# ---------------- VISUALIZATIONS ----------------

# 1. Price by Brand
if brand_col:
    plt.figure()
    sns.barplot(x=brand_col, y=price_col, data=df)
    plt.xticks(rotation=90)
    plt.title("Price by Brand")
    plt.savefig("outputs/price_by_brand.png")

# 2. Transmission Pie Chart
if trans_col:
    plt.figure()
    df[trans_col].value_counts().plot(kind='pie', autopct='%1.1f%%')
    plt.title("Transmission Distribution")
    plt.savefig("outputs/transmission.png")

# 3. Fuel Chart (SAFE)
if fuel_col and fuel_col in df.columns:
    df_fuel = df[df[fuel_col].notna()]

    if df_fuel[fuel_col].nunique() > 0:
        plt.figure()
        sns.countplot(x=fuel_col, data=df_fuel)
        plt.title("Fuel Type Count")
        plt.savefig("outputs/fuel.png")
    else:
        print("⚠️ Fuel column has no usable data")
else:
    print("⚠️ Fuel column not found → creating alternative chart")

    # Alternative chart
    plt.figure()
    sns.histplot(df[price_col], bins=30)
    plt.title("Price Distribution")
    plt.savefig("outputs/price_distribution.png")

plt.show()

