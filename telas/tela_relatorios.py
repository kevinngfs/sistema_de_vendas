import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from dominio.relatorios_interativo import Produtos

class TelaRelatorios(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title('Relatórios Financeiros')
        self.geometry('600x500')
        self.grab_set()

        self.backend = Produtos()
        self.vendas_totais = self.backend.obter_vendas()
        
        self.interface()

    def interface(self):
        titulo = tk.Label(self, text='Relatórios e Faturamento', font=('Arial', 24, 'bold'))
        titulo.pack(pady=(20, 10))

        total_geral = self.backend.calcular_faturamento_total()
        
        lbl_total = tk.Label(self, text=f'Faturamento Total: R$ {total_geral:.2f}', font=('Arial', 14, 'bold'), fg='green')
        lbl_total.pack(pady=(0, 20))

        container_lista = tk.Frame(self)
        container_lista.pack(fill='both', expand=True, padx=40, pady=(0, 20))

        self.canvas = tk.Canvas(container_lista, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container_lista, orient="vertical", command=self.canvas.yview)
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

        self.canvas.bind_all("<MouseWheel>", self.ao_rolar_mouse)      
        self.canvas.bind_all("<Button-4>", self.ao_rolar_mouse)        
        self.canvas.bind_all("<Button-5>", self.ao_rolar_mouse)        

        for venda in self.vendas_totais:
            frame_venda = tk.Frame(self.scrollable_frame, bd=1, relief="solid", padx=10, pady=10)
            frame_venda.pack(fill='x', pady=5, padx=5)

            texto_venda = f"Venda #{venda['id']}  |  Total: R$ {venda['total']:.2f}"
            lbl_venda = tk.Label(frame_venda, text=texto_venda, font=('Arial', 11))
            lbl_venda.pack(side='left')

            btn_ver = tk.Button(frame_venda, text="Ver Relatório", 
                                command=lambda v=venda: self.confirmar_abertura(v))
            btn_ver.pack(side='right')

        btn_voltar = tk.Button(self, text="Voltar", font=('Arial', 10), command=self.fechar_tela)
        btn_voltar.pack(side='bottom', pady=20)

    def ao_rolar_mouse(self, event):
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")

    def fechar_tela(self):
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")
        self.destroy()

    def confirmar_abertura(self, venda):
        resposta = messagebox.askyesno(
            title="Confirmação", 
            message=f"Deseja abrir o relatório detalhado da Venda #{venda['id']}?"
        )
        if resposta:
            self.mostrar_detalhes(venda)

    def mostrar_detalhes(self, venda):
        detalhes_window = tk.Toplevel(self)
        detalhes_window.title(f"Relatório de Venda #{venda['id']}")
        detalhes_window.geometry('350x400')
        detalhes_window.grab_set()

        titulo = tk.Label(detalhes_window, text=f"Detalhes da Venda #{venda['id']}", font=('Arial', 16, 'bold'))
        titulo.pack(pady=15)

        frame_itens = ttk.LabelFrame(detalhes_window, text="Itens Comprados", padding=(10, 10))
        frame_itens.pack(fill='both', expand=True, padx=20, pady=10)

        for nome_item, preco_item in venda['itens']:
            tk.Label(frame_itens, text=f"• {nome_item}: R$ {preco_item:.2f}", font=('Arial', 11)).pack(anchor='w', pady=2)

        tk.Label(detalhes_window, text=f"Soma da Venda: R$ {venda['total']:.2f}", font=('Arial', 12, 'bold'), fg='green').pack(pady=10)

        tk.Button(detalhes_window, text="Fechar Relatório", command=detalhes_window.destroy).pack(pady=15)
