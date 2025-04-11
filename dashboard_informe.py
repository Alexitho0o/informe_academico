import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import BytesIO, StringIO

# === Configuración de la página ===
st.set_page_config(page_title="📊 Informe Académico", layout="wide")
st.title("📄 Informe Académico Interactivo")

# === Escala embebida de conversión de puntaje a nota ===
escala_str = '''Ptos\tNOTA
1\t1.1
2\t1.1
3\t1.2
4\t1.2
5\t1.3
6\t1.3
7\t1.4
8\t1.4
9\t1.5
10\t1.5
11\t1.6
12\t1.6
13\t1.7
14\t1.7
15\t1.8
16\t1.8
17\t1.9
18\t1.9
19\t2.0
20\t2.0
21\t2.1
22\t2.1
23\t2.2
24\t2.2
25\t2.3
26\t2.3
27\t2.4
28\t2.4
29\t2.5
30\t2.5
31\t2.6
32\t2.6
33\t2.7
34\t2.7
35\t2.8
36\t2.8
37\t2.9
38\t2.9
39\t3.0
40\t3.0
41\t3.1
42\t3.1
43\t3.2
44\t3.2
45\t3.3
46\t3.3
47\t3.4
48\t3.4
49\t3.5
50\t3.5
51\t3.6
52\t3.6
53\t3.7
54\t3.7
55\t3.8
56\t3.8
57\t3.9
58\t3.9
59\t4.0
60\t4.0
61\t4.1
62\t4.2
63\t4.2
64\t4.3
65\t4.4
66\t4.5
67\t4.5
68\t4.6
69\t4.7
70\t4.8
71\t4.8
72\t4.9
73\t5.0
74\t5.1
75\t5.1
76\t5.2
77\t5.3
78\t5.4
79\t5.4
80\t5.5
81\t5.6
82\t5.7
83\t5.7
84\t5.8
85\t5.9
86\t6.0
87\t6.0
88\t6.1
89\t6.2
90\t6.3
91\t6.3
92\t6.4
93\t6.5
94\t6.6
95\t6.6
96\t6.7
97\t6.8
98\t6.9
99\t6.9
100\t7.0'''
df_escala = pd.read_csv(StringIO(escala_str), sep="\t")

# === Subida de archivos ===
col1, col2 = st.columns(2)
with col1:
    archivo_1 = st.file_uploader("📁 Archivo 1: Lista de inscritos", type=["xlsx", "xls"], key="a1")
with col2:
    archivo_2 = st.file_uploader("📄 Archivo 2: Resultados de evaluación", type=["xlsx", "xls"], key="a2")

# === Cláusulas de guardia ===
if not archivo_1 or not archivo_2:
    st.info("🟡 Sube ambos archivos para comenzar.")
    st.stop()

df1 = pd.read_excel(archivo_1)
df2 = pd.read_excel(archivo_2)
df1.columns = df1.columns.str.strip()
df2.columns = df2.columns.str.strip()

key = "Nombre de usuario"
if key not in df1.columns or key not in df2.columns:
    st.error("❌ Ambos archivos deben contener la columna 'Nombre de usuario'")
    st.stop()

if "Calificación/100,00" not in df2.columns:
    st.error("❌ No se encontró la columna 'Calificación/100,00'")
    st.stop()

# === Procesamiento de notas ===
df2.rename(columns={"Calificación/100,00": "PUNTAJE"}, inplace=True)
df2["PUNTAJE"] = df2["PUNTAJE"].astype(str).str.replace(",", ".").str.extract(r"([0-9.]+)")[0]
df2["PUNTAJE"] = pd.to_numeric(df2["PUNTAJE"], errors="coerce").fillna(0).astype(int)
df2 = df2.merge(df_escala, how="left", left_on="PUNTAJE", right_on="Ptos")
df2["NOTA"] = df2["NOTA"].fillna(1.0)
df2["ESTADO"] = np.where(df2["NOTA"] >= 4.0, "Aprobado", "Reprobado")

df = df1.merge(df2[[key, "PUNTAJE", "NOTA", "ESTADO"]], on=key, how="left")
df["ESTADO"] = df["ESTADO"].fillna("Sin evaluación")
df["NOTA TEXTO"] = df["NOTA"].apply(lambda x: f"{x:.1f}" if pd.notnull(x) else "no rendido")
df["NOTA_NUM"] = pd.to_numeric(df["NOTA"], errors="coerce")
df.drop(columns=["Grupo"], errors="ignore", inplace=True)
df.reset_index(drop=True, inplace=True)
df.index += 1

st.markdown("""
**🎨 Rangos de color utilizados:**  
🟩 **Aprobado** (6.0 - 7.0)  
🟧 **Regular** (4.0 - 5.9)  
🟥 **Reprobado** (1.0 - 3.9)
""")

# === KPIs ===
total = len(df)
evaluados = df[df["NOTA TEXTO"] != "no rendido"]
sin_eval = df["NOTA TEXTO"].eq("no rendido").sum()

st.subheader("📊 KPIs Académicos")
col1, col2, col3, col4 = st.columns(4)
col1.metric("👥 Inscritos", total)
col2.metric("🧪 Evaluados", len(evaluados))
col3.metric("🚫 No rendido", sin_eval)
col4.metric("📈 Participación", f"{100 * (1 - sin_eval / total):.1f}%")

if not evaluados.empty:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("✅ Aprobación", f"{(evaluados['ESTADO'] == 'Aprobado').mean() * 100:.1f}%")
    col2.metric("❌ Reprobación", f"{(evaluados['ESTADO'] == 'Reprobado').mean() * 100:.1f}%")
    col3.metric("📊 Mediana", f"{evaluados['NOTA'].median():.2f}")
    col4.metric("📉 Moda", f"{evaluados['NOTA'].mode().iloc[0]:.2f}")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("⬆️ Máxima", f"{evaluados['NOTA'].max():.2f}")
    col2.metric("⬇️ Mínima", f"{evaluados['NOTA'].min():.2f}")
    col3.metric("📏 Desv. Est.", f"{evaluados['NOTA'].std():.2f}")
    col4.metric("🥇 Nº con Nota Máxima", (evaluados["NOTA"] == 7.0).sum())

# === Filtro por estado ===
st.subheader("🎯 Filtrar resultados por estado")
estado_sel = st.radio("Filtrar:", ["Todos", "Aprobado", "Reprobado", "Sin evaluación"], horizontal=True, index=0)

if estado_sel == "Todos":
    df_filtrado = df
else:
    df_filtrado = df[df["ESTADO"] == estado_sel]

# === Resultados Detallados ===
st.subheader("📋 Resultados Detallados")
st.markdown("""
<style>
thead th {text-align: center !important; font-weight: bold; text-transform: uppercase;}
tbody td {text-align: center !important;}
</style>
""", unsafe_allow_html=True)

st.dataframe(
    df_filtrado
    .drop(columns=["NOTA", "NOTA_NUM", "Nombre de usuario", "Grupos"], errors="ignore")
    .rename(columns={"NOTA TEXTO": "NOTA"}),
    use_container_width=True
)

# === Función auxiliar para aplicar filtro por color ===
def generar_graficos(df_base, filtro_key):
    filtro = st.radio(
        f"🎨 Filtrar por Rango de Nota ({filtro_key})",
        ["Todos", "Aprobado (6.0 - 7.0)", "Regular (4.0 - 5.9)", "Reprobado (1.0 - 3.9)"],
        index=0,
        horizontal=True,
        key=filtro_key
    )
    
    filtro_map = {
        "Todos": ["green", "orange", "red"],
        "Aprobado (6.0 - 7.0)": ["green"],
        "Regular (4.0 - 5.9)": ["orange"],
        "Reprobado (1.0 - 3.9)": ["red"]
    }
    
    color_dict = {
        "green": "#2ecc71",   # Aprobado
        "orange": "#f39c12",  # Regular
        "red": "#e74c3c"      # Reprobado
    }

    df_plot = df_base[df_base["NOTA TEXTO"] != "no rendido"].copy()
    df_plot["NOTA"] = pd.to_numeric(df_plot["NOTA TEXTO"], errors="coerce")
    df_plot["Color"] = pd.cut(
        df_plot["NOTA"],
        bins=[0, 3.9, 5.9, 7.1],
        labels=["red", "orange", "green"]
    )
    df_plot = df_plot[df_plot["Color"].isin(filtro_map[filtro])]
    return df_plot, color_dict

# === Análisis Visual de Notas ===
st.subheader("📈 Análisis Visual de las Notas")

# Filtro 1 - Histogram y Boxplot
df_plot1, color_dict = generar_graficos(df_filtrado, "filtro1")
filtro_map_label = {
    "green": "Aprobado (6.0 - 7.0)",
    "orange": "Regular (4.0 - 5.9)",
    "red": "Reprobado (1.0 - 3.9)"
}

col_g1, col_g2 = st.columns(2)
with col_g1:
    fig1 = px.histogram(df_plot1, x="NOTA", color="Color", nbins=20,
                        color_discrete_map=color_dict,
                        category_orders={"Color": ["red", "orange", "green"]})
    fig1.update_layout(
        title=dict(text="📊 Frecuencia de Notas - ¿Cuántas veces se repite cada nota?", x=0.0),
        showlegend=True,
        legend_title_text="Rango"
    )
    fig1.for_each_trace(lambda t: t.update(name=filtro_map_label[t.name]))
    st.plotly_chart(fig1, use_container_width=True)
    st.caption("🔹 El histograma muestra cuántas veces se repite cada nota en el rango seleccionado.")

with col_g2:
    fig2 = px.box(df_plot1, y="NOTA", color="Color", points="all",
                  color_discrete_map=color_dict)
    fig2.update_layout(
        title=dict(text="📦 Boxplot - Rango y valores atípicos de las notas", x=0.0),
        showlegend=True,
        legend_title_text="Rango"
    )
    fig2.for_each_trace(lambda t: t.update(name=filtro_map_label[t.name]))
    st.plotly_chart(fig2, use_container_width=True)
    st.caption("🔹 El boxplot permite visualizar la dispersión, valores atípicos y rangos intercuartiles de las notas.")

# Filtro 2 - Violin y Pie chart
df_plot2, _ = generar_graficos(df_filtrado, "filtro2")
col_g3, col_g4 = st.columns(2)
with col_g3:
    fig3 = px.violin(df_plot2, y="NOTA", box=True, points="all", color="Color",
                     color_discrete_map=color_dict)
    fig3.update_layout(
        title=dict(text="🎻 Violín Plot - Densidad y forma de distribución", x=0.0),
        showlegend=True,
        legend_title_text="Rango"
    )
    fig3.for_each_trace(lambda t: t.update(name=filtro_map_label[t.name]))
    st.plotly_chart(fig3, use_container_width=True)
    st.caption("🔹 El gráfico de violín combina distribución, densidad y estadísticos como la mediana y cuartiles.")

with col_g4:
    count_by_color = df_plot2["Color"].value_counts().reset_index()
    count_by_color.columns = ["Rango", "Cantidad"]
    color_names = {"red": "Reprobado (1.0 - 3.9)", "orange": "Regular (4.0 - 5.9)", "green": "Aprobado (6.0 - 7.0)"}
    count_by_color["Etiqueta"] = count_by_color["Rango"].map(color_names)

    fig4 = px.pie(count_by_color, names="Etiqueta", values="Cantidad",
                  color="Rango", color_discrete_map=color_dict, hole=0.4)
    fig4.update_layout(
        title=dict(text="📎 Proporción por Rango de Nota", x=0.0),
        showlegend=True,
        legend_title_text="Rango"
    )
    st.plotly_chart(fig4, use_container_width=True)
    st.caption("🔹 El gráfico de torta refleja visualmente el porcentaje de estudiantes en cada tramo de nota.")

# === Exportar resultados ===
def to_excel(df):
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=True, sheet_name="Resultados")
    buffer.seek(0)
    return buffer

st.download_button(
    label="📥 Exportar Resultados",
    data=to_excel(df),
    file_name="resultados_informe.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# === Explicación ===
with st.expander("ℹ️ ¿Qué significa cada KPI?"):
    st.markdown("""
**Inscritos:** Total de estudiantes registrados.  
**Evaluados:** Estudiantes con nota registrada.  
**No rendido:** Estudiantes sin nota, se marca como “no rendido”.  
**Participación:** Porcentaje de estudiantes evaluados.  
**Aprobación/Reprobación:** % según nota ≥ 4.0.  
**Mediana / Moda / Máxima / Mínima / Desv. Est.:** Estadísticas básicas.  
**Nota Máxima:** Estudiantes con nota 7.0.

**🎨 Rangos de color utilizados:**  
🟩 **Aprobado** (6.0 - 7.0)  
🟧 **Regular** (4.0 - 5.9)  
🟥 **Reprobado** (1.0 - 3.9)

---
**📌 Observaciones del resultado obtenido**  
Un nivel alto de “No rendido” puede indicar falta de motivación, problemas logísticos o fallos de convocatoria.  
Un porcentaje de aprobación bajo puede estar relacionado con dificultad del contenido, problemas de comprensión o evaluación poco alineada.  
La dispersión (desv. estándar) y los valores extremos ayudan a detectar inequidad en el rendimiento.
""")