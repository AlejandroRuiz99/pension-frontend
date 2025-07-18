"""
Módulo de componentes de interfaz de usuario
Contiene estilos CSS y componentes reutilizables
"""

import streamlit as st


def apply_custom_css():
    """Aplicar estilos CSS personalizados a la aplicación"""
    st.markdown("""
    <style>
        .main-header {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            color: white;
            text-align: center;
        }
        
        .feature-card {
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin: 1rem 0;
            border-left: 4px solid #667eea;
        }
        
        .success-box {
            background: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }
        
        .error-box {
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }
        
        .stButton > button {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            transition: all 0.3s;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        
        .download-btn {
            background: #28a745 !important;
        }
        
        .excel-btn {
            background: linear-gradient(90deg, #28a745 0%, #20c997 100%) !important;
        }
        
        .debug-btn {
            background: linear-gradient(90deg, #6c757d 0%, #495057 100%) !important;
            font-size: 0.9em !important;
        }
    </style>
    """, unsafe_allow_html=True)


def show_main_header():
    """Mostrar el header principal de la aplicación"""
    st.markdown("""
    <div class="main-header">
        <h1>Simulador de Pensiones</h1>
        <p>Extracción y cálculo de bases reguladoras profesional</p>
    </div>
    """, unsafe_allow_html=True)


def show_feature_card(title, description, features):
    """
    Mostrar una tarjeta de característica
    
    Args:
        title (str): Título de la característica
        description (str): Descripción de la característica
        features (list): Lista de características
    """
    features_html = "".join([f"<li>{feature}</li>" for feature in features])
    
    st.markdown(f"""
    <div class="feature-card">
        <h3>{title}</h3>
        <p>{description}</p>
        <ul>
            {features_html}
        </ul>
    </div>
    """, unsafe_allow_html=True)


def show_success_message(message):
    """Mostrar mensaje de éxito"""
    st.markdown(f"""
    <div class="success-box">
        ✅ <strong>{message}</strong>
    </div>
    """, unsafe_allow_html=True)


def show_error_message(message):
    """Mostrar mensaje de error"""
    st.markdown(f"""
    <div class="error-box">
        ❌ <strong>{message}</strong>
    </div>
    """, unsafe_allow_html=True)


def show_info_message(message):
    """Mostrar mensaje informativo"""
    st.markdown(f"""
    <div class="feature-card">
        <p>{message}</p>
    </div>
    """, unsafe_allow_html=True)


def show_footer():
    """Mostrar el footer de la aplicación"""
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>🏢 API Bases de Cotización | Desarrollado con ❤️ usando Streamlit</p>
        <p>API actual: <strong>https://pension-bases-api-e707c1384c99.herokuapp.com</strong></p>
        <p>💡 <em>Frontend modularizado para mejor mantenimiento</em></p>
    </div>
    """, unsafe_allow_html=True) 