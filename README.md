# 🌎 LatAm Digital Pulse

### Una mirada interactiva a la economía digital de Latinoamérica

**LatAm Digital Pulse** es un dashboard web que explora indicadores económicos, sociales y digitales de 15 países latinoamericanos entre **2023 y 2025**. Filtra los datos por año, subregión y nivel de ingreso, y convierte la información en gráficos interactivos para comparar tendencias y descubrir patrones.

###**Enlace de la pagina:** https://latinbehavior.onrender.com/

> 📊 Explora los datos, compara países y transforma indicadores en nuevas preguntas.
>
> *Los datos incluidos son simulados y tienen fines educativos.*

## ✨ ¿Qué puedes explorar?

- **Indicadores clave:** pagos digitales, penetración y velocidad de internet, comercio electrónico, inversión de capital de riesgo, startups fintech, PIB per cápita, desempleo, inflación, pobreza y uso de redes sociales.
- **Filtros interactivos:** año, subregión, nivel de ingreso, disponibilidad de pagos instantáneos y existencia de leyes de protección de datos personales.
- **Métricas de resumen:** países incluidos, promedio de pagos digitales, promedio de penetración de internet y ventas de comercio electrónico.
- **Visualizaciones con Plotly Express:**
  - Gráfico de barras para comparar indicadores por país.
  - Gráfico de dona para explorar las ventas de comercio electrónico por categoría.
  - Histograma con diagrama de caja para observar la distribución de los indicadores.
- **Vista previa opcional** de los datos filtrados.

## 🚀 Instalación y ejecución local

Necesitas **Python** instalado y acceso a una terminal.

1. **Clona el repositorio** y entra en la carpeta del proyecto:

   ```bash
   git clone https://github.com/LauVRubioB/latinbehavior.git
   cd latinbehavior
   ```

2. **Crea y activa un entorno virtual** para mantener aisladas las dependencias:

   ```
   python -m virtualenv .venv
   ```

3. **Instala las dependencias** desde `requirements.txt`:

   ```bash
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

4. **Inicia la aplicación**:

   ```bash
   streamlit run app.py
   ```

5. Streamlit abrirá el dashboard en tu navegador. Si no lo hace automáticamente, visita la dirección local que muestra la terminal (normalmente `http://localhost:8501`).

> 💡 Mantén `dataset_latam.csv` en la carpeta raíz del proyecto: la aplicación lo carga desde esa ubicación.

## 🧰 Tecnologías utilizadas

| Tecnología | Uso en el proyecto |
| --- | --- |
| **Python** | Lenguaje de programación y procesamiento de datos. |
| **Streamlit** | Interfaz web interactiva, filtros y métricas del dashboard. |
| **Pandas** | Lectura, transformación y agrupación de los datos tabulares. |
| **Plotly Express** | Gráficos interactivos de barras, dona e histogramas. |
| **CSV** | Formato del conjunto de datos `dataset_latam.csv`. |

---

🌱 **Un proyecto de exploración de datos para entender mejor el pulso digital de Latinoamérica.**
