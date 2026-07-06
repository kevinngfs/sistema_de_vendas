def add_estoque(janela_formulario):
    produto_nome = janela_formulario.entry_produto.get()
    preco_produto = janela_formulario.entry_preco.get()

    if produto_nome and preco_produto:
        try:
            preco_float = float(preco_produto.replace(',', '.'))
            janela_formulario.master.adicionar_item_na_lista(produto_nome, f"{preco_float:.2f}")
            janela_formulario.destroy()
        except ValueError:
            janela_formulario.master.lbl_info.config(text="Erro: O preço deve ser um número!", fg="red")
    else:
        janela_formulario.master.lbl_info.config(text="Erro: Preencha todos os campos!", fg="red")