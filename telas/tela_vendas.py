import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from dominio.vendas_interativo import ProcessadorVendas, CarrinhoDeCompras

class TelaVendas(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title('Ponto de Vendas')
        self.geometry('800x550') 
        self.grab_set()

        self.processador = ProcessadorVendas()
        self.carrinho_backend = CarrinhoDeCompras()
        self.estoque = self.processador.obter_produtos_disponiveis()

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

        self.scrollable_frame_produtos = ttk.Frame(self.canvas_produtos)
        self.canvas_window = self.canvas_produtos.create_window((0, 0), window=self.scrollable_frame_produtos, anchor="nw")

        self.scrollable_frame_produtos.bind(
            "<Configure>",
            lambda e: self.canvas_produtos.configure(scrollregion=self.canvas_produtos.bbox("all"))
        )
        self.canvas_produtos.bind(
            "<Configure>",
            lambda e: self.canvas_produtos.itemconfig(self.canvas_window, width=e.width)
        )

        self.frame_carrinho_container = ttk.LabelFrame(self, text="Carrinho de Compras")
        self.frame_carrinho_container.place(relx=0.52, rely=0.02, relwidth=0.45, relheight=0.75)

        self.tree_carrinho = ttk.Treeview(self.frame_carrinho_container, columns=("Produto", "Preço", "Qtd", "Subtotal"), show="headings")
        self.tree_carrinho.heading("Produto", text="Produto")
        self.tree_carrinho.heading("Preço", text="Preço")
        self.tree_carrinho.heading("Qtd", text="Qtd")
        self.tree_carrinho.heading("Subtotal", text="Subtotal")
        
        self.tree_carrinho.column("Produto", width=120)
        self.tree_carrinho.column("Preço", width=70)
        self.tree_carrinho.column("Qtd", width=50)
        self.tree_carrinho.column("Subtotal", width=80)
        self.tree_carrinho.pack(fill="both", expand=True)

        self.lbl_total = tk.Label(self, text="Total: R$ 0.00", font=("Arial", 16, "bold"))
        self.lbl_total.place(relx=0.52, rely=0.8)

        self.btn_finalizar = tk.Button(self, text="Finalizar Venda", font=("Arial", 12), command=self.finalizar_venda)
        self.btn_finalizar.place(relx=0.52, rely=0.88)

        self.btn_remover = tk.Button(self, text="Remover Item", font=("Arial", 12), command=self.solicitar_remocao)
        self.btn_remover.place(relx=0.75, rely=0.88)

        self.btn_voltar = tk.Button(self, text="Voltar ao Menu", font=("Arial", 10), command=self.destroy)
        self.btn_voltar.pack(side="bottom", pady=10)

    def carregar_produtos(self):
        self.estoque = self.processador.obter_produtos_disponiveis()
        for widget in self.scrollable_frame_produtos.winfo_children():
            widget.destroy()

        for produto, info in self.estoque.items():
            if isinstance(info, dict):
                preco = info.get("preco", 0.0)
                qtd = info.get("quantidade", 0)
            else:
                preco = info
                qtd = 0

            frame_item = tk.Frame(self.scrollable_frame_produtos, bd=1, relief="solid", padx=5, pady=5)
            frame_item.pack(fill="x", pady=2, padx=2)

            lbl_nome = tk.Label(frame_item, text=f"{produto}\nR$ {float(preco):.2f} | Qtd: {qtd}", font=("Arial", 10), justify="left")
            lbl_nome.pack(side="left")

            btn_add = tk.Button(frame_item, text="Adicionar", command=lambda p=produto, pr=float(preco): JanelaQuantidade(self, "Adicionar", p, pr))
            btn_add.pack(side="right")

    def atualizar_interface(self):
        for row in self.tree_carrinho.get_children():
            self.tree_carrinho.delete(row)

        carrinho = self.carrinho_backend.obter_carrinho()
        for produto, dados in carrinho.items():
            subtotal = dados["preco"] * dados["qtd"]
            self.tree_carrinho.insert("", "end", iid=produto, values=(produto, f"R$ {dados['preco']:.2f}", dados["qtd"], f"R$ {subtotal:.2f}"))

        total = self.carrinho_backend.calcular_total()
        self.lbl_total.config(text=f"Total: R$ {total:.2f}")

    def solicitar_remocao(self):
        selecionado = self.tree_carrinho.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um item no carrinho para remover!")
            return
        produto = selecionado[0]
        carrinho = self.carrinho_backend.obter_carrinho()
        preco = carrinho[produto]["preco"]
        JanelaQuantidade(self, "Remover", produto, preco)

    def finalizar_venda(self):
        sucesso, mensagem = self.processador.finalizar_venda(self.carrinho_backend)
        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            self.atualizar_interface()
        else:
            messagebox.showwarning("Aviso", mensagem)


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
            self.master.carrinho_backend.adicionar_item(self.produto, self.preco, qtd)
        elif self.acao == "Remover":
            self.master.carrinho_backend.remover_item(self.produto, qtd)

        self.master.atualizar_interface()
        self.destroy()
