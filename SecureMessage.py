import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet

# Clave de cifrado compartida (asegúrate de mantener esta clave segura y privada)
key = b'VbvCKhovxpPeXhII2M43hhzLPWJByi5K4aQFjRzXPsg='
cipher_suite = Fernet(key)

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
        messagebox.showinfo("Copiado", "El resultado ha sido copiado al portapapeles.")
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

# Etiqueta y caja de texto para el mensaje (editable)
label_message = tk.Label(root, text="Mensaje:")
label_message.grid(row=0, column=0, padx=10, pady=10)

entry_message = tk.Text(root, height=5, width=50)
entry_message.grid(row=0, column=1, padx=10, pady=10)

# Etiqueta y caja de texto para el resultado (no editable)
label_result = tk.Label(root, text="Resultado:")
label_result.grid(row=2, column=0, padx=10, pady=10)

entry_result = tk.Text(root, height=5, width=50)
entry_result.grid(row=2, column=1, padx=10, pady=10)
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

# Ejecutar la interfaz gráfica
root.mainloop()
