# Cristian Guevara 31.567.525
import tkinter as tk
from tkinter import filedialog, scrolledtext
import re

# Función para analizar el código ingresado en el área de texto
def analizar_codigo():
    # Obtener el código del área de texto
    codigo = text_area.get("1.0", tk.END)
    # Analizar el código léxicamente
    tokens = analizar_lexico(codigo)
    # Mostrar los resultados del análisis
    mostrar_resultados(tokens)

# Función para cargar un archivo de texto
def cargar_archivo():
    # Abrir un cuadro de diálogo para seleccionar un archivo de texto
    archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
    if archivo:
        # Leer el contenido del archivo y mostrarlo en el área de texto
        with open(archivo, "r") as f:
            text_area.delete("1.0", tk.END)
            text_area.insert(tk.END, f.read())

def analizar_lexico(codigo):
    # Definir los patrones en orden de prioridad
    patrones = [
        ("Comentario", r"//.*|/\*[\s\S]*?\*/"),  
        ("Cadena", r"\".*?\""),  
        ("Palabra_clave", r"\b(class|public|private|protected|static|void|int|String|double|float|if|else|while|for|return|new)\b"),
        ("Numero", r"\b\d+(\.\d+)?\b"),
        ("Simbolo", r"[{}();,\[\]]"),
        ("Operador", r"[+\-*/=<>!]"),
        ("Identificador", r"\b[a-zA-Z_][a-zA-Z0-9_]*\b")  # Identificadores al final
    ]
    
    tokens = []
    
    # Unir los patrones en una sola expresión regular
    patron_combinado = "|".join(f"(?P<{tipo}>{patron})" for tipo, patron in patrones)
    
    # Buscar coincidencias en el código
    for match in re.finditer(patron_combinado, codigo):
        for nombre_tipo, _ in patrones:
            if match.group(nombre_tipo):
                tokens.append((match.group(nombre_tipo), nombre_tipo.replace("_", " ")))  # Restaurar espacios en la salida
                break  # Detenerse en la primera coincidencia válida
    
    return tokens

# Función para mostrar los resultados del análisis léxico
def mostrar_resultados(tokens):
    resultado_area.config(state=tk.NORMAL)
    resultado_area.delete("1.0", tk.END)
    # Insertar los tokens y sus tipos en el área de resultados
    for token, tipo in tokens:
        resultado_area.insert(tk.END, f"{token}: {tipo}\n")
    resultado_area.config(state=tk.DISABLED)

# Función para limpiar el área de resultados
def limpiar_salida():
    resultado_area.config(state=tk.NORMAL)
    resultado_area.delete("1.0", tk.END)
    resultado_area.config(state=tk.DISABLED)

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Analizador Léxico de Java")
root.configure(background='lightblue')  # Cambiar el color de fondo de la ventana principal

# Definir la tipografía
font = ("Helvetica", 12, "bold")  # Tipografía en negrita
font2 = ("Helvetica", 12)  # Tipografía en negrita

frame = tk.Frame(root, bg='lightblue')  # Cambiar el color de fondo del frame
frame.pack(pady=10)

text_area = scrolledtext.ScrolledText(frame, width=60, height=15, bg='white', fg='black', font=font2)  # Cambiar los colores de fondo y texto del área de texto
text_area.pack()

btn_frame = tk.Frame(root, bg='lightblue')  # Cambiar el color de fondo del frame de los botones
btn_frame.pack(pady=5)

# Función para crear botones con bordes redondeados
def crear_boton(frame, text, command):
    return tk.Button(frame, text=text, command=command, bg='gray', fg='white', font=font, relief='flat', highlightbackground='gray', highlightthickness=0, bd=0, padx=10, pady=5)

btn_cargar = crear_boton(btn_frame, "Cargar Archivo", cargar_archivo)
btn_cargar.grid(row=0, column=0, padx=5)

btn_analizar = crear_boton(btn_frame, "Analizar Código", analizar_codigo)
btn_analizar.grid(row=0, column=1, padx=5)

btn_limpiar = crear_boton(btn_frame, "Limpiar Salida", limpiar_salida)
btn_limpiar.grid(row=0, column=2, padx=5)

resultado_area = scrolledtext.ScrolledText(root, width=60, height=10, state=tk.DISABLED, bg='white', fg='black', font=font)  # Cambiar los colores del área de resultados
resultado_area.pack(pady=10)

root.mainloop()

