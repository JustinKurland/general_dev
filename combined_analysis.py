import pandas as pd

# Combine results
all_results = pd.DataFrame([results_weekly, results_daily, results_hourly, results_minute])

# Display the consolidated results
import ace_tools as tools; tools.display_dataframe_to_user(name="Consolidated Temporal Analysis Results", dataframe=all_results)


# Interpretation Logic
interpretation = []

# Check seasonality strength across temporal units
if all(all_results['Seasonality Strength'] > 0.8):
    interpretation.append(
        "Strong seasonality detected across all temporal units, suggesting highly repetitive patterns consistent with automation."
    )
elif any(all_results['Seasonality Strength'] > 0.8):
    interpretation.append(
        "Strong seasonality detected at some temporal units, which may indicate partial or conditional automation."
    )
else:
    interpretation.append(
        "Seasonality strength is weak across all temporal units, reducing the likelihood of automation."
    )

# Check residual variance across temporal units
if all(all_results['Residual to Total Ratio'] < 0.1):
    interpretation.append(
        "Residual variance is very small across all temporal units, meaning most variations are predictable. This supports evidence of automation."
    )
elif any(all_results['Residual to Total Ratio'] < 0.1):
    interpretation.append(
        "Residual variance is low at some temporal units, indicating partially systematic patterns."
    )
else:
    interpretation.append(
        "High residual variance across all temporal units indicates lack of systematic patterns, reducing the likelihood of automation."
    )

# Check dominant frequencies
if all_results['Dominant Frequency'].notna().all():
    interpretation.append(
        "Recurring dominant frequencies detected across all temporal units, indicating strong periodic patterns potentially driven by an automated process."
    )
else:
    interpretation.append(
        "Dominant frequencies are not consistently recurring across temporal units, reducing evidence for automation."
    )

# Print Final Interpretation
print("Integrated Analysis Across Temporal Units:")
for line in interpretation:
    print(f"- {line}")
