from dados.persistencia import PersistenciaDados

class CarrinhoDeCompras:
    """
    Classe responsável por gerenciar o carrinho de compras
    Métodos:
        __init__: Inicializa a classe, criando um dicionário vazio para armazenar os itens do carrinho
        adicionar_item: Adiciona um item ao carrinho ou atualiza a quantidade se o item já estiver presente, recebe o nome do produto, preço e quantidade
        remover_item: Remove uma quantidade de um item do carrinho ou remove o item completamente, recebe o nome do produto e a quantidade a ser removida
        obter_carrinho: Retorna os itens que estão atualmente no carrinho
        calcular_total: Calcula o preço total dos itens no carrinho
        limpar_carrinho: Tira todos os itens do carrinho, esvaziando-o
    """
    def __init__(self):
        self.carrinho = {}

    def adicionar_item(self, produto, preco, qtd):
        if produto in self.carrinho:
            self.carrinho[produto]["qtd"] += qtd
        else:
            self.carrinho[produto] = {"preco": preco, "qtd": qtd}

    def remover_item(self, produto, qtd_remover):
        if produto not in self.carrinho:
            return
        if self.carrinho[produto]["qtd"] <= qtd_remover:
            del self.carrinho[produto]
        else:
            self.carrinho[produto]["qtd"] -= qtd_remover

    def obter_carrinho(self):
        return self.carrinho

    def calcular_total(self):
        return sum(item["preco"] * item["qtd"] for item in self.carrinho.values())

    def limpar_carrinho(self):
        self.carrinho.clear()


class ProcessadorVendas:
    """
    Classe responsável por processar as vendas e gerenciar o estoque
    Métodos:
        __init__: Inicializa a classe, carregando os dados do banco de dados e armazenando o estoque e as vendas
        obter_produtos_disponiveis: Retorna os produtos disponíveis no estoque
        finalizar_venda: Finaliza a venda, atualizando o estoque e registrando a venda, recebe o carrinho de compras como parâmetro
    """
    def __init__(self):
        self.persistencia = PersistenciaDados()
        self.dados_sistema = self.persistencia.carregar()
        self.estoque = self.dados_sistema.get("estoque", {})
        self.vendas = self.dados_sistema.get("vendas", [])

    def obter_produtos_disponiveis(self):
        self.dados_sistema = self.persistencia.carregar()
        self.estoque = self.dados_sistema.get("estoque", {})
        return self.estoque

    def finalizar_venda(self, carrinho_compras):
        carrinho = carrinho_compras.obter_carrinho()
        if not carrinho:
            return False, "Carrinho vazio"

        self.dados_sistema = self.persistencia.carregar()
        self.vendas = self.dados_sistema.get("vendas", [])

        proximo_id = max([venda.get("id", 0) for venda in self.vendas], default=0) + 1
        itens_venda = []
        
        for produto, info in carrinho.items():
            itens_venda.append((f"{produto} (x{info['qtd']})", info["preco"] * info["qtd"]))

        nova_venda = {
            "id": proximo_id,
            "total": carrinho_compras.calcular_total(),
            "itens": itens_venda
        }

        self.vendas.append(nova_venda)
        self.dados_sistema["vendas"] = self.vendas
        self.persistencia.salvar(self.dados_sistema)
        carrinho_compras.limpar_carrinho()
        return True, "Venda realizada com sucesso"
