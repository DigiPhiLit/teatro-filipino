import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import time
from tei_generator import generate_tei_xml, save_tei_to_file


def update_status(msg):
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, msg)


def on_load_file():
    filename = filedialog.askopenfilename(
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if filename:
        try:
            with open(filename, "r", encoding="utf-8") as f:
                contenido = f.read()
            input_text.delete("1.0", tk.END)
            input_text.insert(tk.END, contenido)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo: {e}")


def on_generate():
    texto = input_text.get("1.0", tk.END).strip()
    if not texto:
        messagebox.showwarning("Aviso", "Introduce algún texto.")
        return

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, "Generando TEI... por favor espera.")

    hilo = threading.Thread(target=generate_in_background, args=(texto,))
    hilo.start()


def generate_in_background(texto):
    max_reintentos = 3
    intento = 0
    
    while intento < max_reintentos:
        try:
            print(f"Generando TEI... (intento {intento + 1})")
            tei_xml = generate_tei_xml(texto)
            print("Generación terminada")
            output_text.after(0, lambda result=tei_xml: mostrar_resultado(result))
            return
        
        except Exception as e:
            error_msg = str(e)
            print(f"ERROR: {error_msg}")
            
            # Si es error 429 (quota), esperar e reintentar
            if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                intento += 1
                if intento < max_reintentos:
                    msg = f"Cuota excedida. Reintentando en 40s... (intento {intento}/{max_reintentos})"
                    print(msg)
                    output_text.after(0, lambda text=msg: update_status(text))
                    time.sleep(40)
                else:
                    msg = f"API excedió cuota después de {max_reintentos} intentos.\n\nIntenta de nuevo en unos minutos."
                    output_text.after(0, lambda text=msg: messagebox.showerror("Error de Cuota", text))
                    return
            else:
                # Otro tipo de error, no reintentar
                output_text.after(0, lambda text=error_msg: messagebox.showerror("Error", f"Error generando TEI:\n\n{text}"))
                return


def mostrar_resultado(tei_xml):
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, tei_xml if tei_xml else "No se generó contenido.")


def on_save():
    tei_xml = output_text.get("1.0", tk.END).strip()
    if not tei_xml:
        messagebox.showwarning("Aviso", "No hay XML para guardar.")
        return

    filename = filedialog.asksaveasfilename(
        defaultextension=".xml",
        filetypes=[("XML files", "*.xml"), ("All files", "*.*")]
    )
    if filename:
        save_tei_to_file(tei_xml, filename)
        messagebox.showinfo("Éxito", f"Guardado en:\n{filename}")


# ---------------- INTERFAZ ----------------

root = tk.Tk()
root.title("Generador TEI con Gemma")

root.configure(bg="#f2f2f2")
root.option_add("*Font", ("Arial", 10))

# ----- Texto de entrada -----
input_label = tk.Label(root, text="Texto de entrada:", bg="#f2f2f2", font=("Segoe UI", 11, "bold"))
input_label.pack(anchor="w", padx=10, pady=(10, 0))

input_text = tk.Text(root, height=15, width=80, relief="solid", borderwidth=1)
input_text.pack(padx=10, pady=5)

# ----- BOTONES -----
button_frame = tk.Frame(root, bg="#f2f2f2")
button_frame.pack(pady=10)

load_button = tk.Button(button_frame, text="Cargar archivo .txt", command=on_load_file, width=18)
load_button.pack(side="left", padx=5)

generate_button = tk.Button(button_frame, text="Generar TEI", command=on_generate, width=18)
generate_button.pack(side="left", padx=5)

save_button = tk.Button(button_frame, text="Guardar XML", command=on_save, width=18)
save_button.pack(side="left", padx=5)

# ----- XML generado -----
output_label = tk.Label(root, text="XML TEI generado:", bg="#f2f2f2", font=("Segoe UI", 11, "bold"))
output_label.pack(anchor="w", padx=10, pady=(10, 0))

output_text = tk.Text(root, height=15, width=80, relief="solid", borderwidth=1)
output_text.pack(padx=10, pady=5)

root.mainloop()
