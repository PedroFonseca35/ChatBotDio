# Tecnologias da Aplicação
LUMI(Linguagem Unificada e Mentoria em Investimentos)
```
Python + Streamlit + Ollama + llama3
```

Instalar o ollama.com
models -> gpt-oss
ollama pull gpt-oss:20b
ollama run gpt-oss
ollama serve

## Como Rodar

```bash
# Instalar llama3 terminal
ollama pull llama3:8b
# Iniciar o llama3 no terminal
ollama run llama3:8b
# Desintalar terminal
ollama rm llama3:8b
# Server Ollama terminal
ollama serve
# Instalar dependências
pip install streamlit pandas requests
python -m streamlit run .\src\app.py
# Rodar a aplicação
streamlit run .\src\app.py
python -m streamlit run .\src\app.py
```

```bash
# Instalar llama3 terminal
ollama pull gemma2:2b
# Desintalar terminal
ollama rm gemma2:2b

===

ollama pull qwen2.5:3b
ollama rm qwen2.5:3b
```