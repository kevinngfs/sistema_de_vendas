from dados.persistencia import PersistenciaDados

def add_estoque(janela_formulario):
    produto_nome = janela_formulario.entry_produto.get().strip()
    preco_produto = janela_formulario.entry_preco.get().strip()
    qtd_produto = janela_formulario.entry_qtd.get().strip()

    if produto_nome and preco_produto and qtd_produto:
        try:
            preco_float = float(preco_produto.replace(',', '.'))
            qtd_int = int(qtd_produto)
            
            banco = PersistenciaDados()
            dados = banco.carregar()
            
            if isinstance(dados.get("estoque"), list):
                dados["estoque"] = {}
                
            dados["estoque"][produto_nome] = {
                "preco": preco_float,
                "quantidade": qtd_int
            }
            
            banco.salvar(dados)

            janela_formulario.master.adicionar_item_na_lista(produto_nome, f"{preco_float:.2f}", str(qtd_int))
            janela_formulario.destroy()
        except ValueError:
            janela_formulario.master.lbl_info.config(text="Erro: Preço ou quantidade inválidos!", fg="red")
    else:
        janela_formulario.master.lbl_info.config(text="Erro: Preencha todos os campos!", fg="red")
