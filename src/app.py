import pandas as pd
import json
import requests
import streamlit as st
import random

# Configuração ollama serve
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "llama3:8b"

# Carregar dados
renda = json.load(open('./data/tipos_de_renda.json'))
investimentos = json.load(open('./data/metas_investimento.json'))
transacoes = pd.read_csv('./data/exemplo_de_transacoes.csv')
atendimento = pd.read_csv('./data/exemplo_atendimento.csv')

# Montar contexto

contexto = f"""
EXEMPLO DE INVESTIMENTOS
{json.dumps(random.sample(renda, 2), ensure_ascii=False)}

EXEMPLO DE GASTOS:
{transacoes.sample(3).to_string(index=False)}

EXEMPLO ATENDIMENTO:
{atendimento.sample(3).to_string(index=False)}

METAS DE INVESTIMENTO:
{json.dumps(random.sample(investimentos, 2), ensure_ascii=False)}
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
Linguagem simples, curta e objetiva
Não invente informações, admita: Não tenho essa informação
Não garantia de retorno financeiro
Não substitua orientação profissional (contador, assessor, etc.)
Não solicite ou utilize dados sensíveis
Não peça dados sensíveis
Se o usuário apenas cumprimentar (oi, olá etc), apenas cumprimente e pergunte qual dúvida financeira ele tem
Se a pergunta não for sobre finanças, diga que você atende apenas temas financeiros
"""

# Chamar ollama
def perguntar(msg):
    prompt = f"""
    {SYSTEM_PROMPT}

    O contexto abaixo são exemplos didáticos e não representam o usuário atual
    Não assuma que o usuário possui esse perfil
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