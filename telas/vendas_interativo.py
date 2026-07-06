class Estoque:
    def __init__(self):     
        self.estoque_mock = {
            "Arroz 5kg": 25.50,
            "Feijão 1kg": 8.00,
            "Macarrão": 4.50,
            "Óleo de Soja": 6.00,
            "Café 500g": 15.00,
            "Açúcar 1kg": 4.00,
            "Leite 1L": 6.99,
            "Leite 2L": 6.99,
            "Leite 3L": 6.99,
            "Leite 4L": 6.99,
            "Leite 5L": 6.99,
            "Leite 6L": 6.99,
            "Leite 7L": 6.99
        }


class CarrinhoDeCompras:
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
            
        qtd_atual = self.carrinho[produto]["qtd"]
        if qtd_remover >= qtd_atual:
            del self.carrinho[produto]
        else:
            self.carrinho[produto]["qtd"] -= qtd_remover

    def obter_itens(self):
        return self.carrinho

    def calcular_total(self):
        return sum(dados["preco"] * dados["qtd"] for dados in self.carrinho.values())

    def simular_registro_venda(self):
        if not self.carrinho:
            return False, 0.0
        
        total_venda = self.calcular_total()
        self.carrinho.clear()
        return True, total_venda