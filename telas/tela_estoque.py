import tkinter as tk
from tkinter import ttk

class TelaEstoque(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title('Gerenciar Produtos e Estoque')
        self.geometry('600x400')

        self.grab_set()
        self.itens_preco_frame()
        self.interface()

    def interface(self):
        ### Título topo do frame
        titulo = tk.Label(self, text='Estoque', font=('Arial', 24, 'bold')) 
        titulo.pack(pady=25)

        ### botão de adicionar item
        add_button = tk.Button(self, text='adicionar item', font=('Arial', 9), 
                               command=lambda: add_estoque_frame(self))
        add_button.place(x=40, y=80)

        self.lbl_info = tk.Label(self, text="", font=('Arial', 10))
        self.lbl_info.place(x=180, y=82)

        ### botão para volar para a tela principal
        btn_voltar = tk.Button(self, text="Voltar ao Menu", font=('Arial', 10), command=self.destroy)
        btn_voltar.pack(side='bottom', pady=20)

    def itens_preco_frame(self):
        container_principal = tk.Frame(self)
        container_principal.place(relx=0.5, y=140, anchor='n', relwidth=0.85, relheight=0.45)

        self.canvas = tk.Canvas(container_principal, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container_principal, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollable_frame = ttk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width)
        )

        self.scrollable_frame.columnconfigure(0, weight=2)
        self.scrollable_frame.columnconfigure(1, weight=1)

        ### Frame de itens
        self.itens_frame = ttk.Labelframe(self.scrollable_frame, text="Itens")
        self.itens_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

        # Frame de preços
        self.preco_frame = ttk.LabelFrame(self.scrollable_frame, text="Preço")
        self.preco_frame.grid(row=0, column=1, sticky="nsew")

    ### Função de adicionar itens na lista (foco da persistência de dados 
    # manter esses valores existentes mesmo após fechar o frame)
    def adicionar_item_na_lista(self, produto, preco):
        lbl_p = tk.Label(self.itens_frame, text=produto, font=('Arial', 10))
        lbl_p.pack(anchor='w', padx=10, pady=2)
        
        sep_p = ttk.Separator(self.itens_frame, orient='horizontal')
        sep_p.pack(fill='x', padx=10, pady=(2, 5))

        lbl_v = tk.Label(self.preco_frame, text=f"R$ {preco}", font=('Arial', 10))
        lbl_v.pack(anchor='w', padx=10, pady=2)
        
        sep_v = ttk.Separator(self.preco_frame, orient='horizontal')
        sep_v.pack(fill='x', padx=10, pady=(2, 5))
        
        self.lbl_info.config(text=f"Adicionado: {produto}", fg="green")
        

class add_estoque_frame(tk.Toplevel):
    ### Frame que popa quando clicar em adicionar item
    def __init__(self, master):
        super().__init__(master)
        self.master = master 
        self.title('Item e preço')
        self.geometry('250x180') 
        self.grab_set()          
        
        self.criar_formulario()

    ### Função para criar a caixa de texto que permite 
    # inserir o produto e o preço
    def criar_formulario(self):
        ### Entrada de dados do produto
        label_produto = tk.Label(self, text="Nome/Código do Item:", font=('Arial', 10))
        label_produto.pack(pady=(10, 0))
        self.entry_produto = tk.Entry(self, width=25)
        self.entry_produto.pack(pady=5)

        ### Entrada de dados do preço
        label_preco = tk.Label(self, text="Preço do Item:", font=('Arial', 10))
        label_preco.pack(pady=(10, 0))
        self.entry_preco = tk.Entry(self, width=25)
        self.entry_preco.pack(pady=5)

        ### Botão de salvar itens
        btn_salvar = tk.Button(self, text="Salvar Item", command=self.add_estoque)
        btn_salvar.pack(pady=15)
    
    ### Função que pede a entrada de dados para o botão de adicionar item
    def add_estoque(self):
        produto_nome = self.entry_produto.get()
        preco_produto = self.entry_preco.get()

        if produto_nome and preco_produto:
            try:
                preco_float = float(preco_produto.replace(',', '.'))
                self.master.adicionar_item_na_lista(produto_nome, f"{preco_float:.2f}")
                self.destroy()
            except ValueError:
                self.master.lbl_info.config(text="Erro: O preço deve ser um número!", fg="red")
            
        ### Tratamento de erro simples
        else:
            self.master.lbl_info.config(text="Erro: Preencha todos os campos!", fg="red")
