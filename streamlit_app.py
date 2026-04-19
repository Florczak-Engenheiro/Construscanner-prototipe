import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time

# ========== CONFIGURAÇÃO DA PÁGINA ==========
st.set_page_config(
    page_title="Construscanner - Monitoramento de Obras",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cores da marca Construscanner
CORES = {
    "azul_principal": "#003D7A",
    "azul_claro": "#1BA3D6",
    "verde": "#7CB342",
    "amarelo": "#FFC107",
    "turquesa": "#00BCD4",
    "branco": "#FFFFFF",
    "cinza_claro": "#F5F7FA",
    "cinza_escuro": "#1a1a1a",
    "preto": "#000000"
}

# ========== CUSTOM CSS ==========
st.markdown(f"""
    <style>
    /* Background e tema geral */
    .stApp {{
        background-color: {CORES['cinza_claro']};
    }}
    
    /* Main container */
    .main {{
        padding: 0;
    }}
    
    /* Headers */
    h1, h2, h3, h4 {{
        color: {CORES['azul_principal']} !important;
        font-weight: 700;
    }}
    
    /* Texto padrão */
    body, p, span, div {{
        color: {CORES['cinza_escuro']} !important;
    }}
    
    /* Cards e containers */
    [data-testid="column"] {{
        background: {CORES['branco']};
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0, 61, 122, 0.08);
        margin: 8px;
    }}
    
    /* Métricas */
    [data-testid="metric-container"] {{
        background: linear-gradient(135deg, {CORES['branco']} 0%, #FAFBFC 100%);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0, 61, 122, 0.08);
        border-left: 4px solid {CORES['azul_claro']};
    }}
    
    /* Sidebar */
    [data-testid="stSidebar"] {{
        background: {CORES['azul_principal']};
    }}
    
    [data-testid="stSidebar"] label {{
        color: #000 !important;
        font-weight: 600;
    }}
    
    [data-testid="stSidebar"] p {{
        color: #000 !important;
    }}
    
    /* Botões */
    .stButton > button {{
        background-color: {CORES['azul_claro']};
        color: {CORES['branco']};
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.3s ease;
    }}
    
    .stButton > button:hover {{
        background-color: {CORES['azul_principal']};
        box-shadow: 0 4px 12px rgba(0, 61, 122, 0.2);
    }}
    
    /* Radio buttons */
    [role="radio"] {{
        accent-color: {CORES['azul_claro']};
    }}
    
    /* Sliders */
    .stSlider > div[data-baseweb="slider"] > div {{
        background: {CORES['azul_claro']};
    }}
    
    /* Info boxes */
    [data-testid="infoContainer"] {{
        background-color: #E3F2FD !important;
        border-left: 5px solid {CORES['azul_claro']} !important;
    }}
    
    [data-testid="infoContainer"] p {{
        color: {CORES['azul_principal']} !important;
    }}
    
    /* Warning boxes */
    [data-testid="stWarning"] {{
        background-color: #FFF3E0 !important;
        border-left: 5px solid {CORES['amarelo']} !important;
    }}
    
    [data-testid="stWarning"] p {{
        color: {CORES['cinza_escuro']} !important;
    }}
    
    /* Tabelas */
    [data-testid="dataframe"] {{
        border-radius: 8px;
        overflow: hidden;
    }}
    
    [data-testid="dataframe"] th {{
        background-color: {CORES['azul_principal']} !important;
        color: {CORES['branco']} !important;
        font-weight: 700;
    }}
    
    [data-testid="dataframe"] td {{
        color: {CORES['cinza_escuro']} !important;
    }}
    
    /* Dividers */
    hr {{
        border-color: {CORES['azul_claro']};
    }}
    
    /* Links */
    a {{
        color: {CORES['azul_claro']} !important;
        text-decoration: none;
    }}
    
    a:hover {{
        color: {CORES['azul_principal']} !important;
        text-decoration: underline;
    }}
    </style>
""", unsafe_allow_html=True)

# ========== SIDEBAR ==========
with st.sidebar:
    st.markdown(f"""
        <div style="padding: 20px; text-align: center; border-bottom: 2px solid {CORES['amarelo']};">
            <h1 style="color: {CORES['azul_principal']}; margin: 0;">🏗️</h1>
            <h2 style="color: {CORES['azul_principal']}; margin: 10px 0 0 0; font-size: 1.5em;">Construscanner</h2>
            <p style="color: {CORES['azul_principal']}; margin: 5px 0 0 0; font-size: 0.9em;">Sistema Inteligente de Monitoramento</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navegação
    st.write("### 📊 Navegação")
    view_option = st.radio(
        "Selecione a visualização:",
        ["📈 Dashboard", "📷 Câmeras", "🚨 Alertas", "📋 Relatórios", "ℹ️ Sobre"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Configurações
    st.write("### ⚙️ Configurações")
    refresh_speed = st.slider(
        "🔄 Atualização (segundos):",
        min_value=1,
        max_value=10,
        value=3,
    )
    
    st.markdown("---")
    
    # Status do Sistema
    st.write("### 📡 Status do Sistema")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Câmeras", "6/6", "+6")
    with col2:
        st.metric("Sensores", "12/12", "+12")
    
    st.markdown("---")
    st.caption("© 2024 Construscanner | Engenharia & IA")

# ========== HEADER PRINCIPAL ==========
st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {CORES['azul_principal']} 0%, {CORES['azul_claro']} 100%);
        padding: 40px 20px;
        border-radius: 12px;
        margin-bottom: 30px;
        text-align: center;
        box-shadow: 0 8px 20px rgba(0, 61, 122, 0.15);
    ">
        <h1 style="color: {CORES['branco']}; margin: 0; font-size: 2.5em;">🏗️ Monitoramento em Tempo Real</h1>
        <p style="color: {CORES['amarelo']}; margin: 10px 0 0 0; font-size: 1.1em; font-weight: 600;">
            Sistema Inteligente de Monitoramento de Canteiros com IA
        </p>
    </div>
""", unsafe_allow_html=True)

# ========== FUNÇÕES AUXILIARES ==========
def gerar_dados_dashboard():
    return {
        "produtividade": np.random.randint(60, 86),
        "maquinas": np.random.randint(7, 12),
        "trabalhadores": np.random.randint(20, 29),
        "alertas": np.random.randint(1, 6),
        "temperatura": np.random.randint(25, 33),
        "armazenamento": np.random.randint(80, 95),
    }

def gerar_dados_produtividade():
    dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
    dados = []
    for dia in dias:
        dados.append({"Dia": dia, "Produtividade": np.random.randint(65, 85)})
    return pd.DataFrame(dados)

def gerar_alertas():
    return [
        {"tipo": "🔴 Crítico", "titulo": "Equipamento Parado Há Tempo Excessivo", 
         "desc": "Pá Carregadeira P1 parada há 35 minutos", "tempo": "5 min atrás", "sev": "critical"},
        {"tipo": "🟠 Aviso", "titulo": "Temperatura Elevada", 
         "desc": "Temperatura ambiente atingiu 28°C", "tempo": "12 min atrás", "sev": "warning"},
        {"tipo": "🟠 Aviso", "titulo": "Baixa Produtividade", 
         "desc": "Produtividade 8% abaixo da meta", "tempo": "23 min atrás", "sev": "warning"},
        {"tipo": "🔵 Info", "titulo": "Sincronização de Dados", 
         "desc": "Upload completado - 2.3 GB processados", "tempo": "1 hora atrás", "sev": "info"},
        {"tipo": "🔵 Info", "titulo": "Novo Trabalhador Detectado", 
         "desc": "Sistema detectou novo trabalhador no canteiro", "tempo": "2 horas atrás", "sev": "info"},
    ]

# ========== DASHBOARD VIEW ==========
if "Dashboard" in view_option:
    # Métricas principais
    st.markdown("### 📊 Métricas em Tempo Real")
    dados = gerar_dados_dashboard()
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.metric("📈 Produtividade", f"{dados['produtividade']}%", "+2%")
    with col2:
        st.metric("⚙️ Máquinas", dados['maquinas'], "-1")
    with col3:
        st.metric("👥 Trabalhadores", dados['trabalhadores'], "+3")
    with col4:
        st.metric("⚠️ Alertas", dados['alertas'], "+1")
    with col5:
        st.metric("🌡️ Temperatura", f"{dados['temperatura']}°C", "-2°C")
    with col6:
        st.metric("💾 Armazenamento", f"{dados['armazenamento']}%", "+5%")
    
    st.markdown("---")
    
    # Seção de Máquinas e Produtividade
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.markdown("### 🗺️ Localização de Máquinas")
        st.info("""
        **Máquinas em Operação:**
        
        🟢 **E1** - Escavadeira 1 ✅ OPERANDO  
        🟢 **E2** - Escavadeira 2 ✅ OPERANDO  
        🟠 **P1** - Pá Carregadeira ⏸️ PARADA  
        🟢 **R1** - Rolo Compactador ✅ OPERANDO  
        🟢 **C1** - Caminhão 1 ✅ OPERANDO  
        """)
    
    with col_right:
        st.markdown("### 📊 Produtividade")
        st.metric("Total", "10", "Máquinas")
        st.metric("Ativas", dados['maquinas'], "Operando")
    
    st.markdown("---")
    
    # Gráfico de Produtividade Semanal
    st.markdown("### 📈 Produtividade Semanal")
    df_prod = gerar_dados_produtividade()
    st.bar_chart(df_prod.set_index("Dia"))
    
    st.markdown("---")
    st.caption(f"⏱️ Última atualização: {datetime.now().strftime('%H:%M:%S')}")
    
    # Auto-refresh
    if st.button("🔄 Atualizar Agora"):
        st.rerun()
    
    time.sleep(refresh_speed)
    st.rerun()

# ========== CÂMERAS VIEW ==========
elif "Câmeras" in view_option:
    st.markdown("### 📷 Monitoramento por Câmeras")
    st.write(f"<span style='background: {CORES['verde']}; color: white; padding: 8px 16px; border-radius: 8px; font-weight: bold;'>● AO VIVO</span>", unsafe_allow_html=True)
    
    cameras = [
        {"id": 1, "nome": "Câmera 1", "local": "Entrada Principal"},
        {"id": 2, "nome": "Câmera 2", "local": "Zona de Escavação"},
        {"id": 3, "nome": "Câmera 3", "local": "Zona de Compactação"},
        {"id": 4, "nome": "Câmera 4", "local": "Escritório Temporário"},
        {"id": 5, "nome": "Câmera 5", "local": "Acesso Sul"},
        {"id": 6, "nome": "Câmera 6", "local": "Vista Aérea (Drone)"},
    ]
    
    cols = st.columns(3)
    for idx, cam in enumerate(cameras):
        with cols[idx % 3]:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, {CORES['cinza_claro']} 0%, {CORES['branco']} 100%);
                border-radius: 12px;
                padding: 25px;
                text-align: center;
                margin: 10px 0;
                border: 2px solid {CORES['azul_claro']};
                box-shadow: 0 4px 12px rgba(0, 61, 122, 0.1);
            ">
                <div style="font-size: 3em; margin: 15px 0;">📹</div>
                <h4 style="color: {CORES['azul_principal']}; margin: 10px 0;">{cam['nome']}</h4>
                <p style="color: {CORES['cinza_escuro']}; margin: 8px 0; font-size: 0.95em;">{cam['local']}</p>
                <div style="
                    background: {CORES['verde']};
                    color: white;
                    padding: 8px 12px;
                    border-radius: 6px;
                    font-size: 0.85em;
                    display: inline-block;
                    font-weight: bold;
                    margin-top: 10px;
                ">
                    ● CONECTADA
                </div>
            </div>
            """, unsafe_allow_html=True)

# ========== ALERTAS VIEW ==========
elif "Alertas" in view_option:
    st.markdown("### 🚨 Alertas em Tempo Real")
    
    alertas = gerar_alertas()
    
    for alerta in alertas:
        cor_sev = {
            "critical": CORES['azul_principal'],
            "warning": CORES['amarelo'],
            "info": CORES['azul_claro']
        }[alerta["sev"]]
        
        cor_bg = {
            "critical": "#FFEBEE",
            "warning": "#FFF3E0",
            "info": "#E3F2FD"
        }[alerta["sev"]]
        
        st.markdown(f"""
        <div style="
            background: {cor_bg};
            border-left: 5px solid {cor_sev};
            padding: 18px;
            border-radius: 8px;
            margin: 12px 0;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        ">
            <h4 style="color: {CORES['azul_principal']}; margin: 0 0 8px 0;">{alerta['tipo']} {alerta['titulo']}</h4>
            <p style="color: {CORES['cinza_escuro']}; margin: 5px 0; font-weight: 500;">{alerta['desc']}</p>
            <small style="color: #888; font-weight: 500;">{alerta['tempo']}</small>
        </div>
        """, unsafe_allow_html=True)

# ========== RELATÓRIOS VIEW ==========
elif "Relatórios" in view_option:
    st.markdown("### 📈 Relatórios e Estatísticas")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Média de Produtividade", "72%", "+5%")
    with col2:
        st.metric("Máquinas Ativas", "4/5", "-1")
    with col3:
        st.metric("Eficiência", "85%", "+2%")
    
    st.markdown("---")
    
    df_relatorio = pd.DataFrame({
        "Data": pd.date_range(start="2024-01-01", periods=10),
        "Produtividade": np.random.randint(60, 85, 10),
        "Alertas": np.random.randint(1, 8, 10),
    })
    
    st.markdown("### 📊 Evolução Temporal")
    st.line_chart(df_relatorio.set_index("Data"))
    
    st.markdown("---")
    st.markdown("### 📋 Resumo Estático")
    
    resumo_data = {
        "📊 Total de Medições": "1,240",
        "⏱️ Horas de Operação": "328h",
        "🚨 Total de Alertas": "45",
        "✅ Operações Normais": "95%",
        "💾 Dados Armazenados": "12.5 GB",
        "🔄 Taxa de Sincronização": "99.8%"
    }
    
    cols = st.columns(3)
    for idx, (key, value) in enumerate(resumo_data.items()):
        with cols[idx % 3]:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, {CORES['verde']} 0%, {CORES['turquesa']} 100%);
                color: white;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            ">
                <h3 style="color: white; margin: 0; font-size: 1.8em;">{value}</h3>
                <p style="color: white; margin: 8px 0 0 0; font-weight: 600;">{key}</p>
            </div>
            """, unsafe_allow_html=True)

# ========== SOBRE VIEW ==========
elif "Sobre" in view_option:
    st.markdown("### ℹ️ Sobre o Construscanner")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        ## 🏗️ Sistema Inteligente de Monitoramento
        
        **Construscanner** é um sistema de monitoramento em tempo real de canteiros de obras,
        operado por Inteligência Artificial para garantir segurança, produtividade e eficiência.
        
        ### 🎯 Objetivo Principal
        Monitorar e quantificar as ações em um canteiro de obras, otimizando a produtividade
        e identificando riscos de segurança em tempo real.
        """)
    
    with col2:
        st.markdown(f"""
        <div style="
            background: {CORES['azul_principal']};
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        ">
            <h2 style="color: white; margin: 0;">7 ETAPAS</h2>
            <p style="margin: 10px 0 0 0;">Ciclo Inteligente de Monitoramento</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 🔧 Recursos Principais")
    
    recursos = [
        "📷 Câmeras de Monitoramento 24/7",
        "📡 GPS em Tempo Real",
        "🌡️ Sensores Ambientais",
        "🤖 Análise de IA Embarcada",
        "⚠️ Alertas Automáticos",
        "☁️ Relatórios em Nuvem",
        "📶 Conectividade 4G/5G",
        "📜 Histórico de Atividades",
        "🔗 Integração de Dados",
        "🎨 Interface Intuitiva",
        "⏳ Autonomia Estendida",
        "📈 Escalabilidade"
    ]
    
    cols = st.columns(4)
    for idx, recurso in enumerate(recursos):
        with cols[idx % 4]:
            st.markdown(f"""
            <div style="
                background: {CORES['verde']};
                color: white;
                padding: 15px;
                border-radius: 8px;
                text-align: center;
                margin: 8px 0;
                font-weight: 600;
            ">
                {recurso}
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {CORES['azul_principal']} 0%, {CORES['turquesa']} 100%);
        color: white;
        padding: 30px;
        border-radius: 10px;
        text-align: center;
    ">
        <h3 style="color: white; margin: 0;">7 Etapas do Sistema Construscanner</h3>
        <p style="margin: 15px 0 0 0;">
            <strong>1. Coleta</strong> → <strong>2. Processamento</strong> → <strong>3. Transmissão</strong> → 
            <strong>4. Armazenamento</strong> → <strong>5. Interface</strong> → <strong>6. Alertas</strong> → <strong>7. Integração</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

# ========== FOOTER ==========
st.markdown("---")
st.markdown(f"""
<div style="
    background: {CORES['azul_principal']};
    color: white;
    padding: 25px;
    border-radius: 10px;
    text-align: center;
">
    <h3 style="color: {CORES['branco']}; margin: 0;">📊 Construscanner</h3>
    <p style="margin: 10px 0; opacity: 0.9; color: {CORES['branco']};">Sistema Inteligente de Monitoramento de Obras</p>
    <p style="margin: 0; font-size: 0.9em; opacity: 0.7; color: {CORES['branco']};">© 2024 Equipe Construscanner | Engenharia & IA</p>
</div>
""", unsafe_allow_html=True)
