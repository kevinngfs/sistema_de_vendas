import tkinter as tk
from tkinter import ttk, messagebox
from dominio.estoque_interativo import add_estoque
from dados.persistencia import PersistenciaDados

# Nesse arquivo temos duas classes: TelaEstoque e AddEstoqueFrame. A primeira cria a janela principal para gerenciamento de estoque, a segunda é a janela para adicionar novos itens ao estoque

class TelaEstoque(tk.Toplevel):
    """
    Classe responsável por criar a interface de gerenciamento de estoque
    Métodos:
        __init__: Inicializa a classe, criando a janela principal(do estoque) e chamando os métodos para construir a interface e carregar os dados iniciais, recebe como parâmetro a janela mestre (master)
        interface: Cria os elementos da interface gráfica, incluindo botões, labels e uma tabela para exibir os produtos em estoque
        abrir_formulario: Abre a janela de formulário para adicionar um novo item ao estoque
        adicionar_item_na_lista: Adiciona um item à lista de produtos em estoque
        carregar_dados_iniciais: Carrega os dados do banco de dados e preenche a tabela com os produtos existentes
    """
    def __init__(self, master):
        super().__init__(master)
        self.title('Gerenciar Produtos e Estoque')
        self.geometry('700x450')
        self.grab_set()

        self.interface()
        self.carregar_dados_iniciais()

    def interface(self):
        titulo = tk.Label(self, text='Estoque', font=('Arial', 24, 'bold'))
        titulo.pack(pady=15)

        frame_topo = tk.Frame(self)
        frame_topo.pack(fill='x', padx=40, pady=5)

        add_button = tk.Button(frame_topo, text='Adicionar Item', font=('Arial', 10),
                               command=self.abrir_formulario)
        add_button.pack(side='left')

        self.lbl_info = tk.Label(frame_topo, text="", font=('Arial', 10))
        self.lbl_info.pack(side='left', padx=20)

        # --- TROCANDO O CANVAS PELA TABELA (TREEVIEW) ---
        frame_tabela = tk.Frame(self)
        frame_tabela.pack(fill='both', expand=True, padx=40, pady=10)

        colunas = ('nome', 'preco', 'qtd')
        self.tree = ttk.Treeview(frame_tabela, columns=colunas, show='headings')
        self.tree.heading('nome', text='Nome / Código do Item')
        self.tree.heading('preco', text='Preço (R$)')
        self.tree.heading('qtd', text='Quantidade em Estoque')

        self.tree.column('nome', width=300)
        self.tree.column('preco', width=100, anchor='center')
        self.tree.column('qtd', width=150, anchor='center')

        scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side='right', fill='y')
        self.tree.pack(side='left', fill='both', expand=True)

        btn_voltar = tk.Button(self, text="Voltar ao Menu", font=('Arial', 10), command=self.destroy)
        btn_voltar.pack(side='bottom', pady=15)

    def abrir_formulario(self):
        AddEstoqueFrame(self)

    def adicionar_item_na_lista(self, produto, preco, quantidade="0"):
        # Adiciona a linha na tabela instantaneamente.
        # O 'quantidade="0"' garante que o código antigo do seu colega não quebre a sua tela!
        self.tree.insert('', 'end', values=(produto, f"R$ {preco}", quantidade))
        self.lbl_info.config(text=f"Adicionado: {produto}", fg="green")

    def carregar_dados_iniciais(self):
        # A interface lê o banco de dados só para se desenhar na tela ao abrir
        banco = PersistenciaDados()
        dados = banco.carregar()
        estoque = dados.get("estoque", {})

        for produto, info in estoque.items():
            if isinstance(info, dict):
                preco = info.get("preco", 0.0)
                qtd = info.get("quantidade", 0)
            else:
                preco = info  # Trata o formato antigo
                qtd = 0

            self.tree.insert('', 'end', values=(produto, f"R$ {float(preco):.2f}", qtd))


class AddEstoqueFrame(tk.Toplevel):
    """
    Classe responsável por criar a interface de formulário para adicionar novos itens ao estoque
    Métodos:
        __init__: Inicializa a classe, criando a janela de formulário e chamando o método para construir a interface, recebe como parâmetro a janela mestre (master)
        criar_formulario: Cria os elementos da interface gráfica do formulário
    """
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.title('Novo Item')
        self.geometry('300x270')
        self.grab_set()
        self.criar_formulario()

    def criar_formulario(self):
        tk.Label(self, text="Nome/Código do Item:", font=('Arial', 10)).pack(pady=(10, 0))
        self.entry_produto = tk.Entry(self, width=30)
        self.entry_produto.pack(pady=5)

        tk.Label(self, text="Preço do Item (R$):", font=('Arial', 10)).pack(pady=(10, 0))
        self.entry_preco = tk.Entry(self, width=30)
        self.entry_preco.pack(pady=5)

        # --- O CAMPO NOVO DE QUANTIDADE QUE FALTAVA PARA O FRONT-END ---
        tk.Label(self, text="Quantidade Inicial:", font=('Arial', 10)).pack(pady=(10, 0))
        self.entry_qtd = tk.Entry(self, width=30)
        self.entry_qtd.pack(pady=5)

        # Mantive o botão chamando o back-end deles exatamente do jeito que estava
        btn_salvar = tk.Button(self, text="Salvar Item", command=lambda: add_estoque(self))
        btn_salvar.pack(pady=15)
