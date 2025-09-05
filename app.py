import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import datetime
import time

# Configuración de la página
st.set_page_config(
    page_title="Investigación Financiera Automatizada",
    page_icon="📊",
    layout="wide"
)

# Título principal
st.title("📊 Investigación Financiera Automatizada")
st.markdown("### Recomendaciones Personalizadas por Perfil de Riesgo")
st.markdown("---")

# Sidebar para configuración
st.sidebar.title("⚙️ Configuración")

# Selector de perfil
profile = st.sidebar.selectbox(
    "🎯 Perfil de Inversor:",
    ["Conservador", "Equilibrado", "Agresivo"],
    help="Selecciona tu tolerancia al riesgo"
)

# Información del perfil
profile_info = {
    "Conservador": {
        "descripcion": "Prioriza la preservación del capital con mínima volatilidad",
        "objetivo": "3-6% anual",
        "riesgo": "Bajo",
        "horizonte": "1-5 años"
    },
    "Equilibrado": {
        "descripcion": "Balance entre crecimiento y estabilidad",
        "objetivo": "6-10% anual", 
        "riesgo": "Medio",
        "horizonte": "5-10 años"
    },
    "Agresivo": {
        "descripcion": "Maximiza el crecimiento aceptando alta volatilidad",
        "objetivo": "10%+ anual",
        "riesgo": "Alto", 
        "horizonte": "10+ años"
    }
}

# Mostrar información del perfil en sidebar
with st.sidebar:
    st.markdown("### Perfil Seleccionado")
    st.info(f"**{profile}**")
    st.write(f"📝 {profile_info[profile]['descripcion']}")
    st.write(f"🎯 **Objetivo:** {profile_info[profile]['objetivo']}")
    st.write(f"⚡ **Riesgo:** {profile_info[profile]['riesgo']}")
    st.write(f"📅 **Horizonte:** {profile_info[profile]['horizonte']}")

# Botón de análisis
analyze_button = st.sidebar.button("🚀 EJECUTAR ANÁLISIS", type="primary")

# Función para obtener datos
@st.cache_data(ttl=3600)
def get_market_data(tickers):
    data = []
    progress_bar = st.progress(0)
    
    for i, ticker in enumerate(tickers):
        try:
            st.text(f'Obteniendo datos de {ticker}...')
            yf_ticker = yf.Ticker(ticker)
            info = yf_ticker.info
            hist = yf_ticker.history(period="1y")
            
            if not hist.empty:
                current_price = hist['Close'][-1]
                year_start_price = hist['Close'][0] 
                ytd_return = ((current_price / year_start_price) - 1) * 100
                
                data.append({
                    'ETF': ticker,
                    'Nombre': info.get('longName', ticker)[:30] + '...' if len(info.get('longName', ticker)) > 30 else info.get('longName', ticker),
                    'Precio': f"${current_price:.2f}",
                    'Retorno YTD': f"{ytd_return:.1f}%",
                    'TER': f"{info.get('expenseRatio', 0)*100:.2f}%" if info.get('expenseRatio') else "N/A",
                    'Volumen': f"{info.get('averageVolume', 0):,}"
                })
            
            progress_bar.progress((i + 1) / len(tickers))
            time.sleep(0.3)
            
        except Exception as e:
            st.warning(f"Error con {ticker}")
    
    progress_bar.empty()
    return pd.DataFrame(data)

# Función para generar recomendaciones
def generate_recommendations(profile):
    recommendations = {
        'Conservador': [
            {'ETF': 'BND', 'Peso': '35%', 'Justificación': 'Bonos agregados USA - Estabilidad y preservación capital'},
            {'ETF': 'VGSH', 'Peso': '30%', 'Justificación': 'Bonos corto plazo - Protección contra subidas tipos'},
            {'ETF': 'VEA', 'Peso': '25%', 'Justificación': 'Renta variable Europa - Diversificación geográfica defensiva'},
            {'ETF': 'GLD', 'Peso': '10%', 'Justificación': 'Oro - Cobertura inflacionaria y refugio seguro'}
        ],
        'Equilibrado': [
            {'ETF': 'SPY', 'Peso': '30%', 'Justificación': 'S&P 500 - Core holding crecimiento con estabilidad'},
            {'ETF': 'VEA', 'Peso': '20%', 'Justificación': 'Europa desarrollada - Diversificación internacional'},
            {'ETF': 'VWO', 'Peso': '15%', 'Justificación': 'Mercados emergentes - Mayor potencial crecimiento'},
            {'ETF': 'BND', 'Peso': '25%', 'Justificación': 'Bonos USA - Componente estabilizador cartera'},
            {'ETF': 'GLD', 'Peso': '10%', 'Justificación': 'Oro - Protección ante volatilidad mercados'}
        ],
        'Agresivo': [
            {'ETF': 'SPY', 'Peso': '35%', 'Justificación': 'S&P 500 - Base sólida crecimiento largo plazo'},
            {'ETF': 'QQQ', 'Peso': '25%', 'Justificación': 'NASDAQ-100 - Tecnología y innovación disruptiva'},
            {'ETF': 'VWO', 'Peso': '20%', 'Justificación': 'Emergentes - Alto crecimiento y demographics favorables'},
            {'ETF': 'SOXX', 'Peso': '15%', 'Justificación': 'Semiconductores - Infraestructura revolución IA'},
            {'ETF': 'GLD', 'Peso': '5%', 'Justificación': 'Oro - Mínima protección en cartera agresiva'}
        ]
    }
    return recommendations[profile]

# Ejecución del análisis
if analyze_button:
    st.markdown("---")
    st.subheader(f"📈 Análisis Completo - Perfil {profile}")
    
    # ETFs por perfil
    profile_tickers = {
        'Conservador': ['BND', 'VGSH', 'VEA', 'GLD'],
        'Equilibrado': ['SPY', 'VEA', 'VWO', 'BND', 'GLD'],
        'Agresivo': ['SPY', 'QQQ', 'VWO', 'SOXX', 'GLD']
    }
    
    tickers = profile_tickers[profile]
    
    with st.spinner('🔄 Analizando mercados en tiempo real...'):
        market_data = get_market_data(tickers)
        recommendations = generate_recommendations(profile)
    
    st.success('✅ Análisis completado!')
    st.info(f'📅 Análisis realizado: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}')
    
    # Crear columnas
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("📊 Datos de Mercado en Tiempo Real")
        if not market_data.empty:
            st.dataframe(market_data, use_container_width=True, hide_index=True)
            
            # Extraer valores numéricos para gráfico
            market_data_numeric = market_data.copy()
            market_data_numeric['Retorno_Num'] = market_data_numeric['Retorno YTD'].str.replace('%', '').astype(float)
            
            # Gráfico de barras
            fig = px.bar(
                market_data_numeric, 
                x='ETF', 
                y='Retorno_Num',
                title='Rendimiento Year-to-Date (%)',
                color='Retorno_Num',
                color_continuous_scale='RdYlGn'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("❌ No se pudieron obtener datos. Inténtalo de nuevo.")
    
    with col2:
        st.subheader("🎯 Recomendaciones de Cartera")
        
        rec_df = pd.DataFrame(recommendations)
        st.dataframe(rec_df[['ETF', 'Peso']], use_container_width=True, hide_index=True)
        
        # Gráfico circular
        weights = [float(rec['Peso'].replace('%', '')) for rec in recommendations]
        etfs = [rec['ETF'] for rec in recommendations]
        
        fig_pie = px.pie(
            values=weights, 
            names=etfs,
            title='Distribución Recomendada'
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # Justificaciones
        st.subheader("💡 Justificaciones")
        for rec in recommendations:
            with st.expander(f"{rec['ETF']} - {rec['Peso']}"):
                st.write(rec['Justificación'])

# Información en sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ Información")
st.sidebar.markdown("""
**Fuente:** Yahoo Finance  
**Actualización:** Tiempo real  
**Coste:** Completamente gratuito  

**⚠️ Disclaimer:**  
Herramienta educativa únicamente.  
No constituye asesoramiento financiero.
""")

# Footer
st.markdown("---")
st.markdown("### 🚀 Tu Investigación Financiera Automatizada")
st.markdown("Aplicación gratuita desarrollada con Streamlit | Datos en tiempo real de Yahoo Finance")
