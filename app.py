"""
🏢 Frontend para API de Bases de Cotización
Aplicación Streamlit moderna y funcional
"""

import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime
import time

# Configuración de la página
st.set_page_config(
    page_title="Simulador de Pensiones",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# URL de la API
API_BASE_URL = "https://pension-bases-api-e707c1384c99.herokuapp.com"

# CSS personalizado para un diseño moderno
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
</style>
""", unsafe_allow_html=True)

# Funciones para interactuar con la API
def check_api_health():
    """Verificar el estado de la API"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=10)
        return response.status_code == 200, response.json() if response.status_code == 200 else None
    except Exception as e:
        return False, str(e)

def extract_bases(file):
    """Extraer bases de cotización de un PDF"""
    try:
        files = {"file": file}
        response = requests.post(f"{API_BASE_URL}/api/extract", files=files, timeout=60)
        return response.status_code == 200, response.json()
    except Exception as e:
        return False, {"error": str(e)}

def process_complete(file, fecha_jubilacion, regimen_acceso, sexo):
    """Procesar PDF completo (extraer + simular)"""
    try:
        files = {"file": file}
        data = {
            "fecha_jubilacion": fecha_jubilacion,
            "regimen_acceso": regimen_acceso,
            "sexo": sexo
        }
        response = requests.post(f"{API_BASE_URL}/api/process", files=files, data=data, timeout=120)
        return response.status_code == 200, response.json()
    except Exception as e:
        return False, {"error": str(e)}

def get_configuration():
    """Obtener configuración de la API"""
    try:
        # Obtener todas las configuraciones
        configs = {}
        
        # Parámetros de cómputo
        response = requests.get(f"{API_BASE_URL}/api/config/parametros", timeout=10)
        if response.status_code == 200:
            configs["parametros"] = response.json()
        
        # Índices de revalorización
        response = requests.get(f"{API_BASE_URL}/api/config/indices", timeout=10)
        if response.status_code == 200:
            configs["indices"] = response.json()
        
        # Topes de cotización
        response = requests.get(f"{API_BASE_URL}/api/config/topes", timeout=10)
        if response.status_code == 200:
            configs["topes"] = response.json()
        
        return True, configs
    except Exception as e:
        return False, {"error": str(e)}

# Header principal
st.markdown("""
<div class="main-header">
    <h1>Simulador de Pensiones</h1>
    <p>Extracción y cálculo de bases reguladoras profesional</p>
</div>
""", unsafe_allow_html=True)

# Verificar estado de la API
with st.sidebar:
    st.header("🔗 Estado de la API")
    
    if st.button("🔄 Verificar Conexión"):
        with st.spinner("Verificando conexión..."):
            is_healthy, health_data = check_api_health()
        
        if is_healthy:
            st.success("✅ API conectada correctamente")
            if health_data:
                st.json(health_data.get("services", {}))
        else:
            st.error("❌ Error de conexión con la API")
            if health_data:
                st.error(health_data)

# Navegación principal
st.sidebar.markdown("---")
option = st.sidebar.selectbox(
    "🎛️ Selecciona una opción:",
    ["🏠 Inicio", "📄 Extraer Bases", "🚀 Procesar Completo", "⚙️ Configuración"]
)

# Página de inicio
if option == "🏠 Inicio":
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>📄 Extracción</h3>
            <p>Sube un archivo PDF y extrae automáticamente las bases de cotización.</p>
            <ul>
                <li>Identifica empresas y regímenes</li>
                <li>Valida datos automáticamente</li>
                <li>Descarga resultados en JSON</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🚀 Procesamiento Completo</h3>
            <p>Extrae bases y calcula la base reguladora en un solo paso.</p>
            <ul>
                <li>Simulación de períodos futuros</li>
                <li>Aplicación de revalorización</li>
                <li>Cálculo de base reguladora</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>⚙️ Configuración</h3>
            <p>Consulta los parámetros de cálculo actualizados.</p>
            <ul>
                <li>Índices de revalorización</li>
                <li>Topes de cotización</li>
                <li>Parámetros de cómputo</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Página de extracción
elif option == "📄 Extraer Bases":
    st.header("📄 Extracción de Bases de Cotización")
    
    st.markdown("""
    <div class="feature-card">
        <p>Sube un archivo PDF con bases de cotización de la Seguridad Social y obtén los datos estructurados automáticamente.</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Selecciona un archivo PDF",
        type=['pdf'],
        help="Archivo PDF con bases de cotización de la Seguridad Social (máximo 10MB)"
    )
    
    if uploaded_file is not None:
        # Mostrar información del archivo
        st.info(f"📁 Archivo: {uploaded_file.name} ({uploaded_file.size / 1024:.1f} KB)")
        
        if st.button("🔍 Extraer Bases", key="extract"):
            if uploaded_file.size > 10 * 1024 * 1024:  # 10MB
                st.error("❌ El archivo es demasiado grande. Máximo 10MB.")
            else:
                with st.spinner("Extrayendo bases de cotización..."):
                    success, result = extract_bases(uploaded_file)
                
                if success:
                    st.markdown("""
                    <div class="success-box">
                        ✅ <strong>Extracción completada exitosamente</strong>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Mostrar estadísticas
                    if "total_bases" in result:
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total Bases", result["total_bases"])
                        with col2:
                            st.metric("Empresas", result.get("metadata", {}).get("total_empresas", "N/A"))
                        with col3:
                            periodo = result.get("metadata", {}).get("periodo_bases", {})
                            if periodo:
                                st.metric("Período", f"{periodo.get('desde', '')} - {periodo.get('hasta', '')}")
                    
                    # Botón de descarga
                    json_data = json.dumps(result, indent=2, ensure_ascii=False)
                    st.download_button(
                        label="📥 Descargar Resultados (JSON)",
                        data=json_data,
                        file_name=f"bases_extraidas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json",
                        key="download_extract"
                    )
                else:
                    st.markdown(f"""
                    <div class="error-box">
                        ❌ <strong>Error en la extracción:</strong><br>
                        {result.get('error', result.get('detail', 'Error desconocido'))}
                    </div>
                    """, unsafe_allow_html=True)

# Página de procesamiento completo
elif option == "🚀 Procesar Completo":
    st.header("🚀 Procesamiento Completo")
    
    st.markdown("""
    <div class="feature-card">
        <p>Proceso completo en un solo paso: extrae bases del PDF y calcula automáticamente la base reguladora.</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Selecciona un archivo PDF",
        type=['pdf'],
        help="Archivo PDF con bases de cotización de la Seguridad Social (máximo 10MB)",
        key="process_file"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        fecha_jubilacion = st.text_input(
            "📅 Fecha de Jubilación",
            placeholder="MM/YYYY",
            help="Formato: MM/YYYY (ejemplo: 06/2025)"
        )
        
        regimen_acceso = st.selectbox(
            "⚙️ Régimen de Acceso",
            ["GENERAL", "AUTONOMO"],
            help="Régimen de cotización"
        )
    
    with col2:
        sexo = st.selectbox(
            "👤 Sexo del Cotizante",
            ["MASCULINO", "FEMENINO"],
            help="Necesario para el cálculo correcto de lagunas"
        )
    
    if uploaded_file is not None and fecha_jubilacion:
        # Validar formato de fecha
        import re
        if not re.match(r'^\d{2}/\d{4}$', fecha_jubilacion):
            st.error("❌ Formato de fecha incorrecto. Use MM/YYYY")
        else:
            st.info(f"📁 Archivo: {uploaded_file.name} ({uploaded_file.size / 1024:.1f} KB)")
            
            if st.button("🚀 Procesar Completo", key="process"):
                if uploaded_file.size > 10 * 1024 * 1024:  # 10MB
                    st.error("❌ El archivo es demasiado grande. Máximo 10MB.")
                else:
                    with st.spinner("Procesando archivo completo... Esto puede tomar unos minutos."):
                        success, result = process_complete(uploaded_file, fecha_jubilacion, regimen_acceso, sexo)
                    
                    if success:
                        st.markdown("""
                        <div class="success-box">
                            ✅ <strong>Procesamiento completado exitosamente</strong>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Mostrar resultados principales
                        if "estadisticas" in result:
                            stats = result["estadisticas"]
                            
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric("Total Bases", stats.get("total_bases", "N/A"))
                            with col2:
                                st.metric("Base Reguladora", f"€{stats.get('base_reguladora', 0):.2f}")
                            with col3:
                                st.metric("Suma Total", f"€{stats.get('suma_total', 0):.2f}")
                            with col4:
                                st.metric("Cálculo Usado", result.get("calculo_elegido", "N/A"))
                        
                        # Información adicional
                        st.subheader("📊 Detalles del Procesamiento")
                        info_col1, info_col2 = st.columns(2)
                        
                        with info_col1:
                            st.write(f"**Fecha de Jubilación:** {result.get('fecha_jubilacion', 'N/A')}")
                            st.write(f"**Régimen:** {result.get('regimen_acceso', 'N/A')}")
                            st.write(f"**Sexo:** {result.get('sexo', 'N/A')}")
                        
                        with info_col2:
                            if "metadata_extraccion" in result:
                                metadata = result["metadata_extraccion"]
                                st.write(f"**Bases Extraídas:** {metadata.get('total_bases_extraidas', 'N/A')}")
                                st.write(f"**Empresas:** {metadata.get('total_empresas', 'N/A')}")
                                periodo = metadata.get('periodo_extraido', {})
                                if periodo:
                                    st.write(f"**Período:** {periodo.get('desde', '')} - {periodo.get('hasta', '')}")
                        
                        # Botón de descarga
                        json_data = json.dumps(result, indent=2, ensure_ascii=False)
                        st.download_button(
                            label="📥 Descargar Resultados Completos (JSON)",
                            data=json_data,
                            file_name=f"procesamiento_completo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                            mime="application/json",
                            key="download_process"
                        )
                    else:
                        st.markdown(f"""
                        <div class="error-box">
                            ❌ <strong>Error en el procesamiento:</strong><br>
                            {result.get('error', result.get('detail', 'Error desconocido'))}
                        </div>
                        """, unsafe_allow_html=True)

# Página de configuración
elif option == "⚙️ Configuración":
    st.header("⚙️ Configuración del Sistema")
    
    st.markdown("""
    <div class="feature-card">
        <p>Consulta los parámetros de configuración cargados en el sistema para cálculos y simulaciones.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 Cargar Configuración"):
        with st.spinner("Cargando configuración..."):
            success, configs = get_configuration()
        
        if success:
            st.success("✅ Configuración cargada correctamente")
            
            # Parámetros de cómputo
            if "parametros" in configs:
                st.subheader("📊 Parámetros de Cómputo")
                params_data = configs["parametros"]["data"]
                
                # Verificar si ya tenemos los parámetros directamente o están anidados
                params = None
                if params_data:
                    if "parametros_computo_anual" in params_data:
                        params = params_data["parametros_computo_anual"]
                    else:
                        # Asumir que params_data ya contiene los parámetros directamente
                        params = params_data
                
                if params and isinstance(params, dict):
                    # Convertir a DataFrame para mejor visualización
                    df_params = []
                    for año, datos in params.items():
                        if isinstance(datos, dict):
                            df_params.append({
                                "Año": año,
                                "Bases Incluidas": datos.get("bases_incluidas", datos.get("numero_bases", "N/A")),
                                "Período (meses)": datos.get("periodo_meses", "N/A"),
                                "Divisor Base Reguladora": datos.get("divisor_base_reguladora", datos.get("divisor", "N/A"))
                            })
                    
                    if df_params:
                        # Ordenar por año descendente
                        df = pd.DataFrame(df_params)
                        df = df.sort_values('Año', ascending=False)
                        st.dataframe(df, use_container_width=True, hide_index=True)
                        
                        # Mostrar información adicional en columnas
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total Años", len(df_params))
                        with col2:
                            último_año = max(params.keys())
                            st.metric("Último Año", último_año)
                        with col3:
                            if df_params:
                                primer_año = min(params.keys())
                                st.metric("Primer Año", primer_año)
                else:
                    st.warning("⚠️ No se pudieron procesar los parámetros de cómputo")
                    if params_data:
                        st.info("Los datos están disponibles pero en un formato no reconocido.")
            
            # Índices de revalorización
            if "indices" in configs:
                st.subheader("📈 Índices de Revalorización")
                indices_data = configs["indices"]["data"]
                
                # Verificar si ya tenemos los índices directamente o están anidados
                indices = None
                if indices_data:
                    if "indices_revalorizacion" in indices_data:
                        indices = indices_data["indices_revalorizacion"]
                    else:
                        # Asumir que indices_data ya contiene los índices directamente
                        indices = indices_data
                
                if indices and isinstance(indices, dict):
                    # Mostrar información resumida
                    total_indices = len(indices)
                    fechas = list(indices.keys())
                    if fechas:
                        desde = min(fechas)
                        hasta = max(fechas)
                        
                        # Métricas principales
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total Índices", total_indices)
                        with col2:
                            st.metric("Desde", desde)
                        with col3:
                            st.metric("Hasta", hasta)
                    
                    # Mostrar todos los índices ordenados por fecha
                    def sort_key(fecha):
                        """Función para ordenar fechas MM/YYYY correctamente"""
                        try:
                            mes, año = fecha.split('/')
                            return (int(año), int(mes))
                        except:
                            return (0, 0)
                    
                    sorted_dates = sorted(indices.keys(), key=sort_key, reverse=True)
                    
                    df_indices = []
                    for fecha in sorted_dates:
                        indice = indices[fecha]
                        df_indices.append({
                            "Fecha (MM/YYYY)": fecha,
                            "Índice de Revalorización": f"{indice:.6f}"
                        })
                    
                    if df_indices:
                        st.write(f"**📊 Todos los índices de revalorización ({len(df_indices)} registros):**")
                        df = pd.DataFrame(df_indices)
                        
                        # Mostrar tabla con altura fija para scroll
                        st.dataframe(df, use_container_width=True, hide_index=True, height=400)
                        
                        # Estadísticas básicas
                        valores = list(indices.values())
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Índice Promedio", f"{sum(valores)/len(valores):.6f}")
                        with col2:
                            st.metric("Índice Máximo", f"{max(valores):.6f}")
                        with col3:
                            st.metric("Índice Mínimo", f"{min(valores):.6f}")
                        
                        # Información del último índice disponible
                        ultimo_fecha = sorted_dates[0]
                        ultimo_indice = indices[ultimo_fecha]
                        st.info(f"📅 **Último índice disponible**: {ultimo_fecha} - Valor: {ultimo_indice:.6f}")
                else:
                    st.warning("⚠️ No se pudieron procesar los índices de revalorización")
                    if indices_data:
                        st.info("Los datos están disponibles pero en un formato no reconocido.")
            
            # Topes de cotización
            if "topes" in configs:
                st.subheader("💰 Topes de Cotización")
                topes_data = configs["topes"]["data"]
                
                # Verificar si ya tenemos los topes directamente o están anidados
                topes = None
                if topes_data:
                    if "topes_cotizacion" in topes_data:
                        topes = topes_data["topes_cotizacion"]
                    else:
                        # Asumir que topes_data ya contiene los topes directamente
                        topes = topes_data
                
                if topes and isinstance(topes, dict):
                    df_topes = []
                    for año, datos in topes.items():
                        if isinstance(datos, dict):
                            base_min = datos.get('base_minima_mensual', 0)
                            base_max = datos.get('base_maxima_mensual', 0)
                            df_topes.append({
                                "Año": año,
                                "Base Mínima Mensual": f"€{base_min:.2f}",
                                "Base Máxima Mensual": f"€{base_max:.2f}",
                                "Diferencia": f"€{base_max - base_min:.2f}"
                            })
                    
                    if df_topes:
                        # Ordenar por año descendente
                        df = pd.DataFrame(df_topes)
                        df = df.sort_values('Año', ascending=False)
                        st.dataframe(df, use_container_width=True, hide_index=True)
                        
                        # Mostrar métricas en columnas
                        col1, col2, col3, col4 = st.columns(4)
                        
                        ultimo_año = max(topes.keys())
                        ultimo_datos = topes[ultimo_año]
                        
                        with col1:
                            st.metric("Total Años", len(df_topes))
                        with col2:
                            st.metric("Último Año", ultimo_año)
                        with col3:
                            st.metric("Mínima Actual", f"€{ultimo_datos.get('base_minima_mensual', 0):.2f}")
                        with col4:
                            st.metric("Máxima Actual", f"€{ultimo_datos.get('base_maxima_mensual', 0):.2f}")
                        
                        # Información destacada
                        st.success(f"🎯 **Bases de cotización para {ultimo_año}**: Desde €{ultimo_datos.get('base_minima_mensual', 0):.2f} hasta €{ultimo_datos.get('base_maxima_mensual', 0):.2f} mensuales")
                else:
                    st.warning("⚠️ No se pudieron procesar los topes de cotización")
                    if topes_data:
                        st.info("Los datos están disponibles pero en un formato no reconocido.")
            
            # Botón para descargar toda la configuración
            json_data = json.dumps(configs, indent=2, ensure_ascii=False)
            st.download_button(
                label="📥 Descargar Configuración Completa (JSON)",
                data=json_data,
                file_name=f"configuracion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                key="download_config"
            )
        else:
            st.markdown(f"""
            <div class="error-box">
                ❌ <strong>Error cargando configuración:</strong><br>
                {configs.get('error', 'Error desconocido')}
            </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🏢 API Bases de Cotización | Desarrollado con ❤️ usando Streamlit</p>
    <p>API desplegada en: <a href="https://pension-bases-api-e707c1384c99.herokuapp.com" target="_blank">Heroku</a></p>
</div>
""", unsafe_allow_html=True) 