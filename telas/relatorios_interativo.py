class Produtos:
    def __init__(self, vendas=None):
        self.vendas = vendas if vendas else [
            {'id': 1, 'total': 150.00, 'itens': [('Mouse', 50.0), ('Teclado', 100.0)]},
            {'id': 2, 'total': 2200.00, 'itens': [('Notebook', 2200.0)]},
            {'id': 3, 'total': 45.00, 'itens': [('Mousepad', 45.0)]},
            {'id': 4, 'total': 120.00, 'itens': [('Fone de Ouvido', 120.0)]},
            {'id': 5, 'total': 850.00, 'itens': [('Monitor 24"', 850.0)]},
            {'id': 6, 'total': 30.00, 'itens': [('Cabo HDMI', 30.0)]},
            {'id': 7, 'total': 15.00, 'itens': [('Pendrive 16GB', 15.0)]},
        ]

    def obter_vendas(self):
        return self.vendas.copy()

    def calcular_faturamento_total(self):
        return sum(venda['total'] for venda in self.vendas)