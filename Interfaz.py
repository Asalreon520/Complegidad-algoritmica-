import tkinter as tk
import tkinter as tk
from tkinter import ttk

def iniciar_juego():
    jugador1 = entrada_jugador1.get()
    algoritmo = combo_algoritmo.get()
    print(f"Jugador 1: {jugador1}")
    print(f"Jugador 2 seleccionó el algoritmo: {algoritmo}")

ventana = tk.Tk()
ventana.title("Hito 02 - Simulador de Damas")

titulo = tk.Label(ventana, text="HITO 02", font=("Arial", 18))
titulo.pack(pady=10)

label_jugador1 = tk.Label(ventana, text="Nombre del Jugador 1:")
label_jugador1.pack()

entrada_jugador1 = tk.Entry(ventana)
entrada_jugador1.pack(pady=5)

label_jugador2 = tk.Label(ventana, text="Algoritmo para Jugador 2:")
label_jugador2.pack()

combo_algoritmo = ttk.Combobox(ventana, values=["Backtracking", "Programación Dinámica"])
combo_algoritmo.set("Seleccionar Algoritmo")
combo_algoritmo.pack(pady=5)

boton_iniciar = tk.Button(ventana, text="Iniciar Juego", command=iniciar_juego)
boton_iniciar.pack(pady=10)

ventana.mainloop()
