import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet
import firebase_admin
from firebase_admin import credentials, db
import time
import threading


cred = credentials.Certificate("./FireBaseConection.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://message-4383b-default-rtdb.europe-west1.firebasedatabase.app/'
})

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
    new_key = Fernet.generate_key().decode()
    ref = db.reference('encryption_key')
    ref.set({'key': new_key})
    # update_key_display(new_key)
    messagebox.showinfo("Nueva Key", "Se ha generado una nueva clave de encriptación.")

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


# Función para obtener la clave de encriptación desde Firebase
def get_encryption_key():
    ref = db.reference('encryption_key')  # Referencia al nodo 'encryption_key'
    key_data = ref.get()  # Obtener los datos del nodo
    key_str = key_data['key']  # Obtener la cadena sin el prefijo b'
    # Convertir la cadena a bytes agregando el prefijo b''
    key_bytes = key_str.encode('utf-8')  # Convertir la cadena a bytes
    entry_key = key_bytes
    return key_bytes

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

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Encriptador de Mensajes")

root.grid_columnconfigure(1, weight=1)

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


# Iniciar el listener en segundo plano
threading.Thread(target=setup_key_listener, daemon=True).start()
# Aplicar la clave de encriptación
key = get_encryption_key()
cipher_suite = Fernet(key)
update_key_display(key.decode('utf-8'))

root.mainloop()