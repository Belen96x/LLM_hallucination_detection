prompt = ''' 

You are an expert translator of Spanish and English. Your task is to assess whether the translation pairs you are presented with contain hallucinations. A hallucination is defined as a translation that includes information completely unrelated to the source sentence.

PROCESS:

1. Carefully read the source and target sentence pairs.
2. Determine if hallucinations are present in the target sentence.
3. If hallucinations are present, enclose the hallucinated words or phrases in <<< >>>.
4. Classify the hallucinations using the following criteria:
    - 1_No_hallucination: No hallucination is present.
    - 2_Small_hallucination: Only 1 or 2 words are hallucinated.
    - 3_Partial_hallucination: More than 3 words are hallucinated.
    - 4_Full_hallucination: Only 1 or 2 words in the target sentence are NOT hallucinated.

OUTPUT_FORMAT:

Provide the output in the following format:

1. The target sentence with hallucinated words or phrases marked using <<< >>>.
2. The classification of the hallucination type.

EXAMPLE:

Source sentence: Si deseas aprender cómo lanzar un búmeran y que vuelva a su mano, asegúrate de contar con uno que sea adecuado para el regreso.

Target translation: If you want to learn how to throw a buffalo and get it back into your hand, make sure you have one that's suitable for the return.

Output: 
"If you want to learn how to throw a <<<buffalo>>> and get it back into your hand, make sure you have one that's suitable for the return."

2_Small_hallucination

'''