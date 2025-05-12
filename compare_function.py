import csv
import re
from comet import download_model, load_from_checkpoint

# Load the COMET model
try:
    comet_model_path = download_model("Unbabel/wmt22-comet-da")
    comet_model = load_from_checkpoint(comet_model_path)
except Exception as e:
    print(f"Error loading COMET model: {e}")
    comet_model = None

def calculate_comet_score(src_text, mt_text, ref_text):
    """
    Calculate the COMET score for the given source, machine-translated, and reference texts.

    Args:
        src_text (str): The source text.
        mt_text (str): The machine-translated text.
        ref_text (str): The reference text.

    Returns:
        float: The COMET score.
    """
    if comet_model is None:
        return None

    data = [{"src": src_text, "mt": mt_text, "ref": ref_text}]
    scores = comet_model.predict(data, batch_size=1, gpus=1)
    return scores[0]

def check_labels(input_file, output_file):
    """
    Check if the `ground_truth_classification` and `raw_output` columns have the same label,
    calculate COMET scores for hallucinated spans, and save the results to a CSV file.

    Args:
        input_file (str): Path to the input CSV file.
        output_file (str): Path to the output CSV file.
    """
    with open(input_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        fieldnames = ['src_text', 'mt_text', 'ground_truth_classification', 'predicted_label', 'match', 'comet_score']

        with open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                ground_truth_label = row['ground_truth_classification']

                # Extract the label from the raw_output column using regex
                raw_output_match = re.search(r'(\d+_[A-Za-z]+_hallucination)', row['raw_output'])
                predicted_label = raw_output_match.group(1) if raw_output_match else None

                # Check if the labels match
                match = ground_truth_label == predicted_label

                # Extract hallucinated spans from mt_text and raw_output
                mt_hallucinated = re.findall(r'<<<(.*?)>>>', row['ground_truth_text'])
                raw_hallucinated = re.findall(r'<<<(.*?)>>>', row['raw_output'])
                print(f"mt_hallucinated: {mt_hallucinated}")
                print(f"raw_hallucinated: {raw_hallucinated}")

                # Calculate COMET score for hallucinated spans
                comet_score = None
                if mt_hallucinated and raw_hallucinated:
                    comet_score = calculate_comet_score(
                        src_text=row['src_text'],
                        mt_text=" ".join(mt_hallucinated),
                        ref_text=" ".join(raw_hallucinated)
                    )

                # Write the result to the output file
                writer.writerow({
                    'src_text': row['src_text'],
                    'mt_text': row['mt_text'],
                    'ground_truth_classification': ground_truth_label,
                    'predicted_label': predicted_label,
                    'match': match,
                    'comet_score': comet_score
                })

# Example usage
if __name__ == "__main__":
    input_csv_path = "data/output_zeroshot_llama3.csv"
    output_csv_path = "results/comparison_zeroshot_llama3.csv"
    check_labels(input_csv_path, output_csv_path)