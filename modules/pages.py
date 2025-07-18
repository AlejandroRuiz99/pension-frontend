"""
Módulo de páginas de la aplicación
Contiene la lógica de cada página del simulador de pensiones
"""

import streamlit as st
import pandas as pd
import json
import re
from datetime import datetime

from .api_client import extract_bases, process_complete, get_configuration
from .ui_components import show_feature_card, show_success_message, show_error_message, show_info_message
from .excel_generator import generate_excel_from_process_result


def show_home_page():
    """Mostrar la página de inicio con información general"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        show_feature_card(
            "📄 Extracción",
            "Sube un archivo PDF y extrae automáticamente las bases de cotización.",
            [
                "Identifica empresas y regímenes",
                "Valida datos automáticamente",
                "Descarga resultados en JSON"
            ]
        )
    
    with col2:
        show_feature_card(
            "🚀 Procesamiento Completo",
            "Extrae bases y calcula la base reguladora en un solo paso.",
            [
                "Simulación de períodos futuros",
                "Aplicación de revalorización",
                "Cálculo de base reguladora"
            ]
        )
    
    with col3:
        show_feature_card(
            "⚙️ Configuración",
            "Consulta los parámetros de cálculo actualizados.",
            [
                "Índices de revalorización",
                "Topes de cotización",
                "Parámetros de cómputo"
            ]
        )


def show_extract_page():
    """Mostrar la página de extracción de bases"""
    st.header("📄 Extracción de Bases de Cotización")
    
    show_info_message(
        "Sube un archivo PDF con bases de cotización de la Seguridad Social y obtén los datos estructurados automáticamente."
    )
    
    uploaded_file = st.file_uploader(
        "Selecciona un archivo PDF",
        type=['pdf'],
        help="Archivo PDF con bases de cotización de la Seguridad Social (máximo 10MB)"
    )
    
    if uploaded_file is not None:
        st.info(f"📁 Archivo: {uploaded_file.name} ({uploaded_file.size / 1024:.1f} KB)")
        
        if st.button("🔍 Extraer Bases", key="extract"):
            if uploaded_file.size > 10 * 1024 * 1024:  # 10MB
                show_error_message("El archivo es demasiado grande. Máximo 10MB.")
            else:
                with st.spinner("Extrayendo bases de cotización..."):
                    success, result = extract_bases(uploaded_file)
                
                if success:
                    show_success_message("Extracción completada exitosamente")
                    
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
                    error_msg = result.get('error', result.get('detail', 'Error desconocido'))
                    show_error_message(f"Error en la extracción: {error_msg}")


def show_process_page():
    """Mostrar la página de procesamiento completo"""
    st.header("🚀 Procesamiento Completo")
    
    show_info_message(
        "Proceso completo en un solo paso: extrae bases del PDF y calcula automáticamente la base reguladora."
    )
    
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
        if not re.match(r'^\d{2}/\d{4}$', fecha_jubilacion):
            show_error_message("Formato de fecha incorrecto. Use MM/YYYY")
        else:
            st.info(f"📁 Archivo: {uploaded_file.name} ({uploaded_file.size / 1024:.1f} KB)")
            
            if st.button("🚀 Procesar Completo", key="process"):
                if uploaded_file.size > 10 * 1024 * 1024:  # 10MB
                    show_error_message("El archivo es demasiado grande. Máximo 10MB.")
                else:
                    with st.spinner("Procesando archivo completo... Esto puede tomar unos minutos."):
                        success, result = process_complete(uploaded_file, fecha_jubilacion, regimen_acceso, sexo)
                    
                    if success:
                        show_success_message("Procesamiento completado exitosamente")
                        
                        # Mostrar resultados principales
                        _show_process_results(result)
                        
                        # Botones de descarga
                        _show_download_buttons(result)
                    else:
                        error_msg = result.get('error', result.get('detail', 'Error desconocido'))
                        show_error_message(f"Error en el procesamiento: {error_msg}")


def show_config_page():
    """Mostrar la página de configuración"""
    st.header("⚙️ Configuración del Sistema")
    
    show_info_message(
        "Consulta los parámetros de configuración cargados en el sistema para cálculos y simulaciones."
    )
    
    if st.button("🔄 Cargar Configuración"):
        with st.spinner("Cargando configuración..."):
            success, configs = get_configuration()
        
        if success:
            st.success("✅ Configuración cargada correctamente")
            
            # Mostrar cada tipo de configuración
            _show_parametros_computo(configs)
            _show_indices_revalorizacion(configs)
            _show_topes_cotizacion(configs)
            
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
            error_msg = configs.get('error', 'Error desconocido')
            show_error_message(f"Error cargando configuración: {error_msg}")


def _show_process_results(result):
    """Mostrar los resultados del procesamiento"""
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


def _show_download_buttons(result):
    """Mostrar botones de descarga"""
    st.subheader("📥 Descargar Resultados")
    
    col_download1, col_download2 = st.columns(2)
    
    with col_download1:
        # Generar Excel
        excel_data = generate_excel_from_process_result(result)
        if excel_data:
            st.download_button(
                label="📊 Descargar Excel Editable",
                data=excel_data,
                file_name=f"bases_cotizacion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="download_excel",
                help="Excel con pestañas separadas y fórmulas dinámicas para edición"
            )
    
    with col_download2:
        # JSON para desarrollo
        json_data = json.dumps(result, indent=2, ensure_ascii=False)
        st.download_button(
            label="🔨 Descargar JSON (Debug)",
            data=json_data,
            file_name=f"procesamiento_completo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            key="download_process",
            help="Archivo JSON completo para desarrollo y depuración"
        )


def _show_parametros_computo(configs):
    """Mostrar parámetros de cómputo"""
    if "parametros" in configs:
        st.subheader("📊 Parámetros de Cómputo")
        params_data = configs["parametros"]["data"]
        
        params = None
        if params_data:
            if "parametros_computo_anual" in params_data:
                params = params_data["parametros_computo_anual"]
            else:
                params = params_data
        
        if params and isinstance(params, dict):
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
                df = pd.DataFrame(df_params)
                df = df.sort_values('Año', ascending=False)
                st.dataframe(df, use_container_width=True, hide_index=True)
                
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


def _show_indices_revalorizacion(configs):
    """Mostrar índices de revalorización"""
    if "indices" in configs:
        st.subheader("📈 Índices de Revalorización")
        indices_data = configs["indices"]["data"]
        
        indices = None
        if indices_data:
            if "indices_revalorizacion" in indices_data:
                indices = indices_data["indices_revalorizacion"]
            else:
                indices = indices_data
        
        if indices and isinstance(indices, dict):
            total_indices = len(indices)
            fechas = list(indices.keys())
            if fechas:
                desde = min(fechas)
                hasta = max(fechas)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Índices", total_indices)
                with col2:
                    st.metric("Desde", desde)
                with col3:
                    st.metric("Hasta", hasta)
            
            # Mostrar tabla de índices
            def sort_key(fecha):
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
                
                ultimo_fecha = sorted_dates[0]
                ultimo_indice = indices[ultimo_fecha]
                st.info(f"📅 **Último índice disponible**: {ultimo_fecha} - Valor: {ultimo_indice:.6f}")
        else:
            st.warning("⚠️ No se pudieron procesar los índices de revalorización")


def _show_topes_cotizacion(configs):
    """Mostrar topes de cotización"""
    if "topes" in configs:
        st.subheader("💰 Topes de Cotización")
        topes_data = configs["topes"]["data"]
        
        topes = None
        if topes_data:
            if "topes_cotizacion" in topes_data:
                topes = topes_data["topes_cotizacion"]
            else:
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
                df = pd.DataFrame(df_topes)
                df = df.sort_values('Año', ascending=False)
                st.dataframe(df, use_container_width=True, hide_index=True)
                
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
                
                st.success(f"🎯 **Bases de cotización para {ultimo_año}**: Desde €{ultimo_datos.get('base_minima_mensual', 0):.2f} hasta €{ultimo_datos.get('base_maxima_mensual', 0):.2f} mensuales")
        else:
            st.warning("⚠️ No se pudieron procesar los topes de cotización") 