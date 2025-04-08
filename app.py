
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Cálculo de Custo de Funcionário", layout="centered")

st.title("📊 Cálculo de Custo de Funcionário e Reserva Trabalhista")

# Função para calcular os custos
def calcular_custos(salario_bruto, beneficios):
    inss = salario_bruto * 0.268  # 20% patronal + 5,8% terceiros + 1% RAT
    fgts = salario_bruto * 0.08
    provisao_13 = salario_bruto / 12
    provisao_ferias = salario_bruto / 12
    provisao_ferias_1_3 = provisao_ferias / 3  # 1/3 constitucional
    multa_fgts = fgts * 0.4
    total_reserva = provisao_13 + provisao_ferias + provisao_ferias_1_3 + multa_fgts
    custo_total = salario_bruto + beneficios + inss + fgts + total_reserva

    return {
        "Salário Bruto": salario_bruto,
        "Benefícios": beneficios,
        "INSS Patronal": inss,
        "FGTS": fgts,
        "Provisão 13º": provisao_13,
        "Provisão Férias": provisao_ferias,
        "Provisão 1/3 Férias": provisao_ferias_1_3,
        "Multa FGTS": multa_fgts,
        "Reserva Total": total_reserva,
        "Custo Total": custo_total
    }

# Lista para armazenar dados dos funcionários
if "dados_funcionarios" not in st.session_state:
    st.session_state.dados_funcionarios = []

st.subheader("Adicionar Funcionário")

with st.form("funcionario_form"):
    nome = st.text_input("Nome do Funcionário")
    salario = st.number_input("Salário Bruto (R$)", min_value=0.0, format="%.2f")
    beneficios = st.number_input("Benefícios (R$)", min_value=0.0, format="%.2f")
    adicionar = st.form_submit_button("Adicionar")

if adicionar and nome and salario > 0:
    resultado = calcular_custos(salario, beneficios)
    resultado["Nome"] = nome
    st.session_state.dados_funcionarios.append(resultado)
    st.success(f"Funcionário {nome} adicionado!")

# Mostrar resultados
if st.session_state.dados_funcionarios:
    st.subheader("Funcionários Adicionados")
    df = pd.DataFrame(st.session_state.dados_funcionarios)
    df = df[["Nome", "Salário Bruto", "Benefícios", "INSS Patronal", "FGTS",
             "Provisão 13º", "Provisão Férias", "Provisão 1/3 Férias", "Multa FGTS",
             "Reserva Total", "Custo Total"]]
    # Seleciona apenas colunas numéricas para formatar
    numeric_cols = df.select_dtypes(include=['float', 'int']).columns
    st.dataframe(df.style.format({col: "R$ {:,.2f}" for col in numeric_cols}))


    # Botão para baixar CSV
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 Baixar Cálculo em CSV",
        data=csv,
        file_name='custo_funcionarios.csv',
        mime='text/csv'
    )
elseif: st.info("Adicione pelo menos um funcionário para ver o resultado.")
