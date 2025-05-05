import subprocess
import csv

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

# Example usage
if __name__ == "__main__":
    model_name = "llama3.1:latest"  # Updated to use a specific model available in Ollama

    # Get src_text and mt_text from the second row of data.csv
    csv_path = "data/data.csv"
    with open(csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        next(reader)  # Skip the first row
        second_row = next(reader)  # Get the second row
        src_text, mt_text = second_row['src_text'], second_row['mt_text']

    # Format the prompt with src_text and mt_text
    example_prompt = prompt + f"\nSource sentence: {src_text}\nTarget translation: {mt_text}\n"

    try:
        output = run_ollama(model_name, example_prompt)
        print("Model Output:", output)
    except RuntimeError as e:
        print(e)