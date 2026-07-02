import tkinter as tk

class TelaEstoque(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title('Gerenciar Produtos e Estoque')
        self.geometry('600x400')


        self.grab_set()

        self.interface()

    def interface(self):
        titulo = tk.Label(self, text='Controle de Estoque', font=('Arial', 24, 'bold'))
        titulo.pack(pady=30)


        texto_temporario = (
            'fazendo'
        )

        lbl_info = tk.Label(self, text=texto_temporario, font=('Arial', 14), justify='center')
        lbl_info.pack(pady=40)

        btn_voltar = tk.Button(self, text="Voltar ao Menu", font=('Arial', 10), command=self.destroy)
        btn_voltar.pack(side='bottom', pady=20)