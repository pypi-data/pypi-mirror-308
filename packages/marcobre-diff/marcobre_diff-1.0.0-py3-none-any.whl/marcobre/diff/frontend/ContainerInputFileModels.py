import os
import customtkinter as ctk
from tkinter import filedialog, Toplevel,Label,messagebox
import threading
import time
import configparser
#from marcobre.diff.backend.algorithm.algorithm import algorithm_function
from marcobre.diff.backend.algorithm.algorithmModels import algorithm_function_models
import csv
import zipfile

class ContainerInputFileModels(ctk.CTkFrame):
    def __init__(self, master, main_table, **kwargs):
        super().__init__(master, **kwargs)
        self.main_table = main_table

        self.config = configparser.ConfigParser()
        self.config_file = os.path.expanduser("~/.app_config.ini")

        self.file3_label = ctk.CTkLabel(self, text="Archivo 01: Modelo de largo plazo", anchor="w", text_color="#2D649B")
        self.file3_label.grid(row=0, column=0, padx=(10, 5), pady=(10, 0), sticky="w")

        self.file4_label = ctk.CTkLabel(self, text="Archivo 02: Modelo de corto plazo", anchor="w", text_color="#2D649B")
        self.file4_label.grid(row=0, column=2, padx=(10, 5), pady=(10, 0), sticky="w")

        self.file5_label = ctk.CTkLabel(self, text="Archivo 03: Cortes", anchor="w", text_color="#2D649B")
        self.file5_label.grid(row=0, column=4, padx=(10, 5), pady=(10, 0), sticky="w")

        self.file3_entry = ctk.CTkEntry(self, width=50)
        self.file3_entry.grid(row=1, column=0, padx=(10, 5), pady=(0, 5), sticky="we")

        self.file3_button = ctk.CTkButton(
            self,
            text="Seleccionar",
            command=self.select_file3,
            width=120,
            fg_color="#E7EEF7",
            text_color="#2D649B",
        )
        self.file3_button.grid(row=1, column=1, padx=(5, 10), pady=(0, 5), sticky="w")


        self.file3_button.bind("<Enter>", lambda e: self.on_hover(self.file3_button, True))
        self.file3_button.bind("<Leave>", lambda e: self.on_hover(self.file3_button, False))

        self.file4_entry = ctk.CTkEntry(self, width=50)
        self.file4_entry.grid(row=1, column=2, padx=(10, 5), pady=(0, 5), sticky="we")

        self.file4_button = ctk.CTkButton(
            self,
            text="Seleccionar",
            command=self.select_file4,
            width=120,
            fg_color="#E7EEF7",
            text_color="#2D649B"
        )
        self.file4_button.grid(row=1, column=3, padx=(5, 10), pady=(0, 5), sticky="w")


        self.file4_button.bind("<Enter>", lambda e: self.on_hover(self.file4_button, True))
        self.file4_button.bind("<Leave>", lambda e: self.on_hover(self.file4_button, False))

        ######*Nuevo archivo añadido########
        self.file5_entry = ctk.CTkEntry(self, width=120)
        self.file5_entry.grid(row=1, column=4, padx=(10, 5), pady=(0, 5), sticky="we")

        self.file5_button = ctk.CTkButton(
            self,
            text="Seleccionar",
            command=self.select_file5,
            width=120,
            fg_color="#E7EEF7",
            text_color="#2D649B"
        )
        self.file5_button.grid(row=1, column=5, padx=(5, 10), pady=(0, 5), sticky="w")


        self.file5_button.bind("<Enter>", lambda e: self.on_hover(self.file5_button, True))
        self.file5_button.bind("<Leave>", lambda e: self.on_hover(self.file5_button, False))
        #*########################################

        self.submit_btn = ctk.CTkButton(
            self,
            text="Procesar",
            width=180,
            command=self.on_submit,
            fg_color="#2D649B",
            text_color="#FFFFFF"
        )
        self.submit_btn.grid(row=1, column=6, padx=(10, 10), pady=(0, 10), sticky="e")
        self.submit_btn.bind("<Enter>", lambda e: self.on_hover_submit(self.submit_btn, True))
        self.submit_btn.bind("<Leave>", lambda e: self.on_hover_submit(self.submit_btn, False))

        self.timer_label = ctk.CTkLabel(self, text="")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(3, weight=0)
        self.grid_columnconfigure(4, weight=0)

        self.load_config()

        self.loader_frame = ctk.CTkFrame(self, fg_color="#FFFFFF")
        self.loader_frame.grid(row=2, column=0, columnspan=5, sticky="nsew")
        self.loader_frame.grid_remove()

        self.loader_label = ctk.CTkLabel(self.loader_frame, text="Procesando...", text_color="#2D649B")
        self.loader_label.pack(pady=2)

        self.loader_indicator = ctk.CTkProgressBar(self.loader_frame)
        self.loader_indicator.pack(pady=10)

    def on_hover_submit(self, button, hover):
        if hover:
            button.configure(fg_color="#2E6696", text_color="#FFFFFF")
            button.configure(cursor="hand2")
        else:
            button.configure(fg_color="#2D649B", text_color="#FFFFFF")
            button.configure(cursor="")

    def on_hover(self, button, hover):
        if hover:
            button.configure(fg_color="#E7EEF7", text_color="#2D649B")
            button.configure(cursor="hand2")
        else:
            button.configure(fg_color="#E7EEF7", text_color="#2D649B")
            button.configure(cursor="")

    def load_config(self):
        if os.path.exists(self.config_file):
            self.config.read(self.config_file)
            self.file3_path = self.config.get('Paths', 'file3', fallback='')
            self.file4_path = self.config.get('Paths', 'file4', fallback='')
            self.file5_path = self.config.get('Paths', 'file5', fallback='')

            # if not os.path.exists(self.file3_path):
            #     self.file3_path = ''

            # self.file1_entry.delete(0, ctk.END)
            # self.file1_entry.insert(0, self.file1_path)
            self.file3_entry.delete(0, ctk.END)
            self.file3_entry.insert(0, self.file3_path)
            self.file4_entry.delete(0, ctk.END)
            self.file4_entry.insert(0, self.file4_path)
            self.file5_entry.delete(0, ctk.END)
            self.file5_entry.insert(0, self.file5_path)
        else:
            self.file1_path = ''
            self.file2_path = ''
            self.config['Paths'] = {}

    def save_config(self):
        self.config['Paths']['file3'] = self.file3_entry.get()
        self.config['Paths']['file4'] = self.file4_entry.get()
        self.config['Paths']['file5'] = self.file5_entry.get()
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

    def select_file3(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file3_entry.delete(0, ctk.END)
            self.file3_entry.insert(0, file_path)
            self.save_config()

    def select_file4(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file4_entry.delete(0, ctk.END)
            self.file4_entry.insert(0, file_path)
            self.save_config()
    
    #*select_file3

    def select_file5(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file5_entry.delete(0, ctk.END)
            self.file5_entry.insert(0, file_path)
            self.save_config()

    #*######    

    def on_submit(self):
        long_term_model = self.file3_entry.get().strip()
        short_term_model = self.file4_entry.get().strip()
        cuttings = self.file5_entry.get().strip()

        if not long_term_model or not short_term_model or not cuttings:
            messagebox.showwarning("Advertencia", "Por favor, seleccione los 3 archivos antes de procesar.")
            return

        if not os.path.exists(long_term_model):
            messagebox.showerror("Error", f"El archivo 1 no existe: {long_term_model}")
            return

        if not os.path.exists(short_term_model):
            messagebox.showerror("Error", f"El archivo 2 no existe: {short_term_model}")
            return
        
        if not os.path.exists(cuttings):
            messagebox.showerror("Error", f"El archivo 3 no existe: {cuttings}")
            return

        if not long_term_model.lower().endswith('.zip'):
            messagebox.showerror("Error", f"El archivo 1 debe ser un ZIP: {long_term_model}")
            return

        if not short_term_model.lower().endswith('.csv'):
            messagebox.showerror("Error", f"El archivo 2 debe ser un CSV: {short_term_model}")
            return
        
        if not cuttings.lower().endswith('.dxf'):
            messagebox.showerror("Error", f"El archivo 3 debe ser un DXF: {cuttings}")
            return
        #"PTOPO"
        required_columns = ["EAST", "NORTH", "ELEV","CLASS","LITH","CUT","CUAS","CUCN","CUR","C","FE","AG","S","AU","P","AS","SG","OTYPE","MODLO","CATHM","FLMET","FCUR","LCUR","BMU","BVU","BENE","MTYPE","STYPE","TON","ZVOL","RATOX"]

        if not self.validate_csv_columns_zip(long_term_model, required_columns):
            return

        if not self.validate_csv_columns(short_term_model, required_columns):
            return

        self.submit_btn.configure(text="Procesando...", state="disabled")
        self.disable_inputs()
        self.timer_label.configure(text="Tiempo: 0 segundos")

        print(f"Archivo Largo Plazo: {long_term_model}, Archivo Corto Plazo: {short_term_model}, Archivo de Cortes: {cuttings}")
        self.show_loader()
        threading.Thread(target=self.run_algorithm_with_timer, args=(long_term_model, short_term_model, cuttings)).start()

    def validate_csv_columns_zip(self, zip_file_path, required_columns):
        try:
            # Extraer archivos del ZIP
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                # Extraer todos los archivos en un directorio temporal
                temp_dir = os.path.join(os.path.dirname(zip_file_path), 'temp_csv')
                os.makedirs(temp_dir, exist_ok=True)
                zip_ref.extractall(temp_dir)

                # Leer el primer archivo CSV en el ZIP
                csv_files = [f for f in zip_ref.namelist() if f.endswith('.csv')]
                if not csv_files:
                    messagebox.showerror("Error", f"No se encontraron archivos CSV en el ZIP: {zip_file_path}.")
                    return False

                csv_file_path = os.path.join(temp_dir, csv_files[0])

            # Leer el CSV y validar columnas
            with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                header = next(reader)

                missing_columns = [col for col in required_columns if col not in header]

                if missing_columns:
                    messagebox.showerror("Error",
                                        f"El archivo {csv_file_path} no contiene las columnas requeridas: {', '.join(missing_columns)}")
                    return False
                return True
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el archivo {zip_file_path}: {str(e)}")
            return False
        finally:
            # Limpiar el directorio temporal
            if 'temp_dir' in locals():
                for f in os.listdir(temp_dir):
                    os.remove(os.path.join(temp_dir, f))
                os.rmdir(temp_dir)

    def validate_csv_columns(self, file_path, required_columns):
        try:
            with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                header = next(reader)

                missing_columns = [col for col in required_columns if col not in header]

                if missing_columns:
                    messagebox.showerror("Error",
                                         f"El archivo {file_path} no contiene las columnas requeridas: {', '.join(missing_columns)}")
                    return False
                return True
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el archivo {file_path}: {str(e)}")
            return False

    def run_algorithm_with_timer(self, long_term_model, short_term_model, cuttings):
        start_time = time.time()
        algorithm_function_models(long_term_model, short_term_model, cuttings)
        elapsed_time = time.time() - start_time

        self.timer_label.configure(text=f"Tiempo: {int(elapsed_time)} segundos")
        self.hide_loader()
        self.enable_inputs()
        #self.master.main_table.refresh_table()

    def disable_inputs(self):
        self.file3_entry.configure(state="disabled")
        self.file4_entry.configure(state="disabled")
        self.file5_entry.configure(state="disabled")
        self.file3_button.configure(state="disabled", fg_color="#E7EEF7")
        self.file4_button.configure(state="disabled", fg_color="#E7EEF7")
        self.file5_button.configure(state="disabled", fg_color="#E7EEF7")
        self.loader_frame.grid()  # Mostrar loader
        self.loader_indicator.start()

    def enable_inputs(self):
        self.file3_entry.configure(state="normal")
        self.file4_entry.configure(state="normal")
        self.file5_entry.configure(state="normal")
        self.file3_button.configure(state="normal")
        self.file4_button.configure(state="normal")
        self.file5_button.configure(state="normal")
        self.submit_btn.configure(text="Procesar", state="normal")
        self.loader_frame.grid_remove()
        self.loader_indicator.stop()

    def show_loader(self):
        self.loader_frame.grid()
        self.loader_indicator.start()

    def hide_loader(self):
        self.loader_frame.grid_remove()
        self.loader_indicator.stop()
