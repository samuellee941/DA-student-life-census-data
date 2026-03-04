# Biennial Census Data - Approach, Cleaning, Analysis and Findings

I will approach this data considering columns as either **traits** or **scores** (note, some can be both).

**Traits** are characteristics that an individual possesses, from their ethnicity, years at HKIS to whether they play sports, or where they find their social circles at HKIS (Homeroom, Sports Teams, etc.)

**Groups** are subsets within traits (eg. Grade 9 within Grade Levels or Male within Gender). We will compare group-score correlations to see if groups indicate certain scoring trends.

**Scores** are the responses we get: the individual's understanding of HKIS official communication outlets, where they find their social circles at HKIS (note the overlap), and whether they feel a strong sense of community.

---

I have two main objectives:
1. To identify any unusually low scores — these should be the main priority to address, as it demonstrates a school-wide low.
2. To identify any scores that orderedly differ between groups within a trait (ex. Sense of belonging scores differ between sports-players and non-sports players) — these show a disparity that occurs due to certain traits that can be addressed.

**Methodology:**
1. Data Cleaning
2. Data Analysis (two tests)

---

## Data Cleaning

1. Renaming Columns
2. (Easily Inferrable Numbers) → Ints
3. Likert Scale → Ints
4. Multi-Choice Columns → Multi-Hot Encoding
5. Empty Boxes → NaNs
6. Remove Duplicate Columns, Incomplete Rows

Completed.

---

## Data Analysis

As a precursor, I have labeled all columns as either "Trait" columns, "Score" columns, or both.

For reference:
- **Traits:** Grade, Gender, Years attended, Involvement type, Culture, Involvement, Community Context, Service Realm, Service Motivation
- **Scores:** Community, School Sentiment, Academics, Citizenship, Service, Communications, Clubs & Leadership, Sports & Arts, Athletics, Performing Arts

### Analysis 1: Low Scores
- As a benchmark, we will compute the mean and standard deviation of the entire census.
- For each score column, will compute the mean across all respondents.
- Any score whose mean is more than 1 sd below the mean of all scores will be flagged.

### Analysis 2: High Group-Score Disparities
- For each trait-score pairing, split respondents into groups within the trait and compare score distributions. A pairing will be flagged if it passes both of the following:
  - **Statistical significance (p < 0.05):** A t-test (2 groups) or one-way ANOVA (3+ groups) confirms the identified disparity is unlikely to be random noise.
  - **Effect size (Cohen's d > 0.3):** The magnitude of the difference clears a threshold. For 3+ groups, Cohen's d is computed between the highest and lowest scoring groups.
- Pairings that pass both filters are flagged.

**Edit: Raw Results Uploaded**
> *Upon review, a lot of the results are intuitively discardable — PLEASE use intuition to understand what the numbers mean; they're merely a guide.*

---

## Key Findings

### Low Scores
1. **MS Teams is the lowest-rated platform (2.95/6)** — by far the worst performer, critically below threshold
2. **Performing arts students feel unsupported** — performances celebrated (3.03), arts balance (3.18), and groupmate support (3.30) are all in the bottom 4 scores school-wide, not just among arts students
3. **Grading consistency is weak (3.39)** — students broadly don't feel teachers marking the same course grade the same way
4. **Peer accountability is barely above the threshold (3.56)** — students don't feel peers call out racist/homophobic/sexist comments
5. **Comfortable trying out (3.40) and athletic-academic balance (3.41)** are also flagged

### High Group-Score Disparity
6. **Non-binary/gender-fluid students feel significantly less community** — the largest gender gaps are in sense of community (grade, homeroom, classes), with Cohen's d up to 2.0. They also score notably lower on school pride. This is the most concerning disparity in the dataset.
7. **Grade 12s find communication platforms much less useful than Grade 9s** — DragonNet gap is large (d=0.83), Teams and Campus Catchup also significant. Older students are tuning out.
8. **Performing arts students still feel underserved** — even among students who do performing arts, arts scores are low (3.82–4.29), compared to sports players' athletic scores (4.4–4.9)
