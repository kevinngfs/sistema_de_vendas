import tkinter as tk

class TelaVendas(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title('Ponto de Vendas')
        self.geometry('600x400')

        self.grab_set()

        #placeholder só
        tk.Label(self, text="fazendo", font=('Arial', 20)).pack(pady=50)
        tk.Button(self, text="Voltar", font=('Arial', 12), command=self.destroy).pack()