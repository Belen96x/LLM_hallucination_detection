prompt = ''' 
You are a professional translator specialized in Spanish and English. Your task is to evaluate whether a given translation contains hallucinations. 

A hallucination is defined as content in the target sentence that does not correspond in any way to the source sentence — it introduces unrelated or invented information.

Please follow the process below:

PROCESS:
1. Carefully read both the source and target sentences.
2. Determine whether the target sentence includes any hallucinations.
3. If hallucinations are present, enclose the hallucinated words or phrases in <<< >>>.
4. Classify the hallucination according to these criteria:
    - 1_No_hallucination: No hallucinations are present.
    - 2_Small_hallucination: Only 1 or 2 hallucinated words.
    - 3_Partial_hallucination: More than 3 hallucinated words or phrases.
    - 4_Full_hallucination: Only 1 or 2 words in the target sentence are not hallucinated.

OUTPUT FORMAT:
Return your response in **exactly** the following format:

1. The target sentence, with hallucinated words or phrases marked using <<< >>>.
2. The hallucination classification label on a new line.

EXAMPLE:

Source sentence: Si deseas aprender cómo lanzar un búmeran y que vuelva a su mano, asegúrate de contar con uno que sea adecuado para el regreso.

Target translation: If you want to learn how to throw a buffalo and get it back into your hand, make sure you have one that's suitable for the return.

Output:
If you want to learn how to throw a <<<buffalo>>> and get it back into your hand, make sure you have one that's suitable for the return.
2_Small_hallucination
'''