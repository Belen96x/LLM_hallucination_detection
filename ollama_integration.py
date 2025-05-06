import subprocess
import csv
import time
from comet import download_model, load_from_checkpoint

def run_ollama(model: str, prompt: str) -> str:
    """
    Run an Ollama model locally with the given prompt.

    Args:
        model (str): The name of the Ollama model to use (e.g., 'llama', 'mistral').
        prompt (str): The input prompt for the model.

    Returns:
        str: The model's output.
    """
    try:
        # Run the Ollama CLI command
        result = subprocess.run(
            ["ollama", "run", model],
            input=prompt,
            capture_output=True,
            text=True
        )

        # Debugging: Print the command and its output
        print("Command executed:", result.args)
        print("Return code:", result.returncode)
        print("Standard Output:", result.stdout)
        print("Standard Error:", result.stderr)

        # Check for errors
        if result.returncode != 0:
            raise RuntimeError(f"Ollama error: {result.stderr}")

        return result.stdout.strip()

    except FileNotFoundError:
        raise RuntimeError("Ollama CLI is not installed. Please install it from https://ollama.ai.")

# Load the first row from data.csv
def get_first_row_data(file_path):
    """
    Reads the first row of the CSV file and extracts src_text and mt_text.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        tuple: A tuple containing src_text and mt_text.
    """
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        first_row = next(reader)
        return first_row['src_text'], first_row['mt_text']

# Update the prompt to use hall_detection's prompt
from hall_detection import prompt

try:
    # Attempt to load the COMET model
    comet_model_path = download_model("Unbabel/wmt22-comet-da")
    comet_model = load_from_checkpoint(comet_model_path)
except Exception as e:
    print(f"Error loading COMET model: {e}")
    comet_model = None  # Set to None to prevent further errors

def calculate_comet_score(src_text, mt_text, ref_text):
    """
    Calculate the COMET score for a given source and machine-translated text.

    Args:
        src_text (str): The source text.
        mt_text (str): The machine-translated text.

    Returns:
        float: The COMET score.
    """
    data = [{"src": src_text, "mt": mt_text, "ref": ref_text}]
    comet_scores = comet_model.predict(data, batch_size=1, gpus=1)
    return comet_scores[0]

def process_all_rows(file_path, output_path, model_name):
    """
    Process all rows in the dataset and store results in a CSV file.

    Args:
        file_path (str): Path to the input CSV file.
        output_path (str): Path to the output CSV file.
        model_name (str): The name of the Ollama model to use.
    """
    with open(file_path, mode='r', encoding='utf-8') as infile, open(output_path, mode='w', encoding='utf-8', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = ['src_lang', 'tgt_lang', 'src_text', 'mt_text', 'ground_truth', 'ground_truth_classification', 'prediction', 'prediction_class', 'comet_score', 'ref']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        # Write header to the output file
        writer.writeheader()

        rows = list(reader)
        total_rows = len(rows)

        for index, row in enumerate(rows):
            src_lang = row['src_lang']
            tgt_lang = row['tgt_lang']
            src_text = row['src_text']
            mt_text = row['mt_text']
            ground_truth = row['hall_spans']  # Rename hall_spans to ground_truth
            ref_text = ground_truth  # Use ground_truth directly as ref_text
            ground_truth_classification = row['class_hall']  # Rename class_hall to ground_truth_classification

            # Format the prompt with src_text and mt_text
            formatted_prompt = prompt + f"\nSource sentence: {src_text}\nTarget translation: {mt_text}\n"

            try:
                # Get the model output
                model_output = run_ollama(model_name, formatted_prompt)

                # Parse the output into result and classification
                output_lines = model_output.split('\n')
                result = output_lines[0].strip()
                classification = output_lines[1].strip() if len(output_lines) > 1 else ""

                # Calculate COMET score
                comet_score = calculate_comet_score(src_text, mt_text, ref_text)

                # Add results to the row and write to the output file
                row['output'] = result
                row['classification'] = classification
                row['prediction'] = row['mt_text_normalized']  # Assuming this contains the <<<>>> marked sentence
                row['prediction_class'] = row['class_hall']  # Assuming the classification remains the same
                row['comet_score'] = comet_score
                writer.writerow({
                    'src_lang': src_lang,
                    'tgt_lang': tgt_lang,
                    'src_text': src_text,
                    'mt_text': mt_text,
                    'ground_truth': ground_truth,
                    'ground_truth_classification': ground_truth_classification,
                    'prediction': row['prediction'],
                    'prediction_class': row['prediction_class'],
                    'comet_score': row['comet_score'],
                    'ref': ref_text,
                })

                # Print progress percentage
                progress = ((index + 1) / total_rows) * 100
                print(f"Progress: {progress:.2f}% completed", end='\r')

            except RuntimeError as e:
                print(f"Error processing row: {row}")
                print(e)

        print("\nProcessing complete.")

# Example usage
if __name__ == "__main__":
    model_name = "llama3.1:latest"  # Updated to use a specific model available in Ollama
    input_csv_path = "data/data.csv"
    output_csv_path = f"data/output_{model_name}.csv"  # Dynamically set output file name based on model_name

    process_all_rows(input_csv_path, output_csv_path, model_name)