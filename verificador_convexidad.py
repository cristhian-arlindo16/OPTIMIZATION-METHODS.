import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ==============================
# CONFIGURACIÓN DE LA PÁGINA
# ==============================
st.set_page_config(page_title="Verificador de Convexidad", page_icon="📈", layout="centered")

# ==============================
# TÍTULO Y DESCRIPCIÓN
# ==============================
st.title("📈 Verificador de Convexidad de Funciones Matemáticas")
st.markdown("""
Esta aplicación permite verificar si una función matemática es **convexa** en un intervalo determinado.  
Ingrese una función en términos de `x` y el sistema calculará su **segunda derivada**,  
analizando si cumple la condición de **convexidad**.

🔹 **Convexidad:** Una función \( f(x) \) es convexa si su segunda derivada \( f''(x) \geq 0 \) en un intervalo.
""")

# ==============================
# ENTRADA DE DATOS (SIDEBAR)
# ==============================
st.sidebar.header("📌 Parámetros de Entrada")

# Función ingresada por el usuario
func_str = st.sidebar.text_input("✍️ Ingrese la función f(x):", value="x**2")

# Intervalo para el análisis
st.sidebar.markdown("📌 **Seleccione el intervalo de análisis:**")
col1, col2 = st.sidebar.columns(2)
x_min = col1.number_input("🔹 Inicio", value=-10.0)
x_max = col2.number_input("🔹 Fin", value=10.0)

# Verificación de valores inválidos
if x_min >= x_max:
    st.sidebar.error("⚠️ El inicio del intervalo debe ser menor que el fin.")
    st.stop()

# ==============================
# CÁLCULO DE DERIVADAS Y ANÁLISIS
# ==============================
try:
    # Crear el rango de valores de x
    x_vals = np.linspace(x_min, x_max, 400)

    # Convertir la función ingresada en una expresión evaluable con NumPy
    def f(x):
        try:
            return eval(func_str, {"x": x, "np": np})
        except Exception:
            return np.nan  # Retorna NaN si hay error en la función

    # Evaluar la función en el dominio
    f_vals = f(x_vals)

    # Verificación: Si hay valores NaN, detener el programa
    if np.isnan(f_vals).any():
        st.error("⚠️ Error en la función ingresada. Revise la sintaxis.")
        st.stop()

    # Calcular la primera y segunda derivada usando numpy.gradient
    f_prime_vals = np.gradient(f_vals, x_vals)
    f_double_prime_vals = np.gradient(f_prime_vals, x_vals)

    # Determinar si la función es convexa en el dominio
    is_convex = np.all(f_double_prime_vals >= 0)

    # ==============================
    # RESULTADO Y VISUALIZACIÓN
    # ==============================
    st.markdown("## 📊 Resultados del Análisis")

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
    ax.plot(x_vals, f_double_prime_vals, linestyle="dashed", label="f''(x)", linewidth=2, color='red')
    ax.axhline(0, color="black", linewidth=1, linestyle="--")
    ax.set_xlabel("x")
    ax.set_ylabel("Valores")
    ax.legend()
    ax.set_title("Función y su Segunda Derivada")
    st.pyplot(fig)

except Exception as e:
    st.error(f"❌ Error inesperado: {e}")
    st.warning("Asegúrese de ingresar una función válida en términos de 'x'. Ejemplo: `x**2`, `np.exp(x)`, `np.sin(x)`, etc.")
