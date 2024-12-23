from catboost import Pool

# Create a test Pool
test_pool = Pool(
    data=X_test_selected,
    label=y_test,
    cat_features=updated_cat_features,
    text_features=updated_text_features,
    feature_names=list(X_test_selected.columns)
)

# Predict probabilities
y_pred_proba = model.predict_proba(test_pool)

# Combine the results into a DataFrame for analysis
results = pd.DataFrame({
    'number': number_test,  # ID column for reference
    'actual': y_test,
    'predicted_proba_class_0': y_pred_proba[:, 0],
    'predicted_proba_class_1': y_pred_proba[:, 1]
})



from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt

# Convert predicted probabilities to binary class labels (threshold = 0.5)
results['predicted'] = (results['predicted_proba_class_1'] >= 0.5).astype(int)

# Generate the confusion matrix
conf_matrix = confusion_matrix(results['actual'], results['predicted'])

# Plot the confusion matrix
plt.figure(figsize=(8, 5))
plt.imshow(conf_matrix, cmap='Blues', interpolation='nearest')
plt.title('Confusion Matrix')
plt.colorbar()
plt.xticks([0, 1], ['No Impact', 'Risk'])
plt.yticks([0, 1], ['No Impact', 'Risk'])
plt.xlabel('Predicted Label')
plt.ylabel('Actual Label')
plt.text(0, 0, conf_matrix[0, 0], ha='center', va='center', color='black')
plt.text(0, 1, conf_matrix[0, 1], ha='center', va='center', color='black')
plt.text(1, 0, conf_matrix[1, 0], ha='center', va='center', color='black')
plt.text(1, 1, conf_matrix[1, 1], ha='center', va='center', color='black')
plt.show()


from sklearn.metrics import precision_score, recall_score, f1_score

# Function to calculate metrics at various thresholds
def calculate_metrics_at_thresholds(y_true, y_pred_proba, thresholds):
    metrics = []
    for threshold in thresholds:
        y_pred = (y_pred_proba >= threshold).astype(int)
        precision = precision_score(y_true, y_pred, zero_division=0)
        recall = recall_score(y_true, y_pred, zero_division=0)
        f1 = f1_score(y_true, y_pred, zero_division=0)
        metrics.append([threshold, precision, recall, f1])
    return metrics

# Thresholds to test
thresholds = np.arange(0.1, 0.9, 0.05)

# Calculate metrics
metrics = calculate_metrics_at_thresholds(results['actual'], results['predicted_proba_class_1'], thresholds)

# Convert to a DataFrame for easy analysis
metrics_df = pd.DataFrame(metrics, columns=['Threshold', 'Precision', 'Recall', 'F1'])

# Find the optimal threshold based on the highest F1-score
optimal_threshold = metrics_df.loc[metrics_df['F1'].idxmax(), 'Threshold']
print(f"Optimal Threshold: {optimal_threshold}")

# Plot Precision-Recall Curve
plt.figure(figsize=(10, 6))
plt.plot(metrics_df['Threshold'], metrics_df['Precision'], label='Precision')
plt.plot(metrics_df['Threshold'], metrics_df['Recall'], label='Recall')
plt.plot(metrics_df['Threshold'], metrics_df['F1'], label='F1')
plt.xlabel('Threshold')
plt.ylabel('Score')
plt.title('Precision, Recall, and F1 vs. Threshold')
plt.legend()
plt.show()

# Apply the optimal threshold to the predictions
results['predicted'] = (results['predicted_proba_class_1'] >= optimal_threshold).astype(int)
