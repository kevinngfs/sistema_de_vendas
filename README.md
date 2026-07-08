# Programa de Vendas em pyhton
## Integrantes da equipe e suas contribuições

* Ana Beatriz

**Armazenamento e recuperação de dados** 
>Desenvolvimento do banco de dados através da persistência via serialização e integração de arquitetura

* Helder Roger

**Documentação** 
>Escrita do arquivo README e dos comentários dentro do código

* Kevin Nilton

**Interface gráfica** 
>Desenvolvimento do *front-end* através da biblioteca de interface gráfica *Tkinter*

* Pedro Freitas

***Back-end*** 
>Desenvolvimento da classe de negócios, o código de vendas propriamente dito

## Como rodar

Para acessar o programa de vendas, basta rodar o arquivo ```menu_principal.py```

## Distribuição
```
SISTEMA_DE_VENDAS.
│   menu_principal.py - arquivo principal/menu que leva à outras telas - Kevin
│   README.md - documentação - Helder
│   
├───dados - gravação de dados - Ana Beatriz
│       persistencia.py
│       __init__.py
│       
├───dominio - Back-end - Pedro
│       estoque_interativo.py
│       relatorios_interativo.
│       vendas_interativo.py
│       __init__.py
│       
└───telas - Telas de interface - Kevin
        tela_estoque.py
        tela_relatorios.py
        tela_vendas.py
        __init__.py
```