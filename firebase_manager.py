import firebase_admin
from firebase_admin import credentials, db
from tkinter import messagebox

# Inicializa Firebase con las credenciales proporcionadas
def initialize_firebase():
    try:
        cred = credentials.Certificate("./FireBaseConection.json")
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://message-4383b-default-rtdb.europe-west1.firebasedatabase.app/'
        })
    except Exception as e:
        messagebox.showerror("Error", f"Error al inicializar BBDD: {str(e)}")

# Función para obtener la clave de encriptación desde Firebase
def get_encryption_key():
    try:
        ref = db.reference('encryption_key')
        key_data = ref.get()
        if key_data is not None and 'key' in key_data:
            return key_data['key']
        else:
            messagebox.showerror("Error", "No se pudo obtener la clave de encriptación")
            return None
    except Exception as e:
        messagebox.showerror("Error", f"Hubo un problema al obtener la clave: {str(e)}")
        return None

# Función para guardar una nueva clave de encriptación en Firebase
def store_encryption_key(new_key, current_time):
    try:
        ref = db.reference('encryption_key')
        ref.set({
            'key': new_key,
            'created_at': current_time  # Guardar la clave y la fecha de creación
        })
        messagebox.showinfo("Clave actualizada", "Se ha generado una nueva Key")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar la nueva key: {str(e)}")

# Función para obtener la contraseña almacenada en Firebase
def get_stored_password():
    try:
        ref = db.reference('encryption_data/password')
        password = ref.get()
        if password:
            return password
        else:
            messagebox.showerror("Error", "No se encontró ninguna contraseña almacenada.")
            return None
    except Exception as e:
        messagebox.showerror("Error", f"Hubo un error al obtener la contraseña: {str(e)}")
        return None

# Función para actualizar la contraseña en Firebase
def update_password(new_password):
    try:
        ref = db.reference('encryption_data')
        ref.update({'password': new_password})
        messagebox.showinfo("Contraseña actualizada", "La nueva contraseña se ha guardado correctamente")
    except Exception as e:
        messagebox.showerror("Error", f"Hubo un error al guardar la nueva contraseña: {str(e)}")

def get_encryption_key_data():
    try:
        ref = db.reference('encryption_key')
        key_data = ref.get()
        if key_data:
            return key_data  # Devolver la clave y la fecha de creación
        else:
            messagebox.showerror("Error", "No se encontró ninguna clave almacenada.")
            return None
    except Exception as e:
        messagebox.showerror("Error", f"Hubo un problema al obtener la información de la clave: {str(e)}")
        return None
