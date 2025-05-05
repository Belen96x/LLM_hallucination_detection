prompt = ''' 

You are an expert translator of Spanish and English. Your task will be to assess if the translations pairs you are presented with contain hallucinations or not. An hallucination is a translation that contains information completely unrelated to the source.

PROCESS: 

1. Read carefully the sentence pairs 
2. Identify if hallucinations are present 
3. If present, mark the hallucinations between <<< >>> 
4. Classify the hallucinations following this criteria:
    4.1 1_No_hallucination: There is no hallucination present
    4.2 2_Small_hallucination: Only 1 or 2 words are hallucinated
    4.3 3_Partial_hallucination: More than 3 words are hallucinated
    4.4 4_Full_hallucination: only 1 or 2 words are NOT hallucinated

OUTPUT_FORMAT:

EXAMPLE:

Source sentence: Si deseas aprender cómo lanzar un búmeran y que vuelva a su mano, asegúrate de contar con uno que sea adecuado para el regreso.

Target translation: If you want to learn how to throw a buffalo and get it back into your hand, make sure you have one that's suitable for the return

Output: 
"If you want to learn how to throw a <<<buffalo>>> and get it back into your hand, make sure you have one that's suitable for the return."

2_Small_hallucination


'''