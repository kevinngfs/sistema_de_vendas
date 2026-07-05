import tkinter as tk

# Separando as telas em arquivos diferentes, isso possibilita uma melhor 
# organização do código e facilita uma possível manutenção posterior 

from telas.tela_vendas import TelaVendas
from telas.tela_estoque import TelaEstoque
from telas.tela_relatorios import TelaRelatorios

# Aqui encontramos a classe principal do sistema de interface
# Como é possível notar, essa é uma classe filha da classe Tk
# Deixar a classe como filha permite usar os métodos e atributos da classe Tk como se fossem da própria classe

class Sistema(tk.Tk):
    """Classe principal do sistema de interface
    Atributos: Nenhum
    Métodos:
        __init__: Cria a janela principal do sistema
        interface: Chamada automaticamente pelo método __init__, cria a interface do sistema
        abrir_vendas: Abre a aba de vendas do sistema
        abrir_estoque: Abre a aba de gerenciamento de produtos e estoque
        abrir_relatorios: Abre a aba de relatórios financeiros do sistema
    """
    def __init__(self):
        super().__init__()
        self.title('Menu Principal')
        self.geometry('800x670')

        self.interface()

    def interface(self):
        titulo = tk.Label(self, text='Sistema de Vendas', font=('Arial', 30, 'bold'))
        titulo.pack(pady=(30, 0))

        frame_menu = tk.Frame(self)
        frame_menu.pack(expand=True)

        botao_vendas = tk.Button(frame_menu, text='Ponto de Vendas', font=('Arial', 14),
                                 command=self.abrir_vendas)
        botao_vendas.pack(pady=10)

        botao_estoque = tk.Button(frame_menu, text='Gerenciar Produtos e Estoque', font=('Arial', 14),
                                  command=self.abrir_estoque)
        botao_estoque.pack(pady=10)

        botao_relatorio = tk.Button(frame_menu, text='Relatórios Financeiros', font=('Arial', 14),
                                    command=self.abrir_relatorios)
        botao_relatorio.pack(pady=10)

        botao_fechar = tk.Button(frame_menu, text="Sair", font=('Arial', 10), command=self.destroy)
        botao_fechar.pack(pady=(60, 0))

    def abrir_vendas(self):
        TelaVendas(self)

    def abrir_estoque(self):
        TelaEstoque(self)

    def abrir_relatorios(self):
        TelaRelatorios(self)


janela = Sistema()
janela.mainloop()