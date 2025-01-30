import streamlit as st
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

# ==============================
# CONFIGURACIÓN DE LA PÁGINA
# ==============================
st.set_page_config(page_title="Verificación de Convexidad", page_icon="📈", layout="centered")

# ==============================
# TÍTULO Y DESCRIPCIÓN
# ==============================
st.title("📈 Análisis de Convexidad de Funciones Matemáticas")
st.markdown("""
Este programa permite verificar si una función es **convexa** en un intervalo determinado.
Ingrese una función matemática en términos de `x` y el sistema calculará su **segunda derivada**, 
analizando si cumple la condición de **convexidad**.

🔹 **Convexidad:** Una función \( f(x) \) es convexa si su segunda derivada \( f''(x) \geq 0 \) en un intervalo.
""")

# ==============================
# ENTRADA DE LA FUNCIÓN
# ==============================
st.sidebar.header("📌 Parámetros de Entrada")

# Función ingresada por el usuario
func_str = st.sidebar.text_input("✍️ Ingrese la función f(x):", value="x**2")

# Intervalo para el análisis
st.sidebar.markdown("📌 **Seleccione el intervalo de análisis:**")
col1, col2 = st.sidebar.columns(2)
x_min = col1.number_input("🔹 Inicio", value=-10)
x_max = col2.number_input("🔹 Fin", value=10)

# ==============================
# CÁLCULO DE DERIVADAS Y ANÁLISIS
# ==============================
x = sp.Symbol('x')

try:
    # Convertir la función ingresada en una expresión simbólica
    func = sp.sympify(func_str)

    # Calcular derivadas
    first_derivative = sp.diff(func, x)
    second_derivative = sp.diff(first_derivative, x)

    # Evaluar la convexidad en un rango de valores
    x_vals = np.linspace(x_min, x_max, 400)
    f_vals = np.array([func.subs(x, val).evalf() for val in x_vals])
    f2_vals = np.array([second_derivative.subs(x, val).evalf() for val in x_vals])

    # Determinar si la función es convexa
    is_convex = np.all(f2_vals >= 0)

    # ==============================
    # RESULTADO Y VISUALIZACIÓN
    # ==============================
    st.markdown("## 📊 Resultados del Análisis")

    # Mostrar derivadas en formato matemático
    st.markdown("### 🔹 Primera y Segunda Derivada")
    st.latex(f"f'(x) = {sp.latex(first_derivative)}")
    st.latex(f"f''(x) = {sp.latex(second_derivative)}")

    # Mostrar resultado de la convexidad
    if is_convex:
        st.success("✅ La función es convexa en el intervalo analizado.")
    else:
        st.error("❌ La función NO es convexa en el intervalo analizado.")

    # ==============================
    # GRAFICAR FUNCIÓN Y SEGUNDA DERIVADA
    # ==============================
    st.markdown("### 📈 Gráfica de la Función y su Segunda Derivada")

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x_vals, f_vals, label="f(x)", linewidth=2)
    ax.plot(x_vals, f2_vals, linestyle="dashed", label="f''(x)", linewidth=2, color='red')
    ax.axhline(0, color="black", linewidth=1, linestyle="--")
    ax.set_xlabel("x")
    ax.set_ylabel("Valores")
    ax.legend()
    ax.set_title("Función y su Segunda Derivada")
    st.pyplot(fig)

except Exception as e:
    st.error(f"❌ Error al procesar la función: {e}")
    st.warning("Asegúrese de ingresar una función válida en términos de 'x'. Ejemplo: `x**2`, `exp(x)`, `sin(x)`, etc.")
