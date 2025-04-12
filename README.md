# 📊 Informe Académico Interactivo

Esta aplicación permite generar informes visuales y automatizados a partir de archivos exportados desde Moodle. Ideal para docentes, coordinadores y equipos académicos que desean visualizar rápidamente el rendimiento estudiantil.

---

## 🧾 Funcionalidades principales

- 📂 **Carga automática de datos** desde dos archivos Excel: lista de inscritos y notas.
- 🧮 **Conversión de puntajes a notas** utilizando una escala interna personalizada.
- 📊 **Visualización de indicadores clave (KPIs)** del curso en tiempo real.
- 📈 **Gráficos interactivos**: histogramas, boxplots, violin plots y gráficos de torta.
- 📥 **Exportación de resultados** en formato Excel con estado y nota final.

---

## 📁 ¿Qué archivos debes subir?

1. `archivo 1.xlsx`: Lista de inscritos  
   → Debe contener la columna: **"Nombre de usuario"**

2. `archivo 2.xlsx`: Resultados desde Moodle  
   → Debe contener la columna: **"Calificación/100,00"**

---

## 📈 Indicadores automáticos generados

- Total de inscritos, evaluados y no evaluados
- Porcentaje de aprobación y reprobación
- Nota máxima, mínima, mediana y moda
- Distribución de notas por rango (Aprobado, Regular, Reprobado)
- Visualización con filtros por tramo de nota

---

## ▶️ Acceso a la aplicación

👉 [Haz clic aquí para usar la app en línea](https://ip-san-sebastian-informe.streamlit.app/)

> Puedes usarla desde cualquier dispositivo con conexión a internet.

---

### ⚙️ Tecnologías utilizadas

Desarrollado con ❤️ usando:

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [Plotly](https://plotly.com/python/)
- [Pandas](https://pandas.pydata.org/)

---

¿Quieres mejorar esta app o adaptarla a tu institución? ¡Estoy para ayudarte!
