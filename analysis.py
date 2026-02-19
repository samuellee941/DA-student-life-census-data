import pandas as pd
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')  # non-interactive backend (use 'TkAgg' if you want popups)
import matplotlib.pyplot as plt


### 1. Load Data
df = pd.read_excel('2024_Biennial_Census_Results.xlsx')
df = df.drop(columns=['Timestamp'])  # not useful for analysis

### 2. Convert Word-Values to Numbers
likert_map = {
    'Strongly Agree': 6,
    'Agree': 5,
    'Slightly Agree': 4,
    'Slightly Disagree': 3,
    'Disagree': 2,
    'Strongly Disagree': 1,
    'Strongly Agree (Would use)': 6,
    'Strongly Disagree (Would not use)': 1,
}

### 3. Label Columns as Traits or Sentiments
trait_columns = {
    'grade': 'What grade are you in?',
    'gender': 'How would you describe your gender?',
    'years': 'How many years have you attended HKIS?',
    'cultures': 'Which of the following cultures do you identify with? [Choose all that apply]',
    'clubs': 'Which of the following are you involved in (in-school)? [Choose all that apply]',
    'involvement': 'Which of the following best describes your involvement at HKIS?',
}

# Labels all Likert columns as Sentiments
sentiment_cols = []
for col in df.columns:
    if col in trait_columns.values():
        continue
    unique_vals = set(df[col].dropna().unique())
    if unique_vals & set(likert_map.keys()):
        sentiment_cols.append(col)

# Encodes Likert Values
df_encoded = df.copy()
for col in sentiment_cols:
    df_encoded[col] = df[col].map(likert_map)


### 4. Finding Low Sentiments

sentiment_means = df_encoded[sentiment_cols].mean().sort_values()
overall_mean = sentiment_means.mean()
overall_std = sentiment_means.std()
threshold = overall_mean - overall_std

print(f"Overall sentiment mean: {overall_mean:.2f}")
print(f"Flagging threshold (mean - 1 SD): {threshold:.2f}\n")

flagged = sentiment_means[sentiment_means < threshold]
print(f"⚠️  {len(flagged)} questions scored unusually low:")
for col, val in flagged.items():
    print(f"  [{val:.2f}] {col}")


### 5. Trait vs. Sentiment Correlation

# a) involvement
df_encoded['involvement_binary'] = df[trait_columns['involvement']].apply(
    lambda x: 'Participates' if 'Yes' in str(x) else 'Does not'
)

categorical_traits = {
    'Grade': trait_columns['grade'],
    'Gender': trait_columns['gender'],
    'Involvement': 'involvement_binary',
}

results = []

for trait_name, trait_col in categorical_traits.items():
    groups = df_encoded[trait_col].dropna().unique()

    for sent_col in sentiment_cols:
        # gather data for each group
        group_data = [
            df_encoded.loc[df_encoded[trait_col] == g, sent_col].dropna().values
            for g in groups
            if len(df_encoded.loc[df_encoded[trait_col] == g, sent_col].dropna()) >= 5
        ]

        if len(group_data) < 2:
            continue

        stat, p = stats.kruskal(*group_data)

        if p < 0.05:
            # effect size: eta-squared approximation from H statistic
            # n ** 2 = (H - k + 1) / (N - k), where k = number of groups
            n = sum(len(g) for g in group_data)
            k = len(group_data)
            eta_sq = max(0, (stat - k + 1) / (n - k))
            # edit: guide: 0.01 = small, 0.06 = medium, 0.14 = large

            if eta_sq > 0.02:  # considers at least a small-to-medium effect
                results.append({
                    'trait': trait_name,
                    'sentiment': sent_col,
                    'p_value': p,
                    'effect_size': eta_sq,
                })

# b) years at HKIS
def extract_years(val):
    """'3 (joined in 2022)' → 3"""
    try:
        return int(str(val).split('(')[0].strip())
    except:
        return np.nan

df_encoded['years_numeric'] = df[trait_columns['years']].apply(extract_years)

for sent_col in sentiment_cols:
    mask = df_encoded['years_numeric'].notna() & df_encoded[sent_col].notna()
    if mask.sum() < 30:
        continue
    rho, p = stats.spearmanr(
        df_encoded.loc[mask, 'years_numeric'],
        df_encoded.loc[mask, sent_col]
    )
    if p < 0.05 and abs(rho) > 0.1:
        results.append({
            'trait': 'Years at HKIS',
            'sentiment': sent_col,
            'p_value': p,
            'effect_size': rho**2,  # r ** 2 as a comparable effect size
        })

# print results
results_df = pd.DataFrame(results).sort_values('effect_size', ascending=False)
print(f"\n\nTop 20 Trait to Sentiment correlations (by effect size):")
print(results_df.head(20).to_string(index=False))


### 6. Graphing

fig, ax = plt.subplots(figsize=(14, 8))
bottom15 = sentiment_means.head(15)
labels = [s[:55] + '...' if len(s) > 55 else s for s in bottom15.index]
colors = ['#d32f2f' if v < threshold else '#ff9800' for v in bottom15.values]

ax.barh(range(len(bottom15)), bottom15.values, color=colors)
ax.set_yticks(range(len(bottom15)))
ax.set_yticklabels(labels, fontsize=8)
ax.axvline(x=overall_mean, color='black', linestyle='--', label=f'Mean ({overall_mean:.2f})')
ax.axvline(x=threshold, color='red', linestyle=':', label=f'-1 SD ({threshold:.2f})')
ax.set_xlabel('Mean Score (1=Strongly Disagree → 6=Strongly Agree)')
ax.set_title('Bottom 15 Sentiment Scores — HKIS 2024 Census', fontweight='bold')
ax.legend()
ax.invert_yaxis()
plt.tight_layout()
plt.savefig('chart_low_sentiments.png', dpi=150)
plt.close()

print("\n Completed.")