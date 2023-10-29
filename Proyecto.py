import numpy as np
import tkinter as tk
from tkinter import Label, Entry, Button, Text, Radiobutton

def calcular_inversa():
    entrada = entrada_matriz.get()
    try:
        matriz = np.array(eval(entrada), dtype=float)
        matriz_inversa = np.linalg.inv(matriz)
        resultado.config(state="normal")
        resultado.delete(1.0, tk.END)
        resultado.insert(tk.END, "Inversa de la matriz:\n" + str(matriz_inversa))
        resultado.config(state="disabled")
    except Exception as e:
        resultado.config(state="normal")
        resultado.delete(1.0, tk.END)
        resultado.insert(tk.END, "Error al calcular la inversa.")
        resultado.config(state="disabled")

def multiplicar_matrices():
    entrada1 = entrada_matriz1.get()
    entrada2 = entrada_matriz2.get()
    try:
        matriz1 = np.array(eval(entrada1), dtype=float)
        matriz2 = np.array(eval(entrada2), dtype=float)
        resultado_matriz = np.dot(matriz1, matriz2)
        resultado.config(state="normal")
        resultado.delete(1.0, tk.END)
        resultado.insert(tk.END, "Resultado de la multiplicación de matrices:\n" + str(resultado_matriz))
        resultado.config(state="disabled")
    except Exception as e:
        resultado.config(state="normal")
        resultado.delete(1.0, tk.END)
        resultado.insert(tk.END, "Error al multiplicar las matrices.")
        resultado.config(state="disabled")

def resolver_sistema():
    ecuaciones_str = entrada_ecuaciones.get("1.0", "end-1c")
    try:
        ecuaciones = eval(ecuaciones_str)
        filas, columnas = len(ecuaciones), len(ecuaciones[0])

        metodo_seleccionado = metodo_var.get()

        if filas == columnas - 1:
            if metodo_seleccionado == "Cramer":
                solucion = regla_cramer(ecuaciones)
            elif metodo_seleccionado == "Gauss-Jordan":
                solucion = gauss_jordan(ecuaciones)
            else:
                solucion = "Método no válido."

            resultado.config(state="normal")
            resultado.delete(1.0, tk.END)
            resultado.insert(tk.END, "Solución:\n" + solucion)
            resultado.config(state="disabled")

        else:
            solucion = "La Regla de Cramer y el método de Gauss-Jordan solo se aplican a sistemas cuadrados de 2x2, 3x3 y 4x4."

            resultado.config(state="normal")
            resultado.delete(1.0, tk.END)
            resultado.insert(tk.END, "Solución:\n" + solucion)
            resultado.config(state="disabled")

    except Exception as e:
        resultado.config(state="normal")
        resultado.delete(1.0, tk.END)
        resultado.insert(tk.END, "Error al resolver el sistema.")
        resultado.config(state="disabled")

def regla_cramer(ecuaciones):
    try:
        n = len(ecuaciones)
        A = np.array([fila[:-1] for fila in ecuaciones])
        b = np.array([fila[-1] for fila in ecuaciones])

        det_A = np.linalg.det(A)
        if det_A == 0:
            return "Sin solución (determinante de A igual a 0)."

        soluciones = []
        for i in range(n):
            temp_A = A.copy()
            temp_A[:, i] = b
            soluciones.append(np.linalg.det(temp_A) / det_A)

        return f"Solución única: {soluciones}"
    except Exception as e:
        return "Error al resolver el sistema."

def gauss_jordan(ecuaciones):
    try:
        n = len(ecuaciones)
        augmented_matrix = np.array([fila[:] for fila in ecuaciones], dtype=float)
        for i in range(n):
            pivot = augmented_matrix[i][i]
            if pivot == 0:
                return "Sin solución (elemento diagonal igual a 0)."
            augmented_matrix[i] = augmented_matrix[i] / pivot
            for j in range(n):
                if i != j:
                    factor = augmented_matrix[j][i]
                    augmented_matrix[j] = augmented_matrix[j] - factor * augmented_matrix[i]

        soluciones = augmented_matrix[:, -1]
        return f"Solución única: {soluciones}"
    except Exception as e:
        return "Error al resolver el sistema."

def limpiar_resultados():
    resultado.config(state="normal")
    resultado.delete(1.0, tk.END)
    resultado.config(state="disabled")
    
def limpiar_entradas():
    entrada_matriz.delete(0, tk.END)
    entrada_matriz1.delete(0, tk.END)
    entrada_matriz2.delete(0, tk.END)
    entrada_ecuaciones.delete("1.0", tk.END)
    
ventana = tk.Tk()
ventana.title("Calculadora de Matrices y Resolución de Sistemas de Ecuaciones")

ventana.configure(bg='#f0f0f0')
btn_color = '#4CAF50'
btn_fg_color = 'white'

Label(ventana, text="Ingrese la matriz (formato (1,2),(3,4)):", bg='#f0f0f0').pack()
entrada_matriz = Entry(ventana)
entrada_matriz.pack()

btn_calcular_inversa = Button(ventana, text="Calcular Inversa", command=calcular_inversa, bg=btn_color, fg=btn_fg_color)
btn_calcular_inversa.pack()

Label(ventana, text="Ingrese la primera matriz (formato (1,2),(3,4)):", bg='#f0f0f0').pack()
entrada_matriz1 = Entry(ventana)
entrada_matriz1.pack()

Label(ventana, text="Ingrese la segunda matriz (formato (1,2),(3,4)):", bg='#f0f0f0').pack()
entrada_matriz2 = Entry(ventana)
entrada_matriz2.pack()

btn_multiplicar_matrices = Button(ventana, text="Multiplicar Matrices", command=multiplicar_matrices, bg=btn_color, fg=btn_fg_color)
btn_multiplicar_matrices.pack()

Label(ventana, text="Ingrese el sistema de ecuaciones (ejemplo: (2, 3, 4, 7), (1, 2, 3, 5), (3, 2, 1, 6) para 3x3. De la misma manera con 2x2 y 4x4):", bg='#f0f0f0').pack()
entrada_ecuaciones = Text(ventana, height=5, width=40)
entrada_ecuaciones.pack()

Label(ventana, text="Seleccione el método de resolución:", bg='#f0f0f0').pack()
metodo_var = tk.StringVar()
metodo_var.set("Cramer")
Radiobutton(ventana, text="Regla de Cramer", variable=metodo_var, value="Cramer").pack()
Radiobutton(ventana, text="Gauss-Jordan", variable=metodo_var, value="Gauss-Jordan").pack()

btn_resolver = Button(ventana, text="Resolver Sistema", command=resolver_sistema, bg=btn_color, fg=btn_fg_color)
btn_resolver.pack()

resultado = Text(ventana, height=15, width=40, bg='#f0f0f0')
resultado.config(state="disabled")
resultado.pack()

btn_limpiar_resultados = Button(ventana, text="Limpiar Resultados", command=limpiar_resultados, bg="red", fg="white")
btn_limpiar_resultados.pack(side=tk.LEFT)

btn_limpiar_entradas = Button(ventana, text="Limpiar Entradas", command=limpiar_entradas, bg="blue", fg="white")
btn_limpiar_entradas.pack(side=tk.LEFT)

Label(ventana, text="Nota: La Regla de Cramer y el método de Gauss-Jordan se aplican a sistemas cuadrados de 2x2, 3x3 y 4x4.", fg="red", bg='#f0f0f0').pack()

ventana.mainloop()
