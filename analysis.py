import pandas as pd
import numpy as np

df = pd.read_excel("2024_Biennial_Census_Results.xlsx")
print(df.shape)           # rows × columns
print(df.dtypes)          # what type is each column?
print(df.isnull().sum())  # how many NaNs per column?
print(df.head(3))

"""PART ONE: CLEANING"""

### RENAMING COLUMNS

df = df.rename(columns={
    # Demographic Data
    "Timestamp": "timestamp",
    "What grade are you in?": "grade",
    "How would you describe your gender?": "gender",
    "How many years have you attended HKIS?": "years_attended",
    "Which of the following cultures do you identify with? [Choose all that apply]": "culture",
    "Which of the following are you involved in (in-school)? [Choose all that apply]": "involvement",

    # School Sentiment
    "I am excited to come to school": "excited_school",
    "I am proud to be an HKIS Dragon (aka. an HKIS student)": "proud_hkis",
    "There is an adult on campus I feel comfortable speaking to on matters other than academics": "trusted_adult",

    # Sense of Community (Places)
    "I feel a strong sense of HKIS community in the following places [Homeroom/PChG ]": "community_homeroom",
    "I feel a strong sense of HKIS community in the following places [Within My Grade ]": "community_grade",
    "I feel a strong sense of HKIS community in the following places [Academic Classes]": "community_classes",
    "I feel a strong sense of HKIS community in the following places [Clubs]": "community_clubs",
    "I feel a strong sense of HKIS community in the following places [Sports Teams]": "community_sports",
    "I feel a strong sense of HKIS community in the following places [Friends/Social Group]": "community_friends",

    # Seek Friends (Places)
    "I would use the following activities to make new friends [Homeroom/PChG]": "friends_homeroom",
    "I would use the following activities to make new friends [Within My Grade]": "friends_grade",
    "I would use the following activities to make new friends [Academic Classes]": "friends_classes",
    "I would use the following activities to make new friends [Clubs]": "friends_clubs",
    "I would use the following activities to make new friends [Sports Teams ]": "friends_sports",
    "I would use the following activities to make new friends [Friends/Social Group ]": "friends_social",

    # Academic Scores
    "I know how to advocate for myself with teachers in regards to academics": "self_advocate",
    "I feel that teachers are receptive to feedback about my learning experience": "teacher_receptive",
    "I feel that grading expectations/standards from different teachers teaching the same course is consistent.": "grading_consistent",
    "I believe that there are adequate resources to help me select the class that best fits my needs (Insiders Guide, Academic Handbook, etc)": "course_resources",
    "Parental pressure is a significant source of academic stress for me": "parental_pressure",
    "I feel supported by my parents to pursue my academic passions": "parental_support",

    # Citizenship Scores
    "I care about the environment and ensuring our school participates in sustainable practices": "env_care",
    "Students at HKIS hold each other accountable when racist/homophobic/sexist comments are made": "peer_accountability",

    # Service Scores
    "Which realms are you most passionate about serving? [Choose all that apply]": "service_realms",
    "Which factors motivate you to participate in service the most? [Choose all that apply]": "service_motivators",
    "I am aware of my school's various service opportunities and know who to approach to get involved": "service_awareness",

    # PR Scores
    "I find the following platform helpful for receiving information [Instagram (@hkis.exco, @hkis2025) ]": "platform_instagram",
    "I find the following platform helpful for receiving information [DragonNet]": "platform_dragonnet",
    "I find the following platform helpful for receiving information [Cross Section]": "platform_crosssection",
    "I find the following platform helpful for receiving information [Schoology Announcements]": "platform_schoology",
    "I find the following platform helpful for receiving information [Microsoft Teams]": "platform_teams",
    "I find the following platform helpful for receiving information [Campus Catchup/PubliCo Monthly Videos]": "platform_campuscatchup",
    "I find the following platform helpful for receiving information [Email]": "platform_email",

    # Clubs Scores
    "I require more training in Microsoft software": "needs_microsoft_training",
    "I have a good understanding of what the Senate does to serve the school": "understands_senate",
    "I have been exposed to strong student club leaders (who understand school processes, mentor younger students etc.)": "strong_club_leaders",
    "I feel that club leadership selection has been fair (transparent & effective)": "fair_club_selection",
    "Which of the following best describes your involvement at HKIS?": "involvement_type",

    # Sports & Arts [Scores]
    "I feel excited to attend sports games and arts performances hosted at HKIS": "excited_events",
    "I feel comfortable trying out for new sports teams and performing arts": "comfortable_tryouts",

    # Athletes-Only Scores
    "Team victories are acknowledged and celebrated at HKIS": "athletics_victories_celebrated",
    "My teammates support and encourage me in my athletic endeavours": "athletics_teammate_support",
    "My coach cares about me beyond my performance quality": "athletics_coach_cares",
    "I am equipped to balance my academic responsibilities with my athletic commitments": "athletics_balance",

    # Artists-Only Scores
    "Successful performances are acknowledged and celebrated at HKIS": "arts_performances_celebrated",
    "My groupmates (bandmates, ensemble etc.) support and encourage me in my artistic endeavours": "arts_groupmate_support",
    "I am equipped to balance my academic responsibilities with my performing arts commitments": "arts_balance",

    # Duplicate Columns
    "Team victories and successful performances are acknowledged and celebrated at HKIS": "combined_celebrated_dup",
    "I feel excited to attend sports games and arts performances hosted at HKIS.1": "excited_events_dup",
    "I feel comfortable trying out for new sports teams and performing art groups": "comfortable_tryouts_dup",
})

### CONVERTING NUMBER-LIKES TO NUMBERS

df["grade"] = df["grade"].str.extract(r"(\d+)").astype(int)
df["years_attended"] = df["years_attended"].str.extract(r"(\d+)").astype(int)

### CONVERTING LIKEART SCALE

# Label Non-Likearts, Likearts

non_likert = [
    "timestamp", "grade", "gender", "years_attended",
    "culture", "involvement", "service_realms", "service_motivators",
    "involvement_type",
    "combined_celebrated_dup", "excited_events_dup", "comfortable_tryouts_dup"
]

likert_cols = [col for col in df.columns if col not in non_likert]

# First, must strip (Would Use) from some of the scales

df[likert_cols] = df[likert_cols].apply(
    lambda col: col.str.replace(r"\s*\(Would.*?\)", "", regex=True).str.strip()
)

# Additional cleaning

does_not_participate = [
    "I do not participate in HKIS athletics",
    "I do not participate in HKIS performing arts",
    "I am a student athlete/performer who already completed the previous section"
]

# Likeart mapping

for col in likert_cols:
    df[col] = df[col].replace(does_not_participate, pd.NA)

likert_map = {
    "Strongly Disagree": 1,
    "Disagree":          2,
    "Slightly Disagree": 3,
    "Slightly Agree":    4,
    "Agree":             5,
    "Strongly Agree":    6,
}

# Applying it

for col in likert_cols:
    df[col] = df[col].map(likert_map)

print(df[likert_cols].stack().unique())

### Multi-select lists (oh what a horrid census to deal with)

# First, rename the ANNOYING names... (remove commas so we can split)

df["involvement"] = df["involvement"].str.replace(
    "Student Leadership Teams (eg. NHS, SDLT)", 
    "Student Leadership Teams", 
    regex=False
)
df["involvement"] = df["involvement"].str.replace(
    "Formal School Leadership (eg. club leadership, captain, section leader)", 
    "Formal School Leadership", 
    regex=False
)

df["service_motivators"] = df["service_motivators"].str.replace(
    "External Relationships (eg. NGOs, other communities)",
    "External Relationships",
    regex=False
)

# Second, multi-hot encoding

from sklearn.preprocessing import MultiLabelBinarizer

def multi_hot_encode(df, col, prefix):
    mlb = MultiLabelBinarizer()
    encoded = pd.DataFrame(
        mlb.fit_transform(df[col].apply(lambda x: x if isinstance(x, list) else [])),
        columns=[prefix + c.lower().replace(" ", "_").replace("/", "_")
                 for c in mlb.classes_],
        index=df.index
    )
    return pd.concat([df.drop(columns=col), encoded], axis=1)

df["culture"] = df["culture"].str.split(", ")
df = multi_hot_encode(df, "culture", "culture_")

df["involvement"] = df["involvement"].str.split(", ")
df = multi_hot_encode(df, "involvement", "involvement_")

df["service_realms"] = df["service_realms"].str.split(", ")
df = multi_hot_encode(df, "service_realms", "realm_")

df["service_motivators"] = df["service_motivators"].str.split(", ")
df = multi_hot_encode(df, "service_motivators", "motiv_")

### Clean N/A Participants

is_participant = df["involvement_type"] == \
    "Yes, I participate in sports or performing arts at HKIS (Varsity/JV Teams)"

# Sports/Arts Column 1
general_cols = [
    "excited_events",
    "comfortable_tryouts",
]
for col in general_cols:
    df.loc[~is_participant, col] = df.loc[~is_participant, col].fillna(0)

# Athlete-Specific Columns
athletics_cols = [
    "athletics_victories_celebrated",
    "athletics_teammate_support",
    "athletics_coach_cares",
    "athletics_balance",
]
for col in athletics_cols:
    df.loc[~is_participant, col] = df.loc[~is_participant, col].fillna(0)

# Arts-Specific Columns
arts_cols = [
    "arts_performances_celebrated",
    "arts_groupmate_support",
    "arts_balance",
]
for col in arts_cols:
    df.loc[~is_participant, col] = df.loc[~is_participant, col].fillna(0)

### Removing Duplicate Columns & Incomplete Rows

df = df.drop(columns=["combined_celebrated_dup", "excited_events_dup", "comfortable_tryouts_dup"])

threshold = len(df.columns) * 0.5
df = df.dropna(thresh=threshold)

"""PART TWO: ANALYTICS & MODELLING"""
"""
Methodology:

As a precursor, I have labeled all columns as either “Trait” columns, “Score” columns, or both.
For reference:
Traits: 
Scores: 

Analysis 1: Low Scores

As a benchmark, we will compute the mean and standard deviation of the entire census.
For each score column, will compute the mean across all respondents.
Any score whose mean is more than 1 sd below the mean of all scores will be flagged.

Analysis 2: Group-Related Disparity Scores

For each trait-score pairing, split respondents into groups within the trait and compare score
distributions. A pairing will be flagged if it passes both of the following:
    - Statistical significance (p < 0.05): A t-test (2 groups) or one-way ANOVA (3+ groups) confirms
    the identified disparity is unlikely to be random noise.
    - Effect size (Cohen's d > 0.3): The magnitude of the difference clears a threshold.  For 3+
    groups, Cohen's d is computed between the highest and lowest scoring groups.
Pairings that pass both filters are meaningful disparities to consider.

"""
### PRE-ANALYSIS PREP

# Labeling trait / score / both columns (for ease later)

traits = [
    "grade",
    "gender",
    "years_attended",
    "involvement_type",

    "culture_african",
    "culture_east_asian",
    "culture_european",
    "culture_latinx_hispanic",
    "culture_middle_eastern_north_african",
    "culture_north_american",
    "culture_south_asian",
    "culture_southeast_asian",

    "involvement_formal_school_leadership",
    "involvement_non-service_clubs",
    "involvement_none_of_the_above",
    "involvement_performing_arts",
    "involvement_service_clubs",
    "involvement_sports",
    "involvement_student_leadership_teams",

    "realm_none_of_the_above",
    "realm_senior_support",
    "realm_social_justice",
    "realm_special_needs",
    "realm_student_empowerment",
    "realm_sustainability_environment",
    "motiv_college",
    "motiv_external_relationships",
    "motiv_family_values",
    "motiv_i_am_not_motivated_to_participate_in_service",
    "motiv_internal_relationships_(eg._friends_and_club_community)",
    "motiv_personal_values",
    "motiv_the_cause",
]

scores = [
    "excited_school",
    "proud_hkis",
    "trusted_adult",

    "self_advocate",
    "teacher_receptive",
    "grading_consistent",
    "course_resources",
    "parental_pressure",
    "parental_support",

    "env_care",
    "peer_accountability",

    "service_awareness",

    "platform_instagram",
    "platform_dragonnet",
    "platform_crosssection",
    "platform_schoology",
    "platform_teams",
    "platform_campuscatchup",
    "platform_email",

    "needs_microsoft_training",
    "understands_senate",
    "strong_club_leaders",
    "fair_club_selection",

    "excited_events",
    "comfortable_tryouts",

    "athletics_victories_celebrated",
    "athletics_teammate_support",
    "athletics_coach_cares",
    "athletics_balance",

    "arts_performances_celebrated",
    "arts_groupmate_support",
    "arts_balance",
]

both = [
    "community_homeroom",
    "community_grade",
    "community_classes",
    "community_clubs",
    "community_sports",
    "community_friends",
    "friends_homeroom",
    "friends_grade",
    "friends_classes",
    "friends_clubs",
    "friends_sports",
    "friends_social",
]

all_scores = scores + both
all_traits = traits + both

score_means = df[all_scores].mean()

### ANALYSIS 1: LOW SCORES

grand_mean = score_means.mean()
grand_std  = score_means.std()

low_threshold = grand_mean - grand_std

# Print Key

print(f"Grand mean of all score means : {grand_mean:.3f}")
print(f"Standard deviation            : {grand_std:.3f}")
print(f"Low score threshold (mean - 1σ): {low_threshold:.3f}")
print()

# Print Flagged Scores (Too Low)
low_scores = score_means[score_means < low_threshold].sort_values()

print(f"{'Column':<40} {'Mean':>6}  {'Deviation from threshold':>24}")
print("-" * 74)
for col, mean in low_scores.items():
    deviation = mean - low_threshold
    print(f"{col:<40} {mean:>6.3f}  {deviation:>+24.3f}")

### ANALYSIS 2: Group-Related Disparity Scores

from scipy import stats
import itertools

def cohens_d(group_a, group_b):
    na, nb = len(group_a), len(group_b)
    if na < 2 or nb < 2:
        return 0
    pooled_std = np.sqrt(
        ((na - 1) * group_a.std()**2 + (nb - 1) * group_b.std()**2) / (na + nb - 2)
    )
    if pooled_std == 0:
        return 0
    return abs(group_a.mean() - group_b.mean()) / pooled_std

P_THRESHOLD = 0.05
D_THRESHOLD = 0.3
MIN_GROUP_SIZE = 10

results = []

for trait in all_traits:
    col = df[trait]

    # Binary multi-hot traits
    if set(col.dropna().unique()).issubset({0, 1}):
        group_has  = df[col == 1]
        group_not  = df[col == 0]
        if len(group_has) < MIN_GROUP_SIZE or len(group_not) < MIN_GROUP_SIZE:
            continue
        groups_dict = {f"{trait}=1": group_has, f"{trait}=0": group_not}

    # Categorical traits
    else:
        unique_vals = col.dropna().unique()
        groups_dict = {
            val: df[col == val]
            for val in unique_vals
            if len(df[col == val]) >= MIN_GROUP_SIZE
        }
        if len(groups_dict) < 2:
            continue

    group_names  = list(groups_dict.keys())
    group_frames = list(groups_dict.values())

    for score in all_scores:
        # Extract score values per group, drop NaN
        group_scores = [g[score].dropna() for g in group_frames]

        # Drop any group that becomes too small after NaN removal
        valid = [(name, g) for name, g in zip(group_names, group_scores)
                 if len(g) >= MIN_GROUP_SIZE]
        if len(valid) < 2:
            continue

        valid_names, valid_scores = zip(*valid)

        # Filter 1
        if len(valid_scores) == 2:
            _, p_value = stats.ttest_ind(valid_scores[0], valid_scores[1],
                                         equal_var=False)  # Welch's t-test
        else:
            _, p_value = stats.f_oneway(*valid_scores)     # one-way ANOVA

        if p_value >= P_THRESHOLD:
            continue

        # Filter 2
        means = [g.mean() for g in valid_scores]
        best_idx  = int(np.argmax(means))
        worst_idx = int(np.argmin(means))

        d = cohens_d(valid_scores[best_idx], valid_scores[worst_idx])

        if d < D_THRESHOLD:
            continue

        # If passed:
        results.append({
            "trait":        trait,
            "score":        score,
            "p_value":      round(p_value, 4),
            "cohens_d":     round(d, 3),
            "high_group":   valid_names[best_idx],
            "high_mean":    round(means[best_idx], 3),
            "low_group":    valid_names[worst_idx],
            "low_mean":     round(means[worst_idx], 3),
            "mean_gap":     round(means[best_idx] - means[worst_idx], 3),
        })

# Print Results
results_df = pd.DataFrame(results).sort_values("cohens_d", ascending=False)

print(f"Flagged trait-score pairings: {len(results_df)}")
print()
print(results_df.to_string(index=False))
