import matplotlib.pyplot as plt
import pandas as pd

def interpret_results(output_csv_path, model_name):
    """
    Interpret the results by generating plots and examining low-COMET translations.

    Args:
        output_csv_path (str): Path to the output CSV file.
        model_name (str): Name of the model to include in output file names.
    """
    # Load the output CSV into a DataFrame
    df = pd.read_csv(output_csv_path)
    print("🔍 RAW CSV loaded:")  
    print(" • Shape:", df.shape)  

    # Remove leading/trailing brackets and convert directly
    df['comet_score'] = (
        df['comet_score']
        .str.strip('[]')      # "[0.93]" → "0.93"
        .astype(float)        # "0.93" → 0.93
    )
    
    # Now drop NaNs if any remain
    df = df.dropna(subset=['comet_score'])

    print("After droping NaN comet_score:", df.shape)

    # 1. Plot the distribution of COMET scores
    plt.figure(figsize=(10, 6))
    plt.hist(df['comet_score'].dropna(), bins=30, color='skyblue', edgecolor='black')
    plt.title(f'Distribution of COMET Scores ({model_name})')
    plt.xlabel('COMET Score')
    plt.ylabel('Frequency')
    plt.savefig(f'interpretations/comet_score_distribution_{model_name}.png')
    plt.close()

    # Ensure ground_truth_classification is not NaN
    df = df.dropna(subset=['ground_truth_classification'])

    # Ensure ground_truth_classification is treated as a categorical variable
    df['ground_truth_classification'] = df['ground_truth_classification'].astype('category')

    # Drop rows with invalid ground_truth_classification values
    df = df[df['ground_truth_classification'].notnull() & (df['ground_truth_classification'] != '')]

    print("After cleaning, DataFrame shape:", df.shape)
    print("Classes and counts:\n", df['ground_truth_classification'].value_counts(dropna=False))

    # 2. Plot COMET scores by hallucination classes
    plt.figure(figsize=(12, 8))
    df.boxplot(column='comet_score', by='ground_truth_classification', grid=False, showfliers=False)
    plt.title(f'COMET Scores by Hallucination Classes ({model_name})')
    plt.suptitle('')  # Remove the default title
    plt.xlabel('Hallucination Class')
    plt.ylabel('COMET Score')
    plt.savefig(f'interpretations/comet_scores_by_class_{model_name}.png')
    plt.close()

    # 3. Print a few low-COMET translations with model predictions
    low_comet_df = df.nsmallest(5, 'comet_score')
    print(f"Low-COMET Translations with Model Predictions ({model_name}):")
    for _, row in low_comet_df.iterrows():
        print(f"Source: {row['src_text']}")
        print(f"MT: {row['mt_text']}")
        print(f"Prediction: {row['prediction']}")
        print(f"COMET Score: {row['comet_score']}")
        print("---")

    # Save low-COMET translations to a text file
    low_comet_file = f"interpretations/low_comet_translations_{model_name}.txt"
    with open(low_comet_file, 'w', encoding='utf-8') as f:
        f.write(f"Low-COMET Translations with Model Predictions ({model_name}):\n")
        for _, row in low_comet_df.iterrows():
            f.write(f"Source: {row['src_text']}\n")
            f.write(f"MT: {row['mt_text']}\n")
            f.write(f"Prediction: {row['prediction']}\n")
            f.write(f"COMET Score: {row['comet_score']}\n")
            f.write("---\n")

    print(f"Low-COMET translations saved to {low_comet_file}")

# Example usage
if __name__ == "__main__":
    output_csv_path = "data/output_gemma2:2b.csv"  # Path to the output CSV file
    model_name = "gemma2:2b"
    interpret_results(output_csv_path, model_name)