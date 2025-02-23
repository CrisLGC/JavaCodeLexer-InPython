# Cristian Guevara 31.567.525
import tkinter as tk
from tkinter import filedialog, scrolledtext
import re

def analizar_codigo():
    codigo = text_area.get("1.0", tk.END)
    tokens = analizar_lexico(codigo)
    mostrar_resultados(tokens)

def cargar_archivo():
    archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
    if archivo:
        with open(archivo, "r") as f:
            text_area.delete("1.0", tk.END)
            text_area.insert(tk.END, f.read())

def analizar_lexico(codigo):
    patrones = {
        "Palabra clave": r"\b(class|public|private|protected|static|void|int|double|float|if|else|while|for|return|new)\b",
        "Identificador": r"\b[a-zA-Z_][a-zA-Z0-9_]*\b",
        "Número": r"\b\d+(\.\d+)?\b",
        "Símbolo": r"[{}();,]",
        "Operador": r"[+\-*/=<>!]"
    }
    
    tokens = []
    for tipo, patron in patrones.items():
        for match in re.finditer(patron, codigo):
            tokens.append((match.group(), tipo))
    
    return tokens

def mostrar_resultados(tokens):
    resultado_area.config(state=tk.NORMAL)
    resultado_area.delete("1.0", tk.END)
    for token, tipo in tokens:
        resultado_area.insert(tk.END, f"{token}: {tipo}\n")
    resultado_area.config(state=tk.DISABLED)

def limpiar_salida():
    resultado_area.config(state=tk.NORMAL)
    resultado_area.delete("1.0", tk.END)
    resultado_area.config(state=tk.DISABLED)

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Analizador Léxico de Java")

frame = tk.Frame(root)
frame.pack(pady=10)

text_area = scrolledtext.ScrolledText(frame, width=60, height=15)
text_area.pack()

btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)

btn_cargar = tk.Button(btn_frame, text="Cargar Archivo", command=cargar_archivo)
btn_cargar.grid(row=0, column=0, padx=5)

btn_analizar = tk.Button(btn_frame, text="Analizar Código", command=analizar_codigo)
btn_analizar.grid(row=0, column=1, padx=5)

btn_limpiar = tk.Button(btn_frame, text="Limpiar Salida", command=limpiar_salida)
btn_limpiar.grid(row=0, column=2, padx=5)

resultado_area = scrolledtext.ScrolledText(root, width=60, height=10, state=tk.DISABLED)
resultado_area.pack(pady=10)

root.mainloop()

