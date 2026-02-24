import streamlit as st
from datetime import datetime, timedelta

# Configuração da Página
st.set_page_config(page_title="Barbearia Premium", page_icon="✂️")

# CSS Personalizado para o Estilo Branco e Dourado
st.markdown("""
    <style>
    .main { background-color: #FFFFFF; }
    h1 { color: #1A1A1A; border-bottom: 2px solid #D4AF37; padding-bottom: 10px; }
    .stButton>button {
        background-color: #D4AF37;
        color: #1A1A1A;
        border-radius: 5px;
        border: none;
        font-weight: bold;
        width: 100%;
    }
    .stButton>button:hover { border: 1px solid #1A1A1A; color: #000000; }
    </style>
    """, unsafe_allow_html=True)

st.title("✂️ BARBEARIA PREMIUM")
st.subheader("Gestão de Agendamentos Exclusivos")

# Inicializar agenda se não existir
if 'agenda' not in st.session_state:
    st.session_state.agenda = []

# Interface de Input
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        nome = st.text_input("Nome do Cliente")
        data = st.date_input("Data do Atendimento")
    
    with col2:
        horario = st.time_input("Horário de Início")
        
    if st.button("Confirmar Agendamento Ouro"):
        if nome:
            # Lógica de tempo
            inicio = datetime.combine(data, horario)
            fim = inicio + timedelta(minutes=45)
            
            # Verificar Conflitos
            conflito = False
            for ag in st.session_state.agenda:
                if (inicio < ag['fim']) and (fim > ag['inicio']):
                    conflito = True
                    break
            
            if conflito:
                st.error("⚠️ Este horário conflita com outro agendamento!")
            else:
                st.session_state.agenda.append({"nome": nome, "inicio": inicio, "fim": fim})
                st.success(f"✅ Agendado com sucesso para {nome}!")
        else:
            st.warning("Por favor, insira o nome do cliente.")

# Exibição dos Agendamentos
st.markdown("---")
st.write("### 📅 Próximos Clientes")

if not st.session_state.agenda:
    st.info("Nenhum agendamento para hoje.")
else:
    # Ordenar por horário
    st.session_state.agenda.sort(key=lambda x: x['inicio'])
    
    for ag in st.session_state.agenda:
        with st.expander(f"{ag['inicio'].strftime('%H:%M')} - {ag['nome']}"):
            st.write(f"**Término previsto:** {ag['fim'].strftime('%H:%M')}")
            st.write(f"**Data:** {ag['inicio'].strftime('%d/%m/%Y')}")
