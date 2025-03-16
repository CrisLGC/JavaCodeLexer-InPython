# Cristian Guevara 31.567.525
import tkinter as tk
from tkinter import filedialog, scrolledtext
import re

def mostrar_menu_principal():
    menu_principal = tk.Tk()
    menu_principal.title("Menú Principal")
    menu_principal.configure(background='lightblue')
    
    font = ("Helvetica", 12, "bold")
    
    label = tk.Label(menu_principal, text="Seleccione una opción", font=font, bg='lightblue')
    label.pack(pady=20)
    
    btn_lexico = tk.Button(menu_principal, text="Analizador Léxico", command=lambda: iniciar_analizador_lexico(menu_principal), bg='gray', fg='white', font=font, relief='flat', highlightbackground='gray', highlightthickness=0, bd=0, padx=10, pady=5)
    btn_lexico.pack(pady=10)
    
    btn_sintactico = tk.Button(menu_principal, text="Analizador Sintáctico", command=lambda: iniciar_analizador_sintactico(menu_principal), bg='gray', fg='white', font=font, relief='flat', highlightbackground='gray', highlightthickness=0, bd=0, padx=10, pady=5)
    btn_sintactico.pack(pady=10)
    
    menu_principal.mainloop()

def iniciar_analizador_lexico(menu_principal):
    menu_principal.destroy()
    crear_interfaz_analizador_lexico()

def iniciar_analizador_sintactico(menu_principal):
    menu_principal.destroy()
    crear_interfaz_analizador_sintactico()

def regresar_menu_principal(root):
    root.destroy()
    mostrar_menu_principal()

# Función para analizar el código léxicamente
def analizar_codigo_lexico():
    # Obtener el código del área de texto
    codigo = text_area.get("1.0", tk.END)
    # Analizar el código léxicamente
    tokens, errores = analizar_lexico(codigo)
    # Mostrar los resultados del análisis
    mostrar_resultados_lexico(tokens, errores)

# Función para analizar el código sintácticamente
def analizar_codigo_sintactico():
    # Obtener el código del área de texto
    codigo = text_area.get("1.0", tk.END)
    # Analizar el código sintácticamente
    errores = analizar_sintactico(codigo)
    # Mostrar los resultados del análisis
    mostrar_resultados_sintactico(errores)

# Función para cargar un archivo de texto
def cargar_archivo():
    # Abrir un cuadro de diálogo para seleccionar un archivo de texto
    archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
    if archivo:
        # Leer el contenido del archivo y mostrarlo en el área de texto
        with open(archivo, "r") as f:
            text_area.delete("1.0", tk.END)
            text_area.insert(tk.END, f.read())

# Análisis léxico
def analizar_lexico(codigo):
    patrones = [
        ("Comentario", r"//.*|/\*[\s\S]*?\*/"),  
        ("Cadena", r"\".*?\""),  
        ("Palabra_clave", r"\b(import|class|public|private|protected|static|void|int|String|double|float|if|else|while|for|return|new)\b"),
        ("Numero", r"\b\d+(\.\d+)?\b"),
        ("Simbolo", r"[{}();,\[\]]"),
        ("Operador", r"[+\-*/=<>!]"),
        ("Identificador", r"\b[a-zA-Z_][a-zA-Z0-9_]*\b")
    ]
    
    palabras_clave = {"import", "class", "public", "private", "protected", "static", "void", "int", "String", "double", "float", "if", "else", "while", "for", "return", "new"}

    tokens = []
    errores = []
    
    patron_combinado = "|".join(f"(?P<{tipo}>{patron})" for tipo, patron in patrones)
    
    posicion = 0
    while posicion < len(codigo):
        match = re.match(patron_combinado, codigo[posicion:])
        if match:
            for nombre_tipo in patrones:
                if match.group(nombre_tipo[0]):
                    token = match.group(nombre_tipo[0])
                    if nombre_tipo[0] == "Identificador" and token in palabras_clave:
                        errores.append((token, "Identificador como palabra clave", posicion))
                    else:
                        tokens.append((token, nombre_tipo[0].replace("_", " "), token, posicion))
                    break
            posicion += len(token)
        else:
            error = codigo[posicion]
            errores.append((error, "Error léxico", posicion))
            posicion += 1

    return tokens, errores

# Análisis sintáctico (mejorado)
def analizar_sintactico(codigo):
    errores = []
    lineas = codigo.split('\n')  # Dividir el código en líneas

    # Palabras clave que no requieren punto y coma
    palabras_clave_bloque = {"class", "public", "static", "void", "if", "else", "for", "while", "do", "try", "catch", "finally"}

    # Palabras clave de Java
    palabras_clave_java = {"abstract", "assert", "boolean", "break", "byte", "case", "catch", "char", "class", "const", "continue", "default", "do", "double", "else", "enum", "extends", "final", "finally", "float", "for", "if", "goto", "implements", "import", "instanceof", "int", "interface", "long", "native", "new", "package", "private", "protected", "public", "return", "short", "static", "strictfp", "super", "switch", "synchronized", "this", "throw", "throws", "transient", "try", "void", "volatile", "while"}

    for i, linea in enumerate(lineas):
        linea = linea.strip()  # Eliminar espacios en blanco al inicio y final

        # Ignorar líneas vacías, comentarios y bloques de código
        if not linea or linea.startswith("//") or linea.startswith("/*") or linea.endswith("{"):
            continue

        # Verificar punto y coma al final de las sentencias, ignorando líneas que terminan en comentario
        if re.search(r'\b(int|double|float|String|char|boolean|void)\b', linea) and not re.search(r';\s*(//.*|/\*.*\*/)?$', linea) and not linea.strip().endswith('{') and not linea.strip().endswith('}'):
            errores.append((i + 1, "Falta punto y coma al final de la sentencia", len(linea)))


        # Verificar uso de palabras clave como identificadores
        palabras = re.findall(r'\b\w+\b', linea)  # Extraer palabras
        for palabra in palabras:
            if palabra in palabras_clave_java and not linea.strip().startswith(palabra):
                errores.append((f"Línea {i+1}", f"Uso de palabra clave '{palabra}' como identificador", i+1))

        # Verificar caracteres no válidos
        if "@" in linea:
            errores.append((f"Línea {i+1}", "Carácter no válido '@'", i+1))

        # Verificar cadenas no cerradas
        if linea.count('"') % 2 != 0:
            errores.append((f"Línea {i+1}", "Cadena no cerrada", i+1))

    return errores

def mostrar_resultados_sintactico(errores):
    resultado_area.config(state=tk.NORMAL)
    resultado_area.delete("1.0", tk.END)
    
    resultado_area.insert(tk.END, "Tabla de Errores Sintácticos:\n")
    resultado_area.insert(tk.END, f"{'Error':<20}{'Descripción':<30}{'Línea':<10}\n")
    resultado_area.insert(tk.END, "-"*60 + "\n")
    for error, descripcion, linea in errores:
        resultado_area.insert(tk.END, f"{error:<20}{descripcion:<30}{linea:<10}\n")
    
    resultado_area.config(state=tk.DISABLED)

def mostrar_resultados_lexico(tokens, errores):
    resultado_area.config(state=tk.NORMAL)
    resultado_area.delete("1.0", tk.END)
    
    resultado_area.insert(tk.END, f"{'Token':<20}{'Tipo':<20}{'Valor':<20}{'Posición':<10}\n")
    resultado_area.insert(tk.END, "-"*70 + "\n")
    for token, tipo, valor, posicion in tokens:
        resultado_area.insert(tk.END, f"{token:<20}{tipo:<20}{valor:<20}{posicion:<10}\n")
    
    resultado_area.insert(tk.END, "\nTabla de Errores:\n")
    resultado_area.insert(tk.END, f"{'Error':<20}{'Descripción':<30}{'Posición':<10}\n")
    resultado_area.insert(tk.END, "-"*60 + "\n")
    for error, descripcion, posicion in errores:
        resultado_area.insert(tk.END, f"{error:<20}{descripcion:<30}{posicion:<10}\n")
    
    resultado_area.config(state=tk.DISABLED)

# Mostrar resultados del análisis sintáctico


# Función para limpiar el área de resultados
def limpiar_salida():
    resultado_area.config(state=tk.NORMAL)
    resultado_area.delete("1.0", tk.END)
    resultado_area.config(state=tk.DISABLED)

# Crear interfaz del analizador léxico
def crear_interfaz_analizador_lexico():
    global root
    root = tk.Tk()
    root.title("Analizador Léxico de Java")
    root.configure(background='lightblue')

    font = ("Helvetica", 12, "bold")
    font2 = ("Helvetica", 12)

    frame = tk.Frame(root, bg='lightblue')
    frame.pack(pady=10)

    global text_area
    text_area = scrolledtext.ScrolledText(frame, width=60, height=15, bg='white', fg='black', font=font2)
    text_area.pack()

    btn_frame = tk.Frame(root, bg='lightblue')
    btn_frame.pack(pady=5)

    def crear_boton(frame, text, command):
        return tk.Button(frame, text=text, command=command, bg='gray', fg='white', font=font, relief='flat', highlightbackground='gray', highlightthickness=0, bd=0, padx=10, pady=5)

    btn_cargar = crear_boton(btn_frame, "Cargar Archivo", cargar_archivo)
    btn_cargar.grid(row=0, column=0, padx=5)

    btn_analizar = crear_boton(btn_frame, "Analizar Código", analizar_codigo_lexico)
    btn_analizar.grid(row=0, column=1, padx=5)

    btn_limpiar = crear_boton(btn_frame, "Limpiar Salida", limpiar_salida)
    btn_limpiar.grid(row=0, column=2, padx=5)

    btn_regresar = crear_boton(btn_frame, "Regresar al Menú", lambda: regresar_menu_principal(root))
    btn_regresar.grid(row=0, column=3, padx=5)

    global resultado_area
    resultado_area = scrolledtext.ScrolledText(root, width=60, height=10, state=tk.DISABLED, bg='white', fg='black', font=font)
    resultado_area.pack(pady=10)

    root.mainloop()

# Crear interfaz del analizador sintáctico
def crear_interfaz_analizador_sintactico():
    global root
    root = tk.Tk()
    root.title("Analizador Sintáctico de Java")
    root.configure(background='lightblue')

    font = ("Helvetica", 12, "bold")
    font2 = ("Helvetica", 12)

    frame = tk.Frame(root, bg='lightblue')
    frame.pack(pady=10)

    global text_area
    text_area = scrolledtext.ScrolledText(frame, width=60, height=15, bg='white', fg='black', font=font2)
    text_area.pack()

    btn_frame = tk.Frame(root, bg='lightblue')
    btn_frame.pack(pady=5)

    def crear_boton(frame, text, command):
        return tk.Button(frame, text=text, command=command, bg='gray', fg='white', font=font, relief='flat', highlightbackground='gray', highlightthickness=0, bd=0, padx=10, pady=5)

    btn_cargar = crear_boton(btn_frame, "Cargar Archivo", cargar_archivo)
    btn_cargar.grid(row=0, column=0, padx=5)

    btn_analizar = crear_boton(btn_frame, "Analizar Código", analizar_codigo_sintactico)
    btn_analizar.grid(row=0, column=1, padx=5)

    btn_limpiar = crear_boton(btn_frame, "Limpiar Salida", limpiar_salida)
    btn_limpiar.grid(row=0, column=2, padx=5)

    btn_regresar = crear_boton(btn_frame, "Regresar al Menú", lambda: regresar_menu_principal(root))
    btn_regresar.grid(row=0, column=3, padx=5)

    global resultado_area
    resultado_area = scrolledtext.ScrolledText(root, width=60, height=10, state=tk.DISABLED, bg='white', fg='black', font=font)
    resultado_area.pack(pady=10)

    root.mainloop()

# Mostrar el menú principal al iniciar el programa
mostrar_menu_principal()