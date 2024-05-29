import customtkinter as ctk
from tkinter import messagebox
import random
from PIL import Image, ImageTk
import os
from customtkinter import CTkImage

# Configuración del tema y apariencia
ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("dark-blue") 

# Listas de personajes, armas y habitaciones con sus imágenes correspondientes
personajes = [
    {"name": "Señor Amapola", "image": "clue_imagenes/amapola.png"},
    {"name": "Profesora Mora", "image": "clue_imagenes/mora.jpg"},
    {"name": "Señora Blanco", "image": "clue_imagenes/blanco.jpg"},
    {"name": "Coronel Mostaza", "image": "clue_imagenes/mostaza.jpg"},
    {"name": "Doctor Verde", "image": "clue_imagenes/verde.jpg"},
    {"name": "Señorita Celeste", "image": "clue_imagenes/celeste.jpg"}
]

armas = [
    {"name": "Candelabro", "image": "clue_imagenes/candelabro.png"},
    {"name": "Cuchillo", "image": "clue_imagenes/cuchillo.jpg"},
    {"name": "Cuerda", "image": "clue_imagenes/cuerda.jpg"},
    {"name": "Llave Inglesa", "image": "clue_imagenes/llave_inglesa.jpg"},
    {"name": "Revolver", "image": "clue_imagenes/revolver.jpg"},
    {"name": "Tubo", "image": "clue_imagenes/tubo.jpg"}
]

habitaciones = [
    {"name": "Cocina", "image": "clue_imagenes/cocina.png"},
    {"name": "Comedor", "image": "clue_imagenes/comedor.jpg"},
    {"name": "Sala de Baile", "image": "clue_imagenes/sala_baile.jpg"},
    {"name": "Invernadero", "image": "clue_imagenes/invernadero.jpg"},
    {"name": "Biblioteca", "image": "clue_imagenes/biblioteca.jpg"},
    {"name": "Estudio", "image": "clue_imagenes/estudio.jpg"},
    {"name": "Sala", "image": "clue_imagenes/sala.jpg"},
    {"name": "Vestíbulo", "image": "clue_imagenes/vestibulo.jpg"},
    {"name": "Billar", "image": "clue_imagenes/billar.jpg"}
]

# Selección aleatoria de la solución
solucion_personaje = random.choice(personajes)
solucion_arma = random.choice(armas)
solucion_habitacion = random.choice(habitaciones)

# Variables globales para la IA
posibles_personajes = personajes[:]
posibles_armas = armas[:]
posibles_habitaciones = habitaciones[:]
intentos = 10  # Modificar el número de intentos según el nivel de dificultad

# Variables de control
personaje_var = None
arma_var = None
habitacion_var = None
intento_label = None
intentos_var = None
ia_resultado_label = None

def reiniciar_juego():
    global solucion_personaje, solucion_arma, solucion_habitacion
    global posibles_personajes, posibles_armas, posibles_habitaciones, intentos

    solucion_personaje = random.choice(personajes)
    solucion_arma = random.choice(armas)
    solucion_habitacion = random.choice(habitaciones)

    posibles_personajes = personajes[:]
    posibles_armas = armas[:]
    posibles_habitaciones = habitaciones[:]
    intentos = 10  # Modificar el número de intentos según el nivel de dificultad
    intento_label.configure(text="")
    ia_resultado_label.configure(text="")
    mostrar_mensaje("Reiniciar", "El juego ha sido reiniciado.")

def mostrar_mensaje(titulo, mensaje):
    intento_label.configure(text=f"{titulo}: {mensaje}")

def verificar_solucion():
    global intentos
    if intentos <= 0:
        mostrar_ventana("¡Perdiste!", "Te has quedado sin intentos. ¡Juego terminado!")
        return

    personaje = personaje_var.get()
    arma = arma_var.get()
    habitacion = habitacion_var.get()
    
    intentos -= 1
    intentos_var.set(intentos)

    if personaje == solucion_personaje["name"] and arma == solucion_arma["name"] and habitacion == solucion_habitacion["name"]:
        mostrar_ventana("¡Ganaste!", f"¡Has resuelto el misterio en {10 - intentos} intentos!")
            
    else:
        pistas = []
        if personaje != solucion_personaje["name"]:
            pistas.append(f"El personaje {personaje} no es correcto.")
        if arma != solucion_arma["name"]:
            pistas.append(f"El arma {arma} no es correcta.")
        if habitacion != solucion_habitacion["name"]:
            pistas.append(f"La habitación {habitacion} no es correcta.")
        mostrar_mensaje("Pistas", "\n".join(pistas))

def resolver_ia():
    global intentos
    if intentos <= 0:
        messagebox.showinfo("¡Perdiste!","Te has quedado sin intentos. ¡Juego terminado!")
        reiniciar_juego()
        return

    if posibles_personajes and posibles_armas and posibles_habitaciones:
        intentos -= 1
        
        # Buscar la combinación más probable
        personaje = posibles_personajes[0] if posibles_personajes else None
        arma = posibles_armas[0] if posibles_armas else None
        habitacion = posibles_habitaciones[0] if posibles_habitaciones else None

        ia_resultado_label.configure(text=f"Intento #{10 - intentos}: {personaje['name']} con el {arma['name']} en la {habitacion['name']}")

        if personaje == solucion_personaje and arma == solucion_arma and habitacion == solucion_habitacion:
            mostrar_ventana("¡Ganó IA!", f"La IA ha resuelto el misterio en {10 - intentos} intentos. Es más inteligente que tú.")
            reiniciar_juego()
        else:
            # Remover elementos incorrectos basados en el resultado
            if personaje != solucion_personaje:
                posibles_personajes.remove(personaje)
            if arma != solucion_arma:
                posibles_armas.remove(arma)
            if habitacion != solucion_habitacion:
                posibles_habitaciones.remove(habitacion)
            # Reintentar después de un pequeño retraso
            root.after(500, resolver_ia)  # Reducir el tiempo de espera a 500 ms para una resolución más rápida

def seleccionar_opcion(lista, variable, frame):
    def on_select(item):
        variable.set(item["name"])
        # Despintar todos los botones
        for button in buttons.values():
            button.configure(fg_color="transparent")
        # Pintar el botón seleccionado
        buttons[item["name"]].configure(fg_color="green")

    buttons = {}
    for widget in frame.winfo_children():
        widget.destroy()

    for item in lista:
        if os.path.exists(item["image"]):  # Verifica si la imagen existe
            img = Image.open(item["image"])
            img = img.resize((122, 122))
            img = ImageTk.PhotoImage(img)
            frame_image = ctk.CTkFrame(frame)
            frame_image.pack(side="left", padx=8, pady=8)
            boton = ctk.CTkButton(frame_image, image=img, compound="top", command=lambda i=item: on_select(i), width=100, height=100, anchor="center", font=("Arial", 14), text="")
            boton.image = img
            boton.pack()
            ctk.CTkLabel(frame_image, text=item["name"], font=("Arial", 15)).pack()
            buttons[item["name"]] = boton
        else:
            print(f"Archivo de imagen no encontrado: {item['image']}")

def generar_pistas_adicionales():
    pistas = []

    # Pistas relacionadas con los personajes
    pistas.append(f"El presunto asesino/a es un/a {generar_caracteristica_personaje(solucion_personaje['name'])}.")

    # Pistas relacionadas con las armas
    pistas.append(f"El arma tiene la siguiente caracteriztica: {generar_caracteristica_arma(solucion_arma['name'])}")

    # Pistas relacionadas con las habitaciones
    pistas.append(f"La habitacion tiene un acceso directo al {generar_acceso_directo(solucion_habitacion['name'])}.")

    return pistas

def generar_caracteristica_personaje(personaje):
    if personaje == "Señor Amapola":
        return "médico."
    elif personaje == "Profesora Mora":
        return "experta en armas."
    elif personaje == "Señora Blanco":
        return "ama de casa."
    elif personaje == "Coronel Mostaza":
        return "militar."
    elif personaje == "Doctor Verde":
        return "científico."
    elif personaje == "Señorita Celeste":
        return "actriz."

def generar_acceso_directo(habitacion):
    if habitacion == "Cocina":
        return "comedor"
    elif habitacion == "Comedor":
        return "cocina"
    elif habitacion == "Sala de Baile":
        return "vestíbulo"
    elif habitacion == "Invernadero":
        return "jardín"
    elif habitacion == "Biblioteca":
        return "estudio"
    elif habitacion == "Estudio":
        return "biblioteca"
    elif habitacion == "Sala":
        return "comedor"
    elif habitacion == "Vestíbulo":
        return "sala"
    elif habitacion == "Billar":
        return "sala"

def generar_caracteristica_arma(arma):
    if arma == "Candelabro":
        return "antiguo y pesado, utilizado en los salones más elegantes."
    elif arma == "Cuchillo":
        return "afilado y peligroso, comúnmente encontrado en la cocina."
    elif arma == "Cuerda":
        return "larga y resistente, a menudo utilizada en situaciones de emergencia."
    elif arma == "Llave Inglesa":
        return "metálica y contundente, típicamente encontrada en la caja de herramientas."
    elif arma == "Revolver":
        return "letal y preciso, una opción común entre los delincuentes."
    elif arma == "Tubo":
        return "largo y contundente, fácilmente disponible en cualquier hogar."

def mostrar_pistas_adicionales():
    pistas = generar_pistas_adicionales()
    
    # Crear una nueva ventana para mostrar las pistas
    pistas_window = ctk.CTkToplevel(root)
    pistas_window.title("Pistas adicionales")
    pistas_window.attributes("-topmost", True)  # Para que aparezca delante de la ventana principal
    
    # Crear un cuadro de texto para mostrar las pistas con texto grande
    text_widget = ctk.CTkTextbox(pistas_window, wrap="word", font=("Arial", 16))
    text_widget.pack(expand=True, fill="both", padx=20, pady=20)
    text_widget.insert("1.0", "\n".join(pistas))
    text_widget.configure(state="disabled")  # Hacer el texto de solo lectura
    
    ctk.CTkButton(pistas_window, text="Cerrar", command=pistas_window.destroy, font=("Arial", 16)).pack(pady=10)

def mostrar_ventana(titulo, mensaje):
    ventana = ctk.CTkToplevel(root)
    ventana.title(titulo)
    ventana.attributes("-topmost", True)  # Para que aparezca delante de la ventana principal

    global imagen  # Mantén una referencia global a la imagen

    # Agregar la imagen
    if titulo == "¡Ganaste!":
        imagen_path = "clue_imagenes/ganaste.gif"
    elif titulo == "¡Ganó IA!":
        imagen_path = "clue_imagenes/ia_gano.jpg"
    else:
        imagen_path = "clue_imagenes/perdiste.gif"
    
    if os.path.exists(imagen_path):
        imagen = Image.open(imagen_path)
        imagen = imagen.resize((1200, 800))
        imagen = ImageTk.PhotoImage(imagen)
        ctk.CTkLabel(ventana, image=imagen, text="").pack()
        ctk.CTkLabel(ventana, text=mensaje, font=("Arial", 16)).pack()
    else:
        ctk.CTkLabel(ventana, text="Imagen no encontrada", font=("Arial", 16)).pack()
    
    ventana.update()  # Actualiza la ventana después de agregar la imagen
    
    # Botón para regresar
    ctk.CTkButton(ventana, text="Regresar", command=ventana.destroy).pack()



def run_clue():
    global root, personaje_var, arma_var, habitacion_var, intentos_var, intento_label, ia_resultado_label

    root = ctk.CTk()
    root.title("Clue")

    # Variables de control
    personaje_var = ctk.StringVar(root)
    arma_var = ctk.StringVar(root)
    habitacion_var = ctk.StringVar(root)
    intentos_var = ctk.IntVar(value=10)  # Modificar el número de intentos según el nivel de dificultad

    # Crear frames para las opciones
    frame_personajes = ctk.CTkFrame(root)
    frame_armas = ctk.CTkFrame(root)
    frame_habitaciones = ctk.CTkFrame(root)
    frame_personajes.pack(pady=10)
    frame_armas.pack(pady=10)
    frame_habitaciones.pack(pady=10)

    # Crear widgets
    seleccionar_opcion(personajes, personaje_var, frame_personajes)
    seleccionar_opcion(armas, arma_var, frame_armas)
    seleccionar_opcion(habitaciones, habitacion_var, frame_habitaciones)

    frame_botones = ctk.CTkFrame(root)
    frame_botones.pack()

    # Crear y empaquetar los botones
    ctk.CTkButton(frame_botones, text="Verificar", command=verificar_solucion, font=("Arial", 18)).pack(side="left", padx=5)
    ctk.CTkButton(frame_botones, text="Resolver con IA", command=resolver_ia, font=("Arial", 18)).pack(side="left", padx=5)
    ctk.CTkButton(frame_botones, text="Mostrar pistas adicionales", command=mostrar_pistas_adicionales, font=("Arial", 18)).pack(side="left", padx=5)
    ctk.CTkButton(frame_botones, text="Rendirse", command=reiniciar_juego, font=("Arial", 18)).pack(side="left", padx=20, pady=5)  
    ctk.CTkButton(frame_botones, text="Salir", command=root.quit, font=("Arial", 18)).pack(side="left", padx=5)

    ctk.CTkLabel(root, text="Intentos restantes:", font=("Arial", 20, "bold")).pack(pady=5)
    ctk.CTkLabel(root, textvariable=intentos_var, font=("Arial", 20, "bold")).pack(pady=5)

    intento_label = ctk.CTkLabel(root, text="", font=("Arial", 20, "bold"))
    intento_label.pack(pady=10)

    ia_resultado_label = ctk.CTkLabel(root, text="", wraplength=400, font=("Arial", 20, "bold"))
    ia_resultado_label.pack(pady=10)

    # Ejecutar el bucle principal de la aplicación
    root.mainloop()

if __name__ == "__main__":
    run_clue()

