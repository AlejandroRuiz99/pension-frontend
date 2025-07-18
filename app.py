"""
🏢 Frontend para API de Bases de Cotización - Versión Modularizada
Aplicación Streamlit moderna y funcional con arquitectura modular
"""

import streamlit as st

# Importar módulos locales
from modules.ui_components import apply_custom_css, show_main_header, show_footer
from modules.sidebar import show_sidebar
from modules.pages import show_home_page, show_extract_page, show_process_page, show_config_page

# Configuración de la página
st.set_page_config(
    page_title="Simulador de Pensiones",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Función principal de la aplicación"""
    # Aplicar estilos CSS personalizados
    apply_custom_css()
    
    # Mostrar header principal
    show_main_header()
    
    # Mostrar sidebar y obtener la opción seleccionada
    option = show_sidebar()
    
    # Router: mostrar la página correspondiente según la opción
    if option == "🏠 Inicio":
        show_home_page()
    elif option == "📄 Extraer Bases":
        show_extract_page()
    elif option == "🚀 Procesar Completo":
        show_process_page()
    elif option == "⚙️ Configuración":
        show_config_page()
    
    # Mostrar footer
    show_footer()


if __name__ == "__main__":
    main() 