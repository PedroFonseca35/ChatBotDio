# Tecnologias da Aplicação

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
# Instalar gpt-oss terminal
ollama pull llama3:8b
# Iniciar o ollama terminal
ollama run llama3:8b
# Desintalar terminal
ollama rm llama3:8b
# Server Ollama terminal
ollama serve
# Instalar dependências
pip install streamlit pandas requests
# Rodar a aplicação
stremlit run .\src\app.py
```