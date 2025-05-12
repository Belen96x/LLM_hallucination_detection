import subprocess
import csv
import time
from hall_detection import prompt

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
        result = subprocess.run(
            ["ollama", "run", model],
            input=prompt,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )

        print("Command executed:", result.args)
        print("Return code:", result.returncode)
        #print("Standard Output:", result.stdout.encode('utf-8', errors='ignore').decode('utf-8'))
        #print("Standard Error:", result.stderr.encode('utf-8', errors='ignore').decode('utf-8'))

        if result.returncode != 0:
            raise RuntimeError(f"Ollama error: {result.stderr}")

        return result.stdout.strip()

    except FileNotFoundError:
        raise RuntimeError("Ollama CLI is not installed. Please install it from https://ollama.ai.")


def process_all_rows(file_path, output_path, model_name):
    """
    Process each row from input CSV using Ollama and save predictions to output CSV.

    Args:
        file_path (str): Path to the input CSV file.
        output_path (str): Path to the output CSV file.
        model_name (str): Ollama model name (e.g., 'gemma2:2b').
    """
    with open(file_path, mode='r', encoding='utf-8') as infile, open(output_path, mode='w', encoding='utf-8', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['prediction', 'prediction_class']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        writer.writeheader()
        rows = list(reader)
        total_rows = len(rows)

        for index, row in enumerate(rows):
            src_text = row['src_text']
            mt_text = row['mt_text']

            formatted_prompt = prompt + f"\nSource sentence: {src_text}\nTarget translation: {mt_text}\n"

            try:
                model_output = run_ollama(model_name, formatted_prompt)

                output_lines = model_output.split('\n')
                result = output_lines[0].strip()
                classification = output_lines[1].strip() if len(output_lines) > 1 else ""

                row['prediction'] = result
                row['prediction_class'] = classification

                writer.writerow(row)

                progress = ((index + 1) / total_rows) * 100
                print(f"Progress: {progress:.2f}% completed", end='\r')

            except RuntimeError as e:
                print(f"Error processing row {index}: {e}")
                continue

        print("\nProcessing complete.")


# Example usage
if __name__ == "__main__":
    model_name = "qwen:latest"
    input_csv_path = "data/data_filtered.csv"
    output_csv_path = f"data/output_v2_qwen.csv"

    process_all_rows(input_csv_path, output_csv_path, model_name)