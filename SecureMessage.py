import tkinter as tk
from tkinter import messagebox,simpledialog
from cryptography.fernet import Fernet
import firebase_admin
from firebase_admin import credentials, db
import time
import threading
import firebase_manager as fb
import datetime
import os
from PIL import Image, ImageTk


# Inicializa Firebase al arrancar
fb.initialize_firebase()

# Variable global para almacenar la clave de encriptación
cipher_suite = None

# Función para mostrar solo los últimos 4 caracteres de la clave
def update_key_display(new_key):
    entry_key.config(state=tk.NORMAL)
    entry_key.delete(1.0, tk.END)
    partial_key = "*************" + new_key[-8:]  # Mostrar solo los últimos 4 caracteres
    entry_key.insert(tk.END, partial_key)
    entry_key.config(state=tk.DISABLED)


# Función para generar una nueva clave manualmente y actualizar el campo
def manual_generate_key():
    if verify_password():
        new_key = Fernet.generate_key().decode()
        current_time = datetime.datetime.now().isoformat()  # Guardar la fecha y hora actuales
        fb.store_encryption_key(new_key,current_time)  # Guardar la nueva clave usando firebase_manager

# Función para escuchar cambios en la clave de encriptación en Firebase
def key_listener(event):
    global cipher_suite
    new_key = event.data  # Obtener la nueva clave
    if new_key:
        print(f"New key received: {new_key}")
        # Actualizar el cifrador con la nueva clave
        cipher_suite = Fernet(new_key.encode())
        update_key_display(new_key)

# Función para configurar el listener para cambios en la clave
def setup_key_listener():
    ref = db.reference('encryption_key/key')  # Referencia al nodo 'key'
    ref.listen(key_listener)


def get_encryption_key():
    try:
        ref = db.reference('encryption_key')
        key_data = ref.get()
        if key_data is not None:
            key_str = key_data['key']
            return key_str.encode('utf-8')
        else:
            messagebox.showerror("Error", "No se pudo obtener la clave de encriptación.")
    except Exception as e:
        messagebox.showerror("Error", f"Hubo un error al conectarse a Firebase: {str(e)}")
        return None

# Función para encriptar el mensaje
def encrypt_message():
    message = entry_message.get("1.0", tk.END).strip()
    if message:
        encrypted_message = cipher_suite.encrypt(message.encode())
        entry_result.config(state=tk.NORMAL)
        entry_result.delete(1.0, tk.END)
        entry_result.insert(tk.END, encrypted_message.decode())
        entry_result.config(state=tk.DISABLED)
    else:
        messagebox.showwarning("Error", "Por favor ingresa un mensaje.")

# Función para desencriptar el mensaje
def decrypt_message():
    encrypted_message = entry_message.get("1.0", tk.END).strip()
    if encrypted_message:
        try:
            decrypted_message = cipher_suite.decrypt(encrypted_message.encode()).decode()
            entry_result.config(state=tk.NORMAL)
            entry_result.delete(1.0, tk.END)
            entry_result.insert(tk.END, decrypted_message)
            entry_result.config(state=tk.DISABLED)
        except Exception:
            messagebox.showerror("Error", "No se pudo desencriptar el mensaje. Asegúrate de que esté correcto.")
    else:
        messagebox.showwarning("Error", "Por favor ingresa un mensaje.")

# Función para copiar el resultado al portapapeles
def copy_to_clipboard():
    result_text = entry_result.get("1.0", tk.END).strip()
    if result_text:
        root.clipboard_clear()
        root.clipboard_append(result_text)    
    else:
        messagebox.showwarning("Error", "No hay resultado para copiar.")

# Función para borrar el texto en ambas cajas
def clear_text():
    entry_message.delete(1.0, tk.END)
    entry_result.config(state=tk.NORMAL)
    entry_result.delete(1.0, tk.END)
    entry_result.config(state=tk.DISABLED)

# Funciones para los comandos del menú
def administraon():
    if verify_password():
        new_password = simpledialog.askstring("Nueva Contraseña", "Introduce la nueva contraseña:", show="*")
        if new_password:
            fb.update_password(new_password)  # Actualizar la contraseña usando firebase_manager
        else:           
            messagebox.showinfo("Error Nueva contraseña", "No se ha introducido una nueva contraseña.")
    else:
        messagebox.showerror("Error", "Contraseña incorrecta. No se generó la nueva contraseña.")

def verify_password():
    input_password = simpledialog.askstring("Contraseña", "Introduce la contraseña:", show="*")
    
    if input_password:  # Si se ha introducido una contraseña
        stored_password = fb.get_stored_password()  # Obtener la contraseña almacenada desde Firebase
        if stored_password == input_password:
            return True  # La contraseña es correcta
        else:
            messagebox.showerror("Error", "Contraseña incorrecta.")
            return False  # Contraseña incorrecta
    else:
        messagebox.showwarning("Advertencia", "No se ha introducido ninguna contraseña.")
        return None  # No se ha introducido contraseña


def show_key_info():   
    if verify_password():
        # Obtener la clave y la fecha de creación desde Firebase
        key_data = fb.get_encryption_key_data()  # Suponiendo que 'get_encryption_key_data' devuelve tanto la clave como la fecha
        if key_data:
            key = key_data.get('key')
            created_at_str = key_data.get('created_at')

            if created_at_str:
                # Convertir la fecha de creación a un objeto datetime
                created_at = datetime.datetime.fromisoformat(created_at_str)
                # Calcular la duración que la clave ha estado en uso
                now = datetime.datetime.now()
                duration = now - created_at

                # Formatear la duración de manera más bonita
                days = duration.days
                hours, remainder = divmod(duration.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                formatted_duration = f"{days} días, {hours} horas, {minutes} minutos, {seconds} segundos"

                # Crear una ventana nueva para mostrar la información
                key_info_window = tk.Toplevel(root)
                key_info_window.title("Información de la Clave")

                # Mostrar la clave completa
                label_key = tk.Label(key_info_window, text=f"{key}")
                label_key.pack(padx=10, pady=10)

                # Botón pequeño para copiar la clave al portapapeles
                def copy_key():
                    root.clipboard_clear()
                    root.clipboard_append(key)

                btn_copy_key = tk.Button(key_info_window, text="Copiar clave", command=copy_key, width=10)
                btn_copy_key.pack(pady=5)

                # Mostrar la duración de la clave en un formato bonito
                label_duration = tk.Label(key_info_window, text=f"Duración: {formatted_duration}")
                label_duration.pack(padx=10, pady=10)

                # Botón para cerrar la ventana
                btn_close = tk.Button(key_info_window, text="Cerrar", command=key_info_window.destroy)
                btn_close.pack(padx=10, pady=10)
            else:
                messagebox.showerror("Error", "No se encontró la fecha de creación de la clave.")
        else:
            messagebox.showerror("Error", "No se pudo obtener la información de la clave.")

def import_key():
    # Crear un cuadro de diálogo (ventana emergente) para pegar la clave
    import_window = tk.Toplevel(root)
    import_window.title("Importar Clave")

    # Etiqueta para el cuadro de texto
    label_import = tk.Label(import_window, text="Pega la clave aquí:")
    label_import.pack(padx=10, pady=10)

    # Cuadro de texto donde el usuario pegará la clave
    entry_import_key = tk.Text(import_window, height=2, width=50)
    entry_import_key.pack(padx=10, pady=10)

    # Definir la función apply_key para validar y aplicar la clave
    def apply_key():
        new_key = entry_import_key.get("1.0", tk.END).strip()

        # Validar que la clave importada sea válida (tiene que ser 32 bytes para Fernet en base64)
        if len(new_key) == 44:  # Clave Fernet tiene que ser una cadena base64 de 44 caracteres
            global cipher_suite
            cipher_suite = Fernet(new_key.encode())  # Actualizar la clave usada por el programa
            update_key_display(new_key)  # Mostrar la clave en el cuadro de texto principal
            messagebox.showinfo("Clave Importada", "La clave se ha importado correctamente.")
            import_window.destroy()  # Cerrar el cuadro de diálogo
        else:
            messagebox.showerror("Error", "La clave que has introducido no es válida. Asegúrate de pegar una clave correcta.")

    # Botón para aplicar la clave
    btn_apply_key = tk.Button(import_window, text="Aplicar clave", command=apply_key)
    btn_apply_key.pack(pady=5)

    # Botón para cerrar el cuadro de diálogo
    btn_cancel = tk.Button(import_window, text="Cancelar", command=import_window.destroy)
    btn_cancel.pack(pady=5)

def use_stored_key():
    # Aplicar la clave de encriptación
    global cipher_suite
    key = get_encryption_key()
    cipher_suite = Fernet(key)
    update_key_display(key.decode('utf-8'))



###### Configuración de la interfaz ######


# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Encriptador de Mensajes")

root.grid_columnconfigure(1, weight=1)

# Obtener la ruta absoluta del archivo
logo_path = os.path.abspath("logo.png")
# Cargar el icono usando Pillow
logo_image = Image.open(logo_path)  # Asegúrate de que la ruta sea correcta
logo_image = ImageTk.PhotoImage(logo_image)
# Cambiar el logo de la ventana
root.iconphoto(False, logo_image)
# Cambiar el logo de la ventana
root.iconphoto(False, logo_image)

# Etiqueta y caja de texto para el mensaje (editable)
label_message = tk.Label(root, text="Mensaje:")
label_message.grid(row=0, column=0, padx=10, pady=10, sticky="w")

entry_message = tk.Text(root, height=5, width=50, wrap="word")
entry_message.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

# Etiqueta y caja de texto para el resultado (no editable)
label_result = tk.Label(root, text="Resultado:")
label_result.grid(row=2, column=0, padx=10, pady=10, sticky="w")

entry_result = tk.Text(root, height=5, width=50,wrap="word")
entry_result.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
entry_result.config(state=tk.DISABLED)

# Frame para centrar los botones de encriptar y desencriptar
button_frame = tk.Frame(root)
button_frame.grid(row=1, column=0, columnspan=2)

btn_encrypt = tk.Button(button_frame, text="Encriptar", command=encrypt_message)
btn_encrypt.grid(row=0, column=0, padx=10, pady=10)

btn_decrypt = tk.Button(button_frame, text="Desencriptar", command=decrypt_message)
btn_decrypt.grid(row=0, column=1, padx=10, pady=10)

# Botones para copiar y borrar, centrados debajo del segundo campo de texto
btn_copy = tk.Button(root, text="Copiar", command=copy_to_clipboard)
btn_copy.grid(row=3, column=0, columnspan=2, padx=10, pady=10, ipadx=50)

btn_clear = tk.Button(root, text="Borrar", command=clear_text)
btn_clear.grid(row=4, column=0, columnspan=2, padx=10, pady=10, ipadx=50)

# Añadir debajo de copiar y borrar un campo para mostrar la key actual y un botón para generar una nueva
label_key = tk.Label(root, text="Clave actual:")
label_key.grid(row=5, column=0, padx=10, pady=10)

entry_key = tk.Text(root, height=1, width=50)
entry_key.grid(row=5, column=1, padx=10, pady=10)
entry_key.config(state=tk.DISABLED)

# Botón para generar una nueva key manualmente
btn_generate_key = tk.Button(root, text="Generar nueva key", command=manual_generate_key)
btn_generate_key.grid(row=6, column=0, columnspan=2, padx=10, pady=10, ipadx=50)

# Crear la barra de menú
menu_bar = tk.Menu(root)

# Crear el menú 'Archivo' y añadirlo a la barra de menús
file_menu = tk.Menu(menu_bar, tearoff=0) 
file_menu.add_command(label="Cambiar contraseña", command=administraon)
file_menu.add_command(label="Key info", command=show_key_info)
file_menu.add_command(label="Importar key", command=import_key)
file_menu.add_command(label="Usar clave mas reciente", command=use_stored_key)
menu_bar.add_cascade(label="Archivo", menu=file_menu)


# Configurar la barra de menú en la ventana principal
root.config(menu=menu_bar)


# Iniciar el listener en segundo plano
threading.Thread(target=setup_key_listener, daemon=True).start()

# Aplicar la clave de encriptación
key = get_encryption_key()
cipher_suite = Fernet(key)
update_key_display(key.decode('utf-8'))

root.mainloop()