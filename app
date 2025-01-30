import streamlit as st
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

# Configurar la aplicación
st.title("📈 Verificador de Función Convexa")
st.write("Ingrese una función en términos de `x` y verificaremos si es convexa.")

# Entrada de la función
func_str = st.text_input("✍️ Ingrese la función f(x):", value="x**2")

if func_str:
    try:
        # Definir la variable simbólica
        x = sp.Symbol('x')

        # Convertir la función ingresada en expresión simbólica
        func = sp.sympify(func_str)

        # Calcular la primera y segunda derivada
        first_derivative = sp.diff(func, x)
        second_derivative = sp.diff(first_derivative, x)

        # Mostrar las derivadas
        st.latex(f"f'(x) = {sp.latex(first_derivative)}")
        st.latex(f"f''(x) = {sp.latex(second_derivative)}")

        # Evaluar la convexidad en un rango de valores
        x_vals = np.linspace(-10, 10, 400)
        f_vals = np.array([func.subs(x, val).evalf() for val in x_vals])
        f2_vals = np.array([second_derivative.subs(x, val).evalf() for val in x_vals])

        # Determinar si la función es convexa
        is_convex = np.all(f2_vals >= 0)

        # Mostrar resultado
        if is_convex:
            st.success("✅ La función es convexa en el dominio analizado.")
        else:
            st.error("❌ La función NO es convexa en el dominio analizado.")

        # Graficar la función y su segunda derivada
        fig, ax = plt.subplots()
        ax.plot(x_vals, f_vals, label="f(x)", linewidth=2)
        ax.plot(x_vals, f2_vals, linestyle="dashed", label="f''(x)", linewidth=2)
        ax.axhline(0, color="black", linewidth=1)
        ax.set_xlabel("x")
        ax.set_ylabel("Valores")
        ax.legend()
        ax.set_title("Función y su Segunda Derivada")
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Error al procesar la función: {e}")
