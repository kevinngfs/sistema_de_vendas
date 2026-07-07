import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from dominio.vendas_interativo import Estoque, CarrinhoDeCompras

class TelaVendas(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title('Ponto de Vendas')
        self.geometry('800x550') 
        self.grab_set()

        banco_de_dados = Estoque()
        self.estoque = banco_de_dados.estoque_mock
        self.carrinho_backend = CarrinhoDeCompras()

        self.criar_layout()
        self.carregar_produtos()
        self.atualizar_interface()

    def criar_layout(self):
        self.frame_produtos_container = ttk.LabelFrame(self, text="Produtos Disponíveis")
        self.frame_produtos_container.place(relx=0.02, rely=0.02, relwidth=0.45, relheight=0.75)

        self.canvas_produtos = tk.Canvas(self.frame_produtos_container, highlightthickness=0)
        self.scrollbar_produtos = ttk.Scrollbar(self.frame_produtos_container, orient="vertical", command=self.canvas_produtos.yview)
        self.canvas_produtos.configure(yscrollcommand=self.scrollbar_produtos.set)

        self.scrollbar_produtos.pack(side="right", fill="y")
        self.canvas_produtos.pack(side="left", fill="both", expand=True)

        self.canvas_produtos.bind("<MouseWheel>", lambda e: self.canvas_produtos.yview_scroll(-1*(e.delta//120), "units"))
        self.canvas_produtos.bind("<Button-4>", lambda e: self.canvas_produtos.yview_scroll(-1, "units"))
        self.canvas_produtos.bind("<Button-5>", lambda e: self.canvas_produtos.yview_scroll(1, "units"))

        self.frame_produtos = ttk.Frame(self.canvas_produtos)
        self.canvas_window = self.canvas_produtos.create_window((0, 0), window=self.frame_produtos, anchor="nw")

        self.frame_produtos.bind(
            "<Configure>",
            lambda e: self.canvas_produtos.configure(scrollregion=self.canvas_produtos.bbox("all"))
        )
        self.canvas_produtos.bind(
            "<Configure>",
            lambda e: self.canvas_produtos.itemconfig(self.canvas_window, width=e.width)
        )

        self.frame_carrinho = ttk.LabelFrame(self, text="Carrinho de Compras")
        self.frame_carrinho.place(relx=0.5, rely=0.02, relwidth=0.48, relheight=0.75)

        colunas = ("item", "qtd", "preco", "subtotal")
        self.tree = ttk.Treeview(self.frame_carrinho, columns=colunas, show="headings")
        self.tree.heading("item", text="Item")
        self.tree.heading("qtd", text="Qtd")
        self.tree.heading("preco", text="Preço Unit.")
        self.tree.heading("subtotal", text="Subtotal")
        
        self.tree.column("item", width=120)
        self.tree.column("qtd", width=50, anchor="center")
        self.tree.column("preco", width=80, anchor="e")
        self.tree.column("subtotal", width=80, anchor="e")
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

        btn_remover = tk.Button(self.frame_carrinho, text="Remover Item Selecionado", command=self.abrir_janela_remover)
        btn_remover.pack(pady=5)

        self.frame_inferior = tk.Frame(self, bg="#d9d9d9", relief="raised", bd=2)
        self.frame_inferior.place(relx=0.0, rely=0.8, relwidth=1.0, relheight=0.2)

        self.lbl_total = tk.Label(self.frame_inferior, text="Total: R$ 0.00", font=('Arial', 24, 'bold'), bg="#d9d9d9", fg="green")
        self.lbl_total.pack(side="left", padx=20)

        btn_finalizar = tk.Button(self.frame_inferior, text="Finalizar Venda", font=('Arial', 14, 'bold'), bg="#4caf50", fg="white", command=self.finalizar_venda)
        btn_finalizar.pack(side="right", padx=20, pady=20)

        btn_voltar = tk.Button(self.frame_inferior, text="Voltar", font=('Arial', 12), command=self.destroy)
        btn_voltar.pack(side="right", padx=10)

    def carregar_produtos(self):
        row, col = 0, 0
        for produto, preco in self.estoque.items():
            texto_btn = f"{produto}\nR$ {preco:.2f}"
            btn = tk.Button(self.frame_produtos, text=texto_btn, font=('Arial', 10), width=15, height=3, command=lambda p=produto, v=preco: self.abrir_janela_adicionar(p, v))
            btn.grid(row=row, column=col, padx=10, pady=10)
            
            col += 1
            if col > 1: 
                col = 0
                row += 1

    def abrir_janela_adicionar(self, produto, preco):
        JanelaQuantidade(self, "Adicionar", produto, preco)

    def abrir_janela_remover(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um item no carrinho para remover!")
            return
        
        item_id = selecionado[0]
        produto = self.tree.item(item_id, "values")[0]
        JanelaQuantidade(self, "Remover", produto, 0)

    def adicionar_ao_carrinho(self, produto, preco, qtd):
        self.carrinho_backend.adicionar_item(produto, preco, qtd)
        self.atualizar_interface()

    def remover_do_carrinho(self, produto, qtd):
        self.carrinho_backend.remover_item(produto, qtd)
        self.atualizar_interface()

    def atualizar_interface(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        itens_carrinho = self.carrinho_backend.obter_itens()
        for prod, dados in itens_carrinho.items():
            preco = dados["preco"]
            qtd = dados["qtd"]
            subtotal = preco * qtd
            self.tree.insert("", "end", values=(prod, qtd, f"R$ {preco:.2f}", f"R$ {subtotal:.2f}"))
            
        total = self.carrinho_backend.calcular_total()
        self.lbl_total.config(text=f"Total: R$ {total:.2f}")

    def finalizar_venda(self):
        sucesso, total_final = self.carrinho_backend.simular_registro_venda()
        
        if not sucesso:
            messagebox.showerror("Erro", "O carrinho está vazio!")
            return
        
        messagebox.showinfo("Sucesso", f"Venda de R$ {total_final:.2f} registrada com sucesso!")
        self.atualizar_interface()


class JanelaQuantidade(tk.Toplevel):
    def __init__(self, master, acao, produto, preco):
        super().__init__(master)
        self.master = master
        self.acao = acao
        self.produto = produto
        self.preco = preco
        
        self.title(f"{acao} Quantidade")
        self.geometry("250x150")
        self.grab_set()

        lbl_texto = f"{acao} '{produto}':"
        if acao == "Remover":
            lbl_texto += "\n(Digite um número grande para remover tudo)"

        tk.Label(self, text=lbl_texto).pack(pady=10)

        self.spin_qtd = tk.Spinbox(self, from_=1, to=1000, width=10, font=('Arial', 12))
        self.spin_qtd.pack(pady=5)

        btn_confirmar = tk.Button(self, text="Confirmar", command=self.confirmar)
        btn_confirmar.pack(pady=10)

    def confirmar(self):
        try:
            qtd = int(self.spin_qtd.get())
            if qtd <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Digite uma quantidade válida (maior que zero)!", parent=self)
            return

        if self.acao == "Adicionar":
            self.master.adicionar_ao_carrinho(self.produto, self.preco, qtd)
        elif self.acao == "Remover":
            self.master.remover_do_carrinho(self.produto, qtd)
            
        self.destroy()
