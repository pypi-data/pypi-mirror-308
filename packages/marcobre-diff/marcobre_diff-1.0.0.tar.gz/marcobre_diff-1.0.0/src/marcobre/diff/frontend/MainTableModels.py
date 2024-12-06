import customtkinter as ctk
from tkinter import ttk
from marcobre.diff.backend.backend import get_all_historical_model, delete_historical_model


class MainTableModels(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        # self.records = get_all_historical_model()
        self.create_table()

    def create_table(self):

        style = ttk.Style()
        style.configure("Treeview",
                        background="#808080",
                        foreground="#2D649B",
                        rowheight=25)
        style.configure("Treeview.Heading",
                        background="#808080",
                        foreground="#71717A",
                        font=('Arial', 10, 'bold'))



        style.map("Treeview.Heading",
                  background=[('active', '#2D649B')],
                  foreground=[('active', '#808080')])


        style.map("Treeview",
                  background=[("selected", "#2D649B")],
                  foreground=[("selected", "#808080")])


        self.tree = ttk.Treeview(self, columns=("Date", "LP", "CP","CUTS", "Output"), show='headings')
        # self.tree.heading("Date", text="FECHA DE CREACIÓN")
        # self.tree.heading("File", text="MODELO DE BLOQUE ACTUAL")
        # self.tree.heading("CMP", text="MODELO DE BLOQUE DE REFERENCIA")
        # self.tree.heading("Output", text="NUEVO NOMBRE MODELO DE BLOQUE")
        # self.tree.heading("Date", text="FECHA DE CREACIÓN")
        # self.tree.heading("LP", text="MODELO DE LARGO PLAZO")
        # self.tree.heading("CP", text="MODELO DE CORTO PLAZO")
        # self.tree.heading("CUTS", text="CORTES")
        # self.tree.heading("Output", text="RESULTADO")

        # self.tree.column("Date", width=50)
        # self.tree.column("LP", width=140)
        # self.tree.column("CP", width=140)
        # self.tree.column("CUTS", width=140)
        # self.tree.column("Output", width=300)

        self.tree.pack(fill="both", expand=True)

        # for record in self.records:
        #     self.tree.insert("", "end", iid=record[0], values=(record[1], record[2], record[3], record[4]))

        # self.delete_button = ctk.CTkButton(self, text="Eliminar Seleccionado", command=self.remove_selected,
        #                                    fg_color="#ff6666", hover_color="#ff4d4d")
        # self.delete_button.pack(side="top", anchor="ne", padx=10, pady=10)
        # self.delete_button.configure(state="disabled")

        # self.delete_button.bind("<Enter>", lambda e: self.on_hover(self.delete_button, True))
        # self.delete_button.bind("<Leave>", lambda e: self.on_hover(self.delete_button, False))

        #self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    # def refresh_table(self):
    #     for item in self.tree.get_children():
    #         self.tree.delete(item)

    #     # self.records = get_all_historical_model()

    #     for record in self.records:
    #         self.tree.insert("", "end", iid=record[0], values=(record[1], record[2], record[3], record[4]))

    # def on_hover(self, button, hover):
    #     if hover:
    #         button.configure(fg_color="#ff4d4d", text_color="#FFFFFF")
    #         button.configure(cursor="hand2")  # Cambia el cursor a pointer
    #     else:
    #         button.configure(fg_color="#ff6666", text_color="#FFFFFF")
    #         button.configure(cursor="")

    # def on_tree_select(self, event):
    #     selected_items = self.tree.selection()
    #     if selected_items:
    #         self.delete_button.configure(state="normal")
    #     else:
    #         self.delete_button.configure(state="disabled")

    # def remove_selected(self):
    #     selected_items = self.tree.selection()

    #     if selected_items:
    #         for item in selected_items:
    #             historical_id = int(item)
    #             delete_historical_model(historical_id)
    #             self.tree.delete(item)

    #         # self.records = get_all_historical_model()
    #         self.update_table()

    # def update_table(self):
    #     for item in self.tree.get_children():
    #         self.tree.delete(item)

    #     for record in self.records:
    #         self.tree.insert("", "end", iid=record[0], values=(record[1], record[2], record[3], record[4]))


