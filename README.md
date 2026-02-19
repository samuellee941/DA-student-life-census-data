# Student Wellbeing Report based on Census Data 2024-25

*Methodology:*

Trait vs Sentiment Correlation Analysis

This analysis has two aims:
  1. Identifies which sentiment questions are scored unusually low
  (these should be immediately be considered and addressed)
  2. Tests whether traits (grade, gender, involvement, years) predict
     differences in sentiment responses (these should give us insights
     into HOW to address issues, and which communities to target)

Tools Used: pandas, numpy, scipy.stats, matplotlib

*Key Findings:*

Unusually low sentiments:

Microsoft Teams as an info platform scored the absolute lowest (2.95/6)
Cross Section and DragonNet also scored poorly as info platforms
Grading consistency across teachers is a real pain point (3.39)
Students holding each other accountable for racist/homophobic/sexist comments (3.56) — this is a substantive one
Parental academic pressure is high (3.92 — note this is reverse-coded in spirit; high agreement = more stress)

Strongest trait to sentiment correlations:

1. Involvement (Sports/Arts) has the biggest skewing — participants score ~1 full point higher on community belonging,
excitement to attend events, and comfort trying new activities (n ** 2 up to 0.16, which is a large effect). Chart 3 shows this clearly.
2. Grade level matters a lot — Chart 2's heatmap shows a clear pattern: Grade 9s feel most supported and connected,
and it drops steadily toward Grade 12. The biggest drops are in grading consistency, sense of having a trusted adult,
and feeling equipped to balance academics with activities.
3. Gender showed moderate effects on community belonging and excitement to come to school.
4. Years at HKIS has weaker but real correlations — longer-tenured students find Instagram more useful and feel more
aware of service opportunities, but find Microsoft Teams less useful.
