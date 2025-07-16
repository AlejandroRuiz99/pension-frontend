# 🏢 Frontend para API de Bases de Cotización

Frontend moderno desarrollado con Streamlit para interactuar con la API de Bases de Cotización.

## 🚀 Características

- **📄 Extracción de Bases**: Sube PDFs y extrae bases de cotización automáticamente
- **🚀 Procesamiento Completo**: Extrae bases y calcula base reguladora en un solo paso
- **⚙️ Configuración**: Visualiza parámetros de cálculo del sistema
- **📱 Diseño Moderno**: Interfaz limpia y responsive
- **📥 Descarga de Resultados**: Exporta resultados en formato JSON

## 📋 Requisitos

- Python 3.8+
- Las dependencias listadas en `requirements.txt`

## 🛠️ Instalación

1. **Clonar el repositorio**:
```bash
git clone <url-del-repo>
cd frontend-basess
```

2. **Crear entorno virtual**:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

## 🚀 Ejecución

```bash
streamlit run app.py
```

La aplicación estará disponible en: `http://localhost:8501`

## 🎯 Funcionalidades

### 📄 Extracción de Bases
- Sube archivos PDF de bases de cotización
- Procesa automáticamente con la API
- Descarga resultados estructurados en JSON

### 🚀 Procesamiento Completo
- Extrae bases del PDF
- Calcula base reguladora automáticamente
- Configura parámetros de jubilación
- Descarga análisis completo

### ⚙️ Configuración
- Visualiza parámetros de cómputo
- Consulta índices de revalorización
- Revisa topes de cotización
- Descarga configuración completa

## 🔗 API Backend

Este frontend se conecta a la API desplegada en:
`https://pension-bases-api-e707c1384c99.herokuapp.com`

## 📱 Uso

1. **Verificar Conexión**: Usa el botón en la barra lateral para verificar que la API esté funcionando
2. **Seleccionar Función**: Elige entre extracción, procesamiento completo o configuración
3. **Subir Archivo**: Para extracción y procesamiento, sube un PDF válido
4. **Configurar Parámetros**: Para procesamiento completo, especifica fecha de jubilación, régimen y sexo
5. **Descargar Resultados**: Usa los botones de descarga para obtener los resultados en JSON

## 🎨 Diseño

- Interfaz moderna con gradientes y efectos visuales
- Cards informativos para cada sección
- Feedback visual para operaciones exitosas y errores
- Diseño responsive que funciona en desktop y móvil

## 🛡️ Manejo de Errores

- Validación de archivos (tamaño, formato)
- Manejo de errores de conexión con la API
- Feedback claro para el usuario en caso de problemas
- Timeouts configurados para operaciones largas

## 📊 Métricas y Visualización

- Resumen estadístico de resultados
- Tablas organizadas para configuraciones
- Métricas destacadas para resultados importantes
- Información estructurada del procesamiento 