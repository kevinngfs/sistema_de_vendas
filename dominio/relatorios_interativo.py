from dados.persistencia import PersistenciaDados

class Produtos:
    def __init__(self, vendas=None):
        banco = PersistenciaDados()
        dados = banco.carregar()
        self.vendas = dados["vendas"]

    def obter_vendas(self):
        return self.vendas.copy()

    def calcular_faturamento_total(self):
        return sum(venda['total'] for venda in self.vendas)