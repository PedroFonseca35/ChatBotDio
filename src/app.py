import pandas as pd
import json
import requests
import streamlit as st
import random

# Configuração ollama serve
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "llama3:8b"

# Carregar dados
perfil = json.load(open('./data/perfil_investidor.json'))
produtos = json.load(open('./data/produtos_financeiros.json'))
transacoes = pd.read_csv('./data/transacoes.csv')
historico = pd.read_csv('./data/historico_atendimento.csv')

# Montar contexto
usuario = perfil['usuario']

contexto = f"""

Perfil: {usuario.get('perfil_investidor', 'N/A')}
Objetivo: {usuario.get('objetivo_principal', 'N/A')}
Reserva: {usuario.get('reserva_emergencia_atual','N/A')}

TRANSAÇÕES RECENTES:
{transacoes.sample(3).to_string(index=False)}

ATENDIMENTOS ANTERIORES:
{historico.sample(3).to_string(index=False)}

PRODUTOS DISPONÍVEIS:
{json.dumps(random.sample(produtos, 3), ensure_ascii=False)}
"""
# SYSTEM PROMPT
SYSTEM_PROMPT = """
Você é o LUMI, um educador financeiro amigável e didático. Seu meta é ajudar o cliente a tomar decisões com base em um determinado contexto.
Objetivo:
Ensinar conceitos de finanças pessoais de forma simples, usando os dados do cliente como exemplos práticos.
REGRAS:
Use apenas dados fornecidos
Não recomende investimentos específicos
Explique riscos
Linguagem simples
Não invente informações, admita: Não tenho essa informação
Não garantia de retorno financeiro
Não substitua orientação profissional (contador, assessor, etc.)
Não solicite ou utilize dados sensíveis
Não peça dados sensíveis
"""

# Chamar ollama
def perguntar(msg):
    prompt = f"""
    {SYSTEM_PROMPT}

    CONTEXTO DO CLIENTE:
    {contexto}

    Pergunta: {msg}"""
    r = requests.post(OLLAMA_URL, json={"model": MODELO, "prompt": prompt, "stream": False})
    return r.json()['response']

# Interface Streamlit
st.title("🎓 LUMI, Seu Educador Financeiro")

if pergunta := st.chat_input("Sua dúvida sobre finanças..."):
    st.chat_message("user").write(pergunta)
    with st.spinner("..."):
        st.chat_message("assistant").write(perguntar(pergunta))