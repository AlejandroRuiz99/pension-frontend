"""
Módulo de barra lateral
Maneja la navegación y estado de la API
"""

import streamlit as st
from .api_client import check_api_health


def show_sidebar():
    """
    Mostrar la barra lateral con navegación y estado de la API
    
    Returns:
        str: Opción seleccionada por el usuario
    """
    with st.sidebar:
        # Estado de la API
        _show_api_status()
        
        # Navegación principal
        st.markdown("---")
        option = st.selectbox(
            "🎛️ Selecciona una opción:",
            ["🏠 Inicio", "📄 Extraer Bases", "🚀 Procesar Completo", "⚙️ Configuración"]
        )
        
        # Información adicional
        _show_additional_info()
        
        return option


def _show_api_status():
    """Mostrar el estado de la API en la barra lateral"""
    st.header("🔗 Estado de la API")
    
    if st.button("🔄 Verificar Conexión"):
        with st.spinner("Verificando conexión..."):
            is_healthy, health_data = check_api_health()
        
        if is_healthy:
            st.success("✅ API conectada correctamente")
            if health_data:
                # Mostrar servicios disponibles si los hay
                services = health_data.get("services", {})
                if services:
                    st.json(services)
        else:
            st.error("❌ Error de conexión con la API")
            if health_data:
                st.error(health_data)


def _show_additional_info():
    """Mostrar información adicional en la barra lateral"""
    st.markdown("---")
    st.markdown("### 📋 Información")
    
    st.markdown("""
    **🔧 Funcionalidades:**
    - Extracción automática de PDFs
    - Cálculo de base reguladora
    - Exportación a Excel
    - Configuraciones actualizadas
    
    **📊 Características:**
    - Fórmulas dinámicas
    - Últimos 15 años
    - Múltiples regímenes
    - Validación automática
    """)
    
    st.markdown("---")
    st.markdown("### 💡 Ayuda")
    
    with st.expander("🔍 Cómo usar"):
        st.markdown("""
        1. **Extracción**: Sube un PDF y obtén las bases
        2. **Procesamiento**: Cálculo completo con parámetros
        3. **Configuración**: Consulta índices y parámetros
        4. **Descarga**: Excel editable con fórmulas
        """)
    
    with st.expander("📄 Formatos soportados"):
        st.markdown("""
        - **PDF**: Máximo 10MB
        - **Fecha**: MM/YYYY (ej: 06/2025)
        - **Régimen**: GENERAL o AUTONOMO
        - **Exportación**: Excel (.xlsx) y JSON
        """)
    
    with st.expander("⚠️ Solución de problemas"):
        st.markdown("""
        - **Error de conexión**: Verifica el estado de la API
        - **Archivo muy grande**: Máximo 10MB
        - **Formato incorrecto**: Usa MM/YYYY
        - **Fórmulas Excel**: Usa comas en lugar de punto y coma
        """) 