from dados.persistencia import PersistenciaDados

class Produtos:
    """
    Classe responsável por gerenciar as informações dos produtos em estoque
    Métodos:
        __init__: Inicializa a classe, carregando os dados do banco de dados, recebe como parâmetro opcional uma lista de vendas
        obter_vendas: Retorna a lista das vendas
        calcular_faturamento_total: Retorna o faturamento total com base nas vendas registradas
    """
    def __init__(self, vendas=None):
        banco = PersistenciaDados()
        dados = banco.carregar()
        self.vendas = dados["vendas"]

    def obter_vendas(self):
        return self.vendas.copy()

    def calcular_faturamento_total(self):
        return sum(venda['total'] for venda in self.vendas)
