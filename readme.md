---------
TO - DO :
---------


1. Idioma elegido - Inglés, español y español, inglés. - DONE
2. Limpiar datos y hacer subselección - DONE (Limpiar más?)
3. Elegir los modelos (2 LLMs)
4. Diseñar el prompt para detectar alucinaciones (Al momento de ejecutarlo, tenemos que sacarle las <<< >>>. Hay una columa con traducción pura no marcada). Pedirle que ponga la parte alucinada entre <<< >>>, comparar los fragmentos detectados. - Done (Pulirlo cuando esté la clase para la ejecución)
5. Comparar el resultado del modelo con la human annotation del dataset.
6. Calcular las métricas de performance

# Activate the virtual environment
source venv/bin/activate

# Install Ollama CLI 
# For macOS, you can use Homebrew:
# brew install ollama

# Verify installation
ollama --version
