import tkinter as tk
from tkinter import ttk, messagebox
import math

class DownForceCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Down Force Prediction Calculator")
        self.root.geometry("550x550")
        self.root.resizable(False, False)
        
        # Estilo moderno
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Helvetica', 10))
        self.style.configure('TButton', font=('Helvetica', 10), padding=5)
        self.style.configure('TEntry', font=('Helvetica', 10), padding=5)
        
        # Frame principal
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        # Título
        self.title_label = ttk.Label(self.main_frame, 
                                   text="Down Force Prediction Calculator", 
                                   font=('Helvetica', 14, 'bold'))
        self.title_label.pack(pady=(0, 20))
        
        # Frame de entrada de datos
        self.input_frame = ttk.Frame(self.main_frame)
        self.input_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Campos de entrada
        self.cl_label = ttk.Label(self.input_frame, text="Lift Coefficient (Cl):")
        self.cl_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.cl_entry = ttk.Entry(self.input_frame)
        self.cl_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        
        self.area_label = ttk.Label(self.input_frame, text="Top Area (m²):")
        self.area_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.area_entry = ttk.Entry(self.input_frame)
        self.area_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)
        
        self.speed_label = ttk.Label(self.input_frame, text="Speed (km/h):")
        self.speed_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.speed_entry = ttk.Entry(self.input_frame)
        self.speed_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.EW)
        
        # Botón de cálculo
        self.calculate_button = ttk.Button(self.main_frame, 
                                         text="Calculate Down Force", 
                                         command=self.calculate_downforce)
        self.calculate_button.pack(pady=(10, 20))
        
        # Frame de resultados
        self.result_frame = ttk.Frame(self.main_frame)
        self.result_frame.pack(fill=tk.BOTH, expand=True)
        
        self.result_label = ttk.Label(self.result_frame, 
                                     text="Results:", 
                                     font=('Helvetica', 12, 'bold'))
        self.result_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Variables para resultados
        self.newtons_var = tk.StringVar()
        self.kg_var = tk.StringVar()
        self.ton_var = tk.StringVar()
        

        # Footer frame en la parte inferior
        self.footer_frame = ttk.Frame(self.main_frame)
        self.footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(20, 0))

        # Label del footer centrado
        self.footer_label = ttk.Label(
            self.footer_frame, 
            text="Code by Alfirasy_597 | UI by Softcronos.com.ar | v0.1", 
            style='Footer.TLabel'
        )
        self.footer_label.pack(pady=5)
        
        # Configurar peso de columnas para centrado
        self.input_frame.columnconfigure(1, weight=1)


        # Función para copiar valores
        def copy_to_clipboard(value):
            self.root.clipboard_clear()
            self.root.clipboard_append(value)
            self.root.update()  # Mantiene el valor en el portapapeles después de cerrar la app
            messagebox.showinfo("Copied", f"Value '{value}' copied to clipboard")
        
        # Resultado en Newtons con botón de copia
        self.newtons_frame = ttk.Frame(self.result_frame)
        self.newtons_frame.pack(fill=tk.X, pady=2)
        self.newtons_label = ttk.Label(self.newtons_frame, textvariable=self.newtons_var)
        self.newtons_label.pack(side=tk.LEFT)
        self.copy_newtons = ttk.Button(self.newtons_frame, text="Copy", 
                                     command=lambda: copy_to_clipboard(self.newtons_var.get().split(": ")[1].replace("N", "").strip()))
        self.copy_newtons.pack(side=tk.RIGHT, padx=5)
        
        # Resultado en Kg con botón de copia
        self.kg_frame = ttk.Frame(self.result_frame)
        self.kg_frame.pack(fill=tk.X, pady=2)
        self.kg_label = ttk.Label(self.kg_frame, textvariable=self.kg_var)
        self.kg_label.pack(side=tk.LEFT)
        self.copy_kg = ttk.Button(self.kg_frame, text="Copy", 
                                command=lambda: copy_to_clipboard(self.kg_var.get().split(": ")[1].replace("Kg", "").strip()))
        self.copy_kg.pack(side=tk.RIGHT, padx=5)
        
        # Resultado en Toneladas con botón de copia
        self.ton_frame = ttk.Frame(self.result_frame)
        self.ton_frame.pack(fill=tk.X, pady=2)
        self.ton_label = ttk.Label(self.ton_frame, textvariable=self.ton_var)
        self.ton_label.pack(side=tk.LEFT)
        self.copy_ton = ttk.Button(self.ton_frame, text="Copy", 
                                  command=lambda: copy_to_clipboard(self.ton_var.get().split(": ")[1].replace("Metric Ton", "").strip()))
        self.copy_ton.pack(side=tk.RIGHT, padx=5)
        
        # Configurar peso de columnas para centrado
        self.input_frame.columnconfigure(1, weight=1)
        
    def calculate_downforce(self):
        try:
            # Obtener valores de entrada
            Cl = float(self.cl_entry.get())
            A = float(self.area_entry.get())
            s = float(self.speed_entry.get())/3.6
            ro = 1.225
            
            # Calcular downforce
            Fd = (ro * s**2 * A * Cl)/2
            Fd_Kg = Fd/9.81
            
            # Mostrar resultados formateados
            self.newtons_var.set(f"Down Force: {Fd:.2f} N")
            self.kg_var.set(f"Down Force: {Fd_Kg:.2f} Kg")
            self.ton_var.set(f"Down Force: {Fd_Kg/1000:.4f} Metric Ton")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values in all fields")

if __name__ == "__main__":
    root = tk.Tk()
    app = DownForceCalculator(root)
    root.mainloop()