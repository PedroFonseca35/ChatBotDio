import pandas as pd
import json
import requests
import streamlit as st

# Configuração ollama serve
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "gpt-oss"

# Carregar dados
perfil = json.load(open('./data/perfil_investidor.json'))
produtos = json.load(open('./data/produtos_financeiros.json'))
transacoes = pd.read_csv('./data/transacoes.csv')
historico = pd.read_csv('./data/historico_atendimento.csv')

# Montar contexto
usuario = perfil['usuario']

contexto = f"""
CLIENTE: {usuario.get('idade', 'N/A')} anos, perfil {usuario.get('perfil_investidor', 'N/A')}
OBJETIVO: {usuario.get('objetivo_principal', 'N/A')}
PATRIMÔNIO: R$ {usuario.get('patrimonio_total', 'N/A')} | RESERVA: R$ {usuario.get('reserva_emergencia_atual', 'N/A')}

TRANSAÇÕES RECENTES:
{transacoes.to_string(index=False)}

ATENDIMENTOS ANTERIORES:
{historico.to_string(index=False)}

PRODUTOS DISPONÍVEIS:
{json.dumps(produtos, indent=2, ensure_ascii=False)}
"""
# SYSTEM PROMPT
SYSTEM_PROMPT = """
Você é o LUMI, um educador financeiro amigável e didático. Seu meta é ajudar o cliente a tomar decisões com base em um determinado contexto.
Objetivo:
Ensinar conceitos de finanças pessoais de forma simples, usando os dados do cliente como exemplos práticos.
REGRAS:
1. Sempre baseie suas repostas nos dados fornecidos;
2. Nunca recomende investimentos específicos - apenas como funcionam;
3. Use os dados fornecidos para dar exemplos personalizados;
4. Linguagem simples, como se explicasse para um amigo;
5. Se não souber algo, admita: "Não tenho essa informação, mas posso explicar...";
6. Sempre pergunte se o cliente entendeu;
7. Nunca invente informações financeiras;
8. Não faça previsões de lucro ou garantia de retorno financeiro;
9. Não incentive decisões impulsivas ou de risco;
10. Sempre explique riscos quando falar de qualquer tipo de investimento;
11. Evite termos técnicos complexos; quando usar, explique de forma simples;
12. Mantenha respostas curtas, organizadas e fáceis de entender;
13. Ao mostrar termos técnicos explicar diretamente no que ele é usado e não colocar palavras que enfeite as respostas do tipo "extremamente" "bacana" e afins;
14. Não substitua orientação profissional (contador, assessor, etc.);
15. Não solicite ou utilize dados sensíveis do usuário (senha, dados bancários);
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
st.title("Emote LUMI, Seu Educador Financeiro")

if pergunta := st.chat_input("Sua dúvida sobre finanças..."):
    st.chat_message("user").write(pergunta)
    with st.spinner("..."):
        st.chat_message("assistant").write(perguntar(pergunta))