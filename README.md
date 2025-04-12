# 📊 Informe Académico Interactivo

Este sistema permite generar informes dinámicos y visuales a partir de archivos exportados desde Moodle.

## 🧾 ¿Qué hace?
- Lee dos archivos Excel: lista de inscritos y resultados de evaluación.
- Convierte automáticamente los puntajes a notas según una escala interna.
- Muestra indicadores clave (KPIs), tablas y gráficos interactivos.
- Permite exportar los resultados en formato Excel.

## 📂 ¿Qué necesito subir?
1. `archivo 1.xlsx`: Lista de inscritos (con columna "Nombre de usuario")
2. `archivo 2.xlsx`: Notas exportadas desde Moodle (con columna "Calificación/100,00")

## 📈 Indicadores automáticos
- Inscritos, evaluados, no rendidos
- Aprobación / Reprobación
- Mediana, moda, máxima, mínima
- Análisis visual (histograma, boxplot, violín, torta)

## ▶️ Ver la app online
[Accede aquí a la app publicada](https://informe-academico.streamlit.app) *(se activará al desplegar)*

---

Desarrollado con ❤️ usando Python, Streamlit y Plotly.
