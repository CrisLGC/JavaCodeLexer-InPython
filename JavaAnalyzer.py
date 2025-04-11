# Cristian Guevara 31.567.525
import tkinter as tk
from tkinter import filedialog, scrolledtext
import re
from tkinter import Canvas
import subprocess  # Importar módulo para ejecutar comandos del sistema

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
    
    btn_compilador = tk.Button(menu_principal, text="Compilador", command=lambda: iniciar_compilador(menu_principal), bg='gray', fg='white', font=font, relief='flat', highlightbackground='gray', highlightthickness=0, bd=0, padx=10, pady=5)
    btn_compilador.pack(pady=10)
    
    menu_principal.mainloop()

def iniciar_analizador_lexico(menu_principal):
    menu_principal.destroy()
    crear_interfaz_analizador_lexico()

def iniciar_analizador_sintactico(menu_principal):
    menu_principal.destroy()
    crear_interfaz_analizador_sintactico()

def iniciar_compilador(menu_principal):
    menu_principal.destroy()
    crear_interfaz_compilador()

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

def generar_arbol_sintactico(codigo):
    """
    Genera una estructura jerárquica para representar el árbol sintáctico.
    """
    arbol = []
    lineas = codigo.split('\n')
    for linea in lineas:
        linea = linea.strip()
        if linea.startswith("class"):
            arbol.append(("Clase", linea.split()[1]))
        elif linea.startswith("public") or linea.startswith("private") or linea.startswith("protected"):
            if "class" not in linea:
                arbol.append(("Método", linea.split("(")[0].split()[-1]))
        elif "=" in linea and ";" in linea:
            arbol.append(("Asignación", linea.split("=")[0].strip()))
    return arbol

def mostrar_arbol_sintactico():
    """
    Muestra una nueva ventana con el árbol sintáctico generado dinámicamente.
    """
    # Obtener el código ingresado en el área de texto
    codigo = text_area.get("1.0", tk.END).strip()
    if not codigo:
        return

    # Generar el árbol sintáctico
    arbol = generar_arbol_sintactico(codigo)

    # Crear una nueva ventana para el árbol sintáctico
    ventana_arbol = tk.Toplevel(root)
    ventana_arbol.title("Árbol Sintáctico")
    ventana_arbol.configure(background='lightblue')

    # Crear un canvas para dibujar el árbol
    canvas = Canvas(ventana_arbol, width=800, height=600, bg='white')
    canvas.pack()

    # Dibujar el árbol sintáctico
    x, y = 400, 50  # Coordenadas iniciales
    nivel = 1
    for nodo in arbol:
        tipo, nombre = nodo
        canvas.create_text(x, y, text=f"{tipo}: {nombre}", font=("Helvetica", 12, "bold"))
        if nivel > 1:
            canvas.create_line(x, y - 30, x, y - 10)  # Línea hacia el nodo padre
        y += 50
        nivel += 1

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

    btn_arbol = crear_boton(btn_frame, "Mostrar Árbol", mostrar_arbol_sintactico)
    btn_arbol.grid(row=0, column=3, padx=5)

    btn_regresar = crear_boton(btn_frame, "Regresar al Menú", lambda: regresar_menu_principal(root))
    btn_regresar.grid(row=0, column=4, padx=5)

    global resultado_area
    resultado_area = scrolledtext.ScrolledText(root, width=60, height=10, state=tk.DISABLED, bg='white', fg='black', font=font)
    resultado_area.pack(pady=10)

    root.mainloop()

# Análisis semántico
def analizar_semantico(codigo):
    errores = []
    simbolos = {}
    lineas = codigo.split('\n')

    for i, linea in enumerate(lineas):
        linea = linea.strip()
        # Detectar declaraciones de variables (con o sin inicialización)
        match = re.match(r'\b(int|double|float|String|boolean|char)\b\s+(\w+)\s*(=\s*[^;]+)?;', linea)
        if match:
            tipo = match.group(1)  # Tipo de la variable
            nombre = match.group(2)  # Nombre de la variable
            if nombre in simbolos:
                errores.append((i + 1, f"Variable '{nombre}' ya declarada"))
            else:
                simbolos[nombre] = tipo
        # Detectar uso de variables no declaradas
        elif re.match(r'\w+\s*=', linea):
            nombre = linea.split('=')[0].strip()
            if nombre not in simbolos:
                errores.append((i + 1, f"Variable '{nombre}' no declarada"))

    return errores, simbolos

# Generación de código intermedio
def generar_codigo_intermedio(codigo):
    """
    Versión mejorada de generación de código intermedio con:
    - Manejo de temporales
    - Mejor estructura de control
    - Soporte para más construcciones Java
    """
    lineas = [line.strip() for line in codigo.split('\n') if line.strip()]
    codigo_intermedio = []
    temp_counter = 1
    label_counter = 1
    current_block = None
    
    for linea in lineas:
        # Ignorar comentarios y líneas vacías
        if linea.startswith("//") or linea.startswith("/*") or not linea:
            continue
            
        # Manejar declaraciones de variables
        match_var = re.match(r'(int|double|float|boolean|String)\s+(\w+)\s*(?:=\s*(.*?))?;', linea)
        if match_var:
            var_type, var_name, init_value = match_var.groups()
            if init_value:
                temp_var = f"t{temp_counter}"
                temp_counter += 1
                codigo_intermedio.append(f"{temp_var} = {init_value}")
                codigo_intermedio.append(f"{var_name} = {temp_var}")
            else:
                codigo_intermedio.append(f"DECLARE {var_name} AS {var_type}")
            continue
            
        # Manejar asignaciones
        match_assign = re.match(r'(\w+)\s*=\s*(.*?);', linea)
        if match_assign:
            var_name, expr = match_assign.groups()
            if any(op in expr for op in '+-*/%'):
                temp_var = f"t{temp_counter}"
                temp_counter += 1
                codigo_intermedio.append(f"{temp_var} = {expr}")
                codigo_intermedio.append(f"{var_name} = {temp_var}")
            else:
                codigo_intermedio.append(f"{var_name} = {expr}")
            continue
            
        # Manejar if
        match_if = re.match(r'if\s*\((.*?)\)\s*\{?', linea)
        if match_if:
            condition = match_if.group(1)
            end_label = f"L{label_counter}"
            label_counter += 1
            codigo_intermedio.append(f"IF NOT ({condition}) GOTO {end_label}")
            current_block = ("if", end_label)
            continue
            
        # Manejar while
        match_while = re.match(r'while\s*\((.*?)\)\s*\{?', linea)
        if match_while:
            condition = match_while.group(1)
            start_label = f"L{label_counter}"
            end_label = f"L{label_counter+1}"
            label_counter += 2
            codigo_intermedio.append(f"{start_label}:")
            codigo_intermedio.append(f"IF NOT ({condition}) GOTO {end_label}")
            current_block = ("while", start_label, end_label)
            continue
            
        # Manejar cierre de bloques
        if linea == '}' or linea == '};':
            if current_block:
                block_type = current_block[0]
                if block_type == "while":
                    start_label, end_label = current_block[1], current_block[2]
                    codigo_intermedio.append(f"GOTO {start_label}")
                    codigo_intermedio.append(f"{end_label}:")
                elif block_type == "if":
                    end_label = current_block[1]
                    codigo_intermedio.append(f"{end_label}:")
                current_block = None
            continue
            
        # Manejar System.out.println
        if "System.out.println" in linea:
            match_print = re.match(r'System\.out\.println\((.*?)\);', linea)
            if match_print:
                param = match_print.group(1)
                codigo_intermedio.append(f"PRINT {param}")
            continue
            
    return codigo_intermedio

# Optimización de código
def optimizar_codigo(codigo_intermedio):
    codigo_optimizado = []
    for instruccion in codigo_intermedio:
        if "ASSIGN" in instruccion:
            # Evitar eliminar asignaciones necesarias
            codigo_optimizado.append(instruccion)
        else:
            codigo_optimizado.append(instruccion)
    return codigo_optimizado

# Generación de código final
def generar_codigo_final(codigo_intermedio):
    """
    Genera código final (pseudocódigo de ensamblador) a partir del código intermedio.
    Versión mejorada con:
    - Uso de registros virtuales
    - Optimización de asignaciones
    - Mejor manejo de estructuras de control
    """
    codigo_final = []
    registros = ['R1', 'R2', 'R3']  # Registros disponibles
    registro_actual = 0
    etiquetas = {}
    
    # Primera pasada: identificar todas las etiquetas
    for i, instruccion in enumerate(codigo_intermedio):
        if ':' in instruccion and not instruccion.startswith('IF'):
            etiqueta = instruccion.replace(':', '')
            etiquetas[etiqueta] = f"ETIQUETA_{len(etiquetas)+1}"
    
    # Segunda pasada: generar código
    for instruccion in codigo_intermedio:
        # Asignaciones básicas
        if ' = ' in instruccion:
            partes = instruccion.split(' = ')
            destino = partes[0].strip()
            origen = partes[1].strip()
            
            # Optimización: si es asignación directa de constante
            if origen.isdigit():
                codigo_final.append(f"MOV {destino}, #{origen}")
            # Asignación entre variables
            else:
                reg = registros[registro_actual]
                registro_actual = (registro_actual + 1) % len(registros)
                codigo_final.append(f"MOV {reg}, {origen}")
                codigo_final.append(f"MOV {destino}, {reg}")
        
        # Estructuras IF GOTO
        elif instruccion.startswith('IF'):
            # Extraer condición y etiqueta
            cond_parts = instruccion.split('GOTO')
            cond = cond_parts[0].replace('IF NOT', '').strip()[1:-1]  # Quitar paréntesis
            etiqueta = cond_parts[1].strip()
            
            # Convertir condición a operación de ensamblador
            if '>' in cond:
                var, val = cond.split('>')
                codigo_final.append(f"CMP {var.strip()}, #{val.strip()}")
                codigo_final.append(f"JLE {etiquetas.get(etiqueta, etiqueta)}")
            elif '<' in cond:
                var, val = cond.split('<')
                codigo_final.append(f"CMP {var.strip()}, #{val.strip()}")
                codigo_final.append(f"JGE {etiquetas.get(etiqueta, etiqueta)}")
            # Puedes añadir más operadores aquí
        
        # Etiquetas
        elif ':' in instruccion:
            etiqueta = instruccion.replace(':', '')
            codigo_final.append(f"{etiquetas.get(etiqueta, etiqueta)}:")
        
        # Llamadas a PRINT
        elif instruccion.startswith('PRINT'):
            var = instruccion.split()[1]
            codigo_final.append(f"MOV R0, {var}")  # Registro para parámetros
            codigo_final.append("SVC #PrintInt")    # Llamada al sistema
    
    # Añadir encabezado y pie de código
    codigo_completo = ["; Código generado automáticamente", ".data"]
    
    # Declarar variables (esto requeriría análisis previo)
    variables = set()
    for instr in codigo_intermedio:
        if ' = ' in instr:
            var = instr.split(' = ')[0].strip()
            if var.startswith('t'):  # Temporales
                variables.add(f"{var}: .word 0")
            else:  # Variables del usuario
                variables.add(f"{var}: .word 0")
    
    codigo_completo.extend(variables)
    codigo_completo.extend([".code", "MAIN:"])
    codigo_completo.extend(codigo_final)
    codigo_completo.append("SVC #Exit")  # Terminar programa
    
    return codigo_completo

# Mostrar resultados del análisis semántico
def mostrar_resultados_semantico(errores, simbolos):
    resultado_area.config(state=tk.NORMAL)
    resultado_area.delete("1.0", tk.END)

    resultado_area.insert(tk.END, "Tabla de Errores Semánticos:\n")
    resultado_area.insert(tk.END, f"{'Línea':<10}{'Descripción':<50}\n")
    resultado_area.insert(tk.END, "-"*60 + "\n")
    for linea, descripcion in errores:
        resultado_area.insert(tk.END, f"{linea:<10}{descripcion:<50}\n")

    resultado_area.insert(tk.END, "\nTabla de Símbolos:\n")
    resultado_area.insert(tk.END, f"{'Nombre':<20}{'Tipo':<20}\n")
    resultado_area.insert(tk.END, "-"*40 + "\n")
    for nombre, tipo in simbolos.items():
        resultado_area.insert(tk.END, f"{nombre:<20}{tipo:<20}\n")

    resultado_area.config(state=tk.DISABLED)

# Nueva interfaz para análisis semántico y generación de código
def crear_interfaz_compilador():
    global root
    root = tk.Tk()
    root.title("Compilador de Java")
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

    btn_semantico = crear_boton(btn_frame, "Análisis Semántico", analizar_codigo_semantico)
    btn_semantico.grid(row=0, column=1, padx=5)

    btn_intermedio = crear_boton(btn_frame, "Generar Código Intermedio", generar_codigo_intermedio_ui)
    btn_intermedio.grid(row=0, column=2, padx=5)

    btn_final = crear_boton(btn_frame, "Generar Código Final", generar_codigo_final_ui)
    btn_final.grid(row=0, column=3, padx=5)

    btn_ejecutar = crear_boton(btn_frame, "Ejecutar Código Java", ejecutar_codigo_java)
    btn_ejecutar.grid(row=0, column=4, padx=5)

    btn_regresar = crear_boton(btn_frame, "Regresar al Menú", lambda: regresar_menu_principal(root))
    btn_regresar.grid(row=0, column=5, padx=5)

    global resultado_area
    resultado_area = scrolledtext.ScrolledText(root, width=60, height=10, state=tk.DISABLED, bg='white', fg='black', font=font)
    resultado_area.pack(pady=10)

    root.mainloop()

# Funciones para la interfaz
def analizar_codigo_semantico():
    codigo = text_area.get("1.0", tk.END)
    errores, simbolos = analizar_semantico(codigo)
    mostrar_resultados_semantico(errores, simbolos)

def generar_codigo_intermedio_ui():
    """Función mejorada para generar y mostrar código intermedio desde la UI"""
    try:
        # Obtener código Java del área de texto
        codigo_java = text_area.get("1.0", tk.END).strip()
        
        if not codigo_java:
            mostrar_codigo(["No hay código Java para procesar"], "Advertencia")
            return
        
        # Generar código intermedio
        codigo_intermedio = generar_codigo_intermedio(codigo_java)
        
        # Optimizar código (opcional)
        codigo_optimizado = optimizar_codigo(codigo_intermedio)
        
        # Formatear salida para mejor visualización
        codigo_formateado = []
        codigo_formateado.append("=== CÓDIGO INTERMEDIO GENERADO ===")
        codigo_formateado.append("Instrucciones:")
        codigo_formateado.extend([f"{i+1:03d}: {line}" for i, line in enumerate(codigo_optimizado)])
        
        # Mostrar resultados
        mostrar_codigo(codigo_formateado, "Código Intermedio")
        
    except Exception as e:
        mostrar_codigo([f"Error al generar código intermedio: {str(e)}"], "Error")

def generar_codigo_final_ui():
    """
    Función para UI que genera y muestra el código final
    """
    try:
        # Obtener código Java del área de texto
        codigo_java = text_area.get("1.0", tk.END).strip()
        
        if not codigo_java:
            mostrar_codigo(["No hay código Java para procesar"], "Advertencia")
            return
        
        # Generar código intermedio
        codigo_intermedio = generar_codigo_intermedio(codigo_java)
        
        # Optimizar código intermedio
        codigo_optimizado = optimizar_codigo(codigo_intermedio)
        
        # Generar código final
        codigo_final = generar_codigo_final(codigo_optimizado)
        
        # Mostrar resultados
        mostrar_codigo(codigo_final, "Código Final Generado")
        
    except Exception as e:
        mostrar_codigo([f"Error al generar código final: {str(e)}"], "Error")

def mostrar_codigo(codigo, titulo):
    resultado_area.config(state=tk.NORMAL)
    resultado_area.delete("1.0", tk.END)
    resultado_area.insert(tk.END, f"{titulo}:\n")
    resultado_area.insert(tk.END, "-"*40 + "\n")
    for linea in codigo:
        resultado_area.insert(tk.END, linea + "\n")
    resultado_area.config(state=tk.DISABLED)

def ejecutar_codigo_java():
    """
    Compila y ejecuta el código Java ingresado en el área de texto.
    """
    # Obtener el código Java del área de texto
    codigo_java = text_area.get("1.0", tk.END).strip()
    if not codigo_java:
        mostrar_codigo(["No hay código Java para ejecutar"], "Advertencia")
        return

    # Guardar el código en un archivo temporal
    archivo_java = "TempJavaFile.java"
    with open(archivo_java, "w") as archivo:
        archivo.write(codigo_java)

    try:
        # Compilar el archivo Java
        resultado_compilacion = subprocess.run(
            ["javac", archivo_java],
            capture_output=True,
            text=True
        )

        if resultado_compilacion.returncode != 0:
            # Mostrar errores de compilación
            mostrar_codigo(
                ["Errores de compilación:"] + resultado_compilacion.stderr.splitlines(),
                "Errores de Compilación"
            )
            return

        # Ejecutar el archivo compilado
        resultado_ejecucion = subprocess.run(
            ["java", archivo_java.replace(".java", "")],
            capture_output=True,
            text=True
        )

        if resultado_ejecucion.returncode == 0:
            # Mostrar la salida del programa
            mostrar_codigo(
                ["Salida del programa:"] + resultado_ejecucion.stdout.splitlines(),
                "Salida del Programa"
            )
        else:
            # Mostrar errores de ejecución
            mostrar_codigo(
                ["Errores de ejecución:"] + resultado_ejecucion.stderr.splitlines(),
                "Errores de Ejecución"
            )

    except Exception as e:
        mostrar_codigo([f"Error al ejecutar el código Java: {str(e)}"], "Error")
    finally:
        # Limpiar el archivo temporal
        import os
        if os.path.exists(archivo_java):
            os.remove(archivo_java)
        if os.path.exists(archivo_java.replace(".java", ".class")):
            os.remove(archivo_java.replace(".java", ".class"))

# Mostrar el menú principal al iniciar el programa
mostrar_menu_principal()