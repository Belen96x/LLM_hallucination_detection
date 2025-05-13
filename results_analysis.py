import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

def analyze_results(input_csv, output_folder, model, model_name):
    """
    Analyze the results from the comparison CSV and generate plots.

    Args:
        input_csv (str): Path to the input CSV file.
        output_folder (str): Path to the folder where plots will be saved.
    """
    # Load the CSV file
    df = pd.read_csv(input_csv)

    # Generate a confusion matrix
    y_true = df['ground_truth_classification']
    y_pred = df['predicted_label']

    # Ensure y_true and y_pred are consistent types and convert to strings
    y_true = y_true.astype(str)
    y_pred = y_pred.astype(str)

    # Simplify labels for visibility by extracting the word between [number]_[word]_hallucination
    y_true_simpl = y_true.str.extract(r'\d+_(\w+)_hallucination')[0]
    y_pred_simpl = y_pred.str.extract(r'\d+_(\w+)_hallucination')[0]

    # Filter out rows with missing labels
    valid_mask = y_true_simpl.notna() & y_pred_simpl.notna()
    y_true_filtered = y_true_simpl[valid_mask]
    y_pred_filtered = y_pred_simpl[valid_mask]

    # Generate a sorted list of unique simplified labels as strings
    unique_labels = sorted(set(y_true_filtered).union(set(y_pred_filtered)), key=str)

    # Generate a confusion matrix
    cm = confusion_matrix(y_true_filtered, y_pred_filtered, labels=unique_labels, normalize='true')
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=unique_labels)

    # Plot the confusion matrix
    plt.figure(figsize=(10, 8))
    disp.plot(cmap='Blues', values_format='.2f')
    plt.title(f'Confusion Matrix ({model_name})')
    plt.savefig(f"{output_folder}/confusion_matrix_{model}.png")
    plt.close()

    # Plot the distribution of matches
    plt.figure(figsize=(8, 6))
    sns.countplot(data=df, x='match', palette='viridis')
    plt.title(f'Distribution of Matches ({model_name})')
    plt.xlabel('Match (True/False)')
    plt.ylabel('Count')
    plt.savefig(f"{output_folder}/match_distribution_{model}.png")
    plt.close()

    # Ensure comet_score is numeric
    if 'comet_score' in df.columns:
        df['comet_score'] = pd.to_numeric(df['comet_score'], errors='coerce')

    # Plot the distribution of COMET scores
    if 'comet_score' in df.columns and not df['comet_score'].isnull().all():
        plt.figure(figsize=(8, 6))
        sns.histplot(df['comet_score'].dropna(), bins=30, kde=True, color='skyblue')
        plt.title(f'Distribution of COMET Scores ({model_name})')
        plt.xlabel('COMET Score')
        plt.ylabel('Frequency')
        plt.savefig(f"{output_folder}/comet_score_distribution_{model}.png")
        plt.close()

    # 1. Per-Class Accuracy Bar Chart
    # Calculate accuracy per class
    accuracies = {}
    for label in unique_labels:
        mask = y_true_filtered == label
        if mask.sum() > 0:
            accuracies[label] = (y_true_filtered[mask] == y_pred_filtered[mask]).sum() / mask.sum()
    plt.figure(figsize=(8, 6))
    sns.barplot(x=list(accuracies.keys()), y=list(accuracies.values()), palette='magma')
    plt.title(f'Per-Class Accuracy ({model_name})')
    plt.xlabel('Class')
    plt.ylabel('Accuracy')
    plt.ylim(0, 1)
    plt.savefig(f"{output_folder}/per_class_accuracy_{model}.png")
    plt.close()

    # 2. Precision / Recall / F1 Bar Chart
    from sklearn.metrics import classification_report
    report = classification_report(
        y_true_filtered, y_pred_filtered,
        labels=unique_labels, output_dict=True, zero_division=0
    )
    metrics_df = pd.DataFrame(report).T.loc[unique_labels, ['precision', 'recall', 'f1-score']]
    metrics_df.plot(kind='bar', figsize=(10, 6), rot=0, colormap='viridis')
    plt.title(f'Precision, Recall, F1 by Class ({model_name})')
    plt.ylabel('Score')
    plt.ylim(0, 1)
    plt.legend(loc='lower right')
    plt.savefig(f"{output_folder}/prf_by_class_{model}.png")
    plt.close()

# Example usage
if __name__ == "__main__":
    model = "oneshot_gemma2"
    model_name = "One-Shot Gemma2"
    input_csv_path = f"results/comparison_{model}.csv"
    output_folder = "results"
    analyze_results(input_csv_path, output_folder, model, model_name)