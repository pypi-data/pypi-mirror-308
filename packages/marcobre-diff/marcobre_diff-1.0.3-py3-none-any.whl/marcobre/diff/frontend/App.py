
# import pkg_resources
# from PIL import Image
# from marcobre.diff.backend.backend import create_historical_table
# import customtkinter as ctk

# import marcobre.diff
# from marcobre.diff.frontend.ContainerInputFile import ContainerInputFile
# from marcobre.diff.frontend.MainTable import MainTable

# class App(ctk.CTk):
#     def __init__(self):
#         super().__init__()

#         create_historical_table()

#         ctk.set_appearance_mode('light')
#         ctk.set_default_color_theme('blue')
#         self.title('Marcobre - Reducción del tiempo de procesamiento de modelo de bloques')
#         self.geometry('1280x720')

#         self.rowconfigure(0, weight=0)
#         self.rowconfigure(1, weight=0)
#         self.rowconfigure(2, weight=0)
#         self.rowconfigure(3, weight=1)
#         self.columnconfigure(0, weight=1)


#         #logo_path = 'frontend/images/logo.png'
#         logo_path = pkg_resources.resource_filename(marcobre.diff.PKG_NAME, 'static/frontend/images/logo.png')
#         self.logo_image = ctk.CTkImage(light_image=Image.open(logo_path),
#                                         dark_image=Image.open(logo_path),
#                                         size=(130, 27))


#         self.logo_label = ctk.CTkLabel(self, image=self.logo_image,text="")
#         self.logo_label.grid(
#             column=0,
#             row=0,
#             padx=(10, 5),
#             pady=(10, 0),
#             sticky="nw"
#         )


#         self.title_label = ctk.CTkLabel(self, text='REDUCCIÓN DEL TIEMPO DE PROCESAMIENTO DE MODELO DE BLOQUES',
#                                          font=("Arial", 16, "bold"),
#                                          text_color="#2E6696")
#         self.title_label.grid(
#             column=0,
#             row=1,
#             padx=(10, 10),
#             pady=(5, 10),
#             sticky="nsew"
#         )


#         self.main_table = MainTable(self)
#         self.main_table.grid(
#             column=0,
#             row=3,
#             padx=(20, 20),
#             pady=(10,20),
#             sticky="nsew"
#         )


#         self.container_input_file = ContainerInputFile(self, main_table=self.main_table,fg_color="#FFFFFF")
#         self.container_input_file.grid(
#             column=0,
#             row=2,
#             padx=(20, 20),
#             pady=10,
#             sticky="nsew",

#         )


import os
import pkg_resources
from PIL import Image
from marcobre.diff.backend.backend import create_historical_table, create_historical_table_model
import customtkinter as ctk
import configparser
import marcobre.diff
from marcobre.diff.frontend.ContainerInputFile import ContainerInputFile
from marcobre.diff.frontend.ContainerInputFileModels import ContainerInputFileModels
from marcobre.diff.frontend.MainTable import MainTable
from marcobre.diff.frontend.MainTableModels import MainTableModels

class ContainerButtons(ctk.CTkFrame):
    def __init__(self, app, **kwargs):
        super().__init__(app, **kwargs)
        self.app = app
        self.config = configparser.ConfigParser()
        self.config_file = os.path.expanduser("~/.app_config.ini")

        #logo_path = 'frontend/images/logo.png'
        logo_path = pkg_resources.resource_filename(marcobre.diff.PKG_NAME, 'static/frontend/images/logo.png')
        self.logo_image = ctk.CTkImage(light_image=Image.open(logo_path),
                                        dark_image=Image.open(logo_path),
                                        size=(130, 27))

        # Botón para ir a la segunda ventana
        self.button_to_second_window = ctk.CTkButton(self, text="Comparación de modelos", command=self.app.create_second_window, width=120, fg_color="#fff", text_color="#000")
        self.button_to_second_window.grid(
            column=2,
            row=0, 
            padx=10, 
            pady=10
        )  

        # Botón para ir a la primera ventana
        self.button_to_first_window = ctk.CTkButton(self, text="Reducción del tiempo", command=self.app.create_first_window, width=120, fg_color="#fff", text_color="#000")
        self.button_to_first_window.grid(column=1, row=0, padx=10, pady=10)  

        self.logo_label = ctk.CTkLabel(self, image=self.logo_image,text="")
        self.logo_label.grid(
            column=0,
            row=0,
            padx=(10, 5), #10 5
            pady=(10, 0),# 10 0
            sticky="nw"
        )

        # Agregar eventos para el hover
        self.button_to_second_window.bind("<Enter>", lambda event: self.on_hover(self.button_to_second_window, True))
        self.button_to_second_window.bind("<Leave>", lambda event: self.on_hover(self.button_to_second_window, False))
        self.button_to_first_window.bind("<Enter>", lambda event:  self.on_hover(self.button_to_first_window, True))
        self.button_to_first_window.bind("<Leave>", lambda event:  self.on_hover(self.button_to_first_window, False))

    def on_hover(self, button, hover):
        if hover:
            button.configure(fg_color="#000", text_color="#fff") 
        else:
            button.configure(fg_color="#fff", text_color="#000")  


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        #self.main_frame = ctk.CTkFrame(self)
        #self.main_frame.pack(fill='both', expand=True)
        self.create_first_window()

    def create_first_window(self):

        # Limpiar el marco
        for widget in self.winfo_children():
            widget.destroy()

        create_historical_table()
        ctk.set_appearance_mode('light')
        ctk.set_default_color_theme('blue')

        self.title('Marcobre - Reducción del tiempo de procesamiento de modelo de bloques')
        self.geometry('1280x720')

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=0)
        self.rowconfigure(3, weight=1)
        self.columnconfigure(0, weight=1)


        #logo_path = 'frontend/images/logo.png'
        # logo_path = pkg_resources.resource_filename(marcobre.diff.PKG_NAME, 'static/frontend/images/logo.png')
        # self.logo_image = ctk.CTkImage(light_image=Image.open(logo_path),
        #                                 dark_image=Image.open(logo_path),
        #                                 size=(130, 27))

        # Botón para ir a la segunda ventana
        # self.button_to_second_window = ctk.CTkButton(self, text="Comparación de modelos", command=self.create_second_window)
        # self.button_to_second_window.grid(column=1, row=0, padx=10, pady=10)  # Asegúrate de que el índice de fila sea correcto

        # self.logo_label = ctk.CTkLabel(self, image=self.logo_image,text="")
        # self.logo_label.grid(
        #     column=0,
        #     row=0,
        #     padx=(10, 5), #10 5
        #     pady=(10, 0),# 10 0
        #     sticky="nw"
        # )

        self.container_buttons_file = ContainerButtons(self)
        self.container_buttons_file.grid(
            column=0,
            row=0,
            padx=(20, 20),
            pady=10,
            sticky="nsew",
        )

        self.title_label = ctk.CTkLabel(self, text='REDUCCIÓN DEL TIEMPO DE PROCESAMIENTO DE MODELO DE BLOQUES',
                                        font=("Arial", 16, "bold"),
                                        text_color="#2E6696")
        self.title_label.grid(
            column=0,
            row=1,
            padx=(10, 10), #10 10
            pady=(5, 10), #5,10
            sticky="nsew"
        )


        self.main_table = MainTable(self)
        self.main_table.grid(
            column=0,
            row=3,
            padx=(20, 20),
            pady=(10,20),
            sticky="nsew"
        )


        self.container_input_file = ContainerInputFile(self, main_table=self.main_table,fg_color="#FFFFFF")
        self.container_input_file.grid(
            column=0,
            row=2,
            padx=(20, 20),
            pady=10,
            sticky="nsew",

        )

    def create_second_window(self):

        # Limpiar el marco
        for widget in self.winfo_children():
            widget.destroy()

        create_historical_table_model()
        ctk.set_appearance_mode('light')
        ctk.set_default_color_theme('blue')

        self.title('Marcobre - Comparación de Modelos')
        self.geometry('1280x720')

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=0)
        self.rowconfigure(3, weight=1)
        self.columnconfigure(0, weight=1)


        #logo_path = 'frontend/images/logo.png'
        # logo_path = pkg_resources.resource_filename(marcobre.diff.PKG_NAME, 'static/frontend/images/logo.png')
        # self.logo_image = ctk.CTkImage(light_image=Image.open(logo_path),
        #                                 dark_image=Image.open(logo_path),
        #                                 size=(130, 27))


        # self.logo_label = ctk.CTkLabel(self, image=self.logo_image,text="")
        # self.logo_label.grid(
        #     column=0,
        #     row=0,
        #     padx=(10, 5),
        #     pady=(10, 0),
        #     sticky="nw"
        # )

        self.container_buttons_file = ContainerButtons(self)
        self.container_buttons_file.grid(
            column=0,
            row=0,
            padx=(20, 20),
            pady=10,
            sticky="nsew",
        )

        self.title_label = ctk.CTkLabel(self, text='COMPARACIÓN DE MODELOS',
                                        font=("Arial", 16, "bold"),
                                        text_color="#2E6696")
        self.title_label.grid(
            column=0,
            row=1,
            padx=(10, 10),
            pady=(5, 10),
            sticky="nsew"
        )


        self.main_table = MainTableModels(self)
        self.main_table.grid(
            column=0,
            row=3,
            padx=(20, 20),
            pady=(10,20),
            sticky="nsew"
        )


        self.container_input_file = ContainerInputFileModels(self, main_table=self.main_table,fg_color="#FFFFFF")
        self.container_input_file.grid(
            column=0,
            row=2,
            padx=(20, 20),
            pady=10,
            sticky="nsew",

        )






