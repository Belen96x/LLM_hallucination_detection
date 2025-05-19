# MT Hallucination Detection Project

## Overview
This repository contains code and data for evaluating hallucination detection in machine translation (MT) outputs using large language models (LLMs). We compare one-shot and zero-shot prompting strategies across two models—Gemma2 and LLaMA3—against human annotations. The goal is to assess LLM-based methods for identifying hallucinated segments in translated text.


## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Belen96x/MT_final_project
   cd mt-hallucination-detection

2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

## Usage
1. Run Detection

python ollama_integration.py \
  --model llama3.1:latest \
  --prompt-module hall_detection_oneshot \
  --input data/data_filtered.csv \
  --output results/output_llama3_oneshot.csv

- The model can be changed for the ones available in Ollama.
- The prompt modules available are:
    - hall_detection_oneshot
    - hall_detection_zeroshot
- The input can be changed but needs to ensure to have the needed columns.

2. Compare with human labels

python compare_function.py \
  --input data/output_llama3_oneshot.csv \
  --output results/comparison_oneshot_llama3.csv

- Be sure to match the input file path with the one created in the previous step.

3. Analyze Results

python results_analysis.py \
  --model zeroshot_llama3 \
  --model-name "Zero-Shot Llama3" \
  --input results/comparison_zeroshot_llama3.csv \
  --output-folder results

- The prompt "model" will integrate the name of the output files.
- The "model-name" will be the one show in the plots.
- Be sure to match the "input" with the one created in the previous step.

## Integration with Ollama
The ollama_integration.py module provides helper functions for sending prompts to LLMs via the Ollama API. Configure your Ollama endpoint and API key in the script or via environment variables.

## Results
Summary statistics and figures generated in the results folder illustrate classification accuracy, correlation with COMET scores, and overlap tagging distributions.

Detailed CSVs in comparison/ record exact match rates, partial matches, false positives, and false negatives.

## Contributing
Contributions are welcome! Please open issues or pull requests for improvements.

## Authors
[Belén Saavedra](https://github.com/Belen96x)
[Juliana Planas](https://github.com/julianaplanas)







