import subprocess

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

# Example usage
if __name__ == "__main__":
    model_name = "llama3.1:latest"  # Updated to use a specific model available in Ollama
    example_prompt = "Translate the following sentence and detect hallucinations: 'Hola, ¿cómo estás?'"

    try:
        output = run_ollama(model_name, example_prompt)
        print("Model Output:", output)
    except RuntimeError as e:
        print(e)