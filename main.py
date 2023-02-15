#sistema de gerenciamento para logistas
#o programa tem como objetivo auxiliar o logista a gerenciar seu estoque, clientes, fornecedores, vendas e compras
#Autor: Leonardo da silva de jesus
#Data: 13/02/2023
#Versão: 0.0.1
#Licença: GPL

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import sqlite3
import time

#criando a conexão com o banco de dados
def conectar(comando_sql):
    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()
    cursor.execute(comando_sql)
    conexao.commit()
    conexao.close()

#criando conexão com o banco de dados para buscar dados
def conectar_buscar(comando_sql):
    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()
    cursor.execute(comando_sql)
    conexao.commit()
    dados = cursor.fetchall()
    conexao.close()
    return dados

#criando conexão com o banco de dados para inserir dados
def conectar_inserir(comando_sql):
    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()
    cursor.execute(comando_sql)
    conexao.commit()
    id = cursor.lastrowid
    conexao.close()
    return id

#criando tabelas no banco de dados
def criar_tabelas():
    comando_sql = "CREATE TABLE IF NOT EXISTS clientes (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, telefone TEXT, email TEXT, endereco TEXT)"
    conectar(comando_sql)
    comando_sql = "CREATE TABLE IF NOT EXISTS fornecedores (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, ramo TEXT, telefone TEXT, email TEXT, endereco TEXT)"
    conectar(comando_sql)
    comando_sql = "CREATE TABLE IF NOT EXISTS produtos (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, descricao TEXT, preco_compra REAL, preco_venda REAL, id_fornecedor INTEGER, quantidade INTEGER)"
    conectar(comando_sql)
    comando_sql = "CREATE TABLE IF NOT EXISTS vendas (id INTEGER PRIMARY KEY AUTOINCREMENT, id_cliente INTEGER, id_produto INTEGER, quantidade INTEGER, data TEXT, FOREIGN KEY(id_cliente) REFERENCES clientes(id), FOREIGN KEY(id_produto) REFERENCES produtos(id))"
    conectar(comando_sql)
    comando_sql = "CREATE TABLE IF NOT EXISTS compras (id INTEGER PRIMARY KEY AUTOINCREMENT, id_fornecedor INTEGER, id_produto INTEGER, quantidade INTEGER, data TEXT, FOREIGN KEY(id_fornecedor) REFERENCES fornecedores(id), FOREIGN KEY(id_produto) REFERENCES produtos(id))"
    conectar(comando_sql)

#checkar se o banco de dados existe
try:
    arquivo = open("banco.db", "r")
    arquivo.close()
except:
    arquivo = open("banco.db", "w")
    arquivo.close()
    criar_tabelas()


#função para cadastrar clientes
def janela_cadastrar_cliente():
    #função para cadastrar clientes no banco de dados
    def cadastrar_cliente_bd(nome, telefone, email, endereco, janela_cadastro_clientes):
        #verificando se os campos estão preenchidos
        if nome == "" or telefone == "" or email == "" or endereco == "":
            label_info["text"] = "Preencha todos os campos!"
            janela_cadastro_clientes.update_idletasks()
            time.sleep(1)
            label_info["text"] = ""
            return
        comando_sql = "INSERT INTO clientes (nome, telefone, email, endereco) VALUES ('" + nome + "', '" + telefone + "', '" + email + "', '" + endereco + "')"
        conectar(comando_sql)
        label_info["text"] = "Cliente cadastrado com sucesso!"
        janela_cadastro_clientes.update_idletasks()
        time.sleep(1)
        janela_cadastro_clientes.destroy()

    #criando a janela de cadastro de clientes
    janela_cadastro_clientes = tk.Toplevel()
    janela_cadastro_clientes.title("Cadastro de clientes")
    janela_cadastro_clientes.resizable(False, False)
    janela_cadastro_clientes.configure(background="#ffffff")

    #criando os labels
    label_nome = tk.Label(janela_cadastro_clientes, text="Nome:", bg="#ffffff", fg="#000000")
    label_nome.grid(row=0, column=0, padx=10, pady=10)
    label_telefone = tk.Label(janela_cadastro_clientes, text="Telefone:", bg="#ffffff", fg="#000000")
    label_telefone.grid(row=1, column=0, padx=10, pady=10)
    label_email = tk.Label(janela_cadastro_clientes, text="E-mail:", bg="#ffffff", fg="#000000")
    label_email.grid(row=2, column=0, padx=10, pady=10)
    label_endereco = tk.Label(janela_cadastro_clientes, text="Endereço:", bg="#ffffff", fg="#000000")
    label_endereco.grid(row=3, column=0, padx=10, pady=10)
    label_info = tk.Label(janela_cadastro_clientes, text="", bg="#ffffff", fg="#000000")
    label_info.grid(row=4, column=0, columnspan=2, padx=10, pady=10)



    #criando os campos de entrada
    entrada_nome = tk.Entry(janela_cadastro_clientes, width=50)
    entrada_nome.grid(row=0, column=1, padx=10, pady=10)
    entrada_telefone = tk.Entry(janela_cadastro_clientes, width=50)
    entrada_telefone.grid(row=1, column=1, padx=10, pady=10)
    entrada_email = tk.Entry(janela_cadastro_clientes, width=50)
    entrada_email.grid(row=2, column=1, padx=10, pady=10)
    entrada_endereco = tk.Entry(janela_cadastro_clientes, width=50)
    entrada_endereco.grid(row=3, column=1, padx=10, pady=10)

    #criando o botão de cadastro
    botao_cadastrar = tk.Button(janela_cadastro_clientes, text="Cadastrar", command=lambda: cadastrar_cliente_bd(entrada_nome.get(), entrada_telefone.get(), entrada_email.get(), entrada_endereco.get(), janela_cadastro_clientes))
    botao_cadastrar.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    #criando o botão de cancelar
    botao_cancelar = tk.Button(janela_cadastro_clientes, text="Cancelar", command=janela_cadastro_clientes.destroy)
    botao_cancelar.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    #fazendo a janela ficar no centro da tela
    janela_cadastro_clientes.update_idletasks()
    largura = janela_cadastro_clientes.winfo_width()
    altura = janela_cadastro_clientes.winfo_height()
    x = (janela_cadastro_clientes.winfo_screenwidth() // 2) - (largura // 2)
    y = (janela_cadastro_clientes.winfo_screenheight() // 2) - (altura // 2)
    janela_cadastro_clientes.geometry('{}x{}+{}+{}'.format(largura, altura, x, y))
    janela_cadastro_clientes.mainloop()


#função para consultar clientes
def janela_consultar_editar_cliente():
    #gera uma tabela com os clientes cadastrados no banco de dados mostrando o id, nome, telefone, email e endereço
    def gerar_tabela():
        #deletando a tabela anterior
        try:
            tabela.destroy()
        except:
            pass

        #criando a tabela
        tabela = ttk.Treeview(janela_consulta_clientes, height=10, columns=("id", "nome", "telefone", "email", "endereco"))
        tabela.heading("#0", text="")
        tabela.heading("id", text="ID")
        tabela.heading("nome", text="Nome")
        tabela.heading("telefone", text="Telefone")
        tabela.heading("email", text="E-mail")
        tabela.heading("endereco", text="Endereço")
        tabela.column("#0", width=0)
        tabela.column("id", width=50)
        tabela.column("nome", width=200)
        tabela.column("telefone", width=100)
        tabela.column("email", width=200)
        tabela.column("endereco", width=300)
        tabela.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        #adicionar scroll na tabela
        scroll = tk.Scrollbar(janela_consulta_clientes, orient="vertical", command=tabela.yview)
        scroll.grid(row=1, column=2, sticky="ns")
        tabela.configure(yscrollcommand=scroll.set)

        #preenchendo a tabela
        comando_sql = "SELECT * FROM clientes"
        resultado = conectar_buscar(comando_sql)
        for linha in resultado:
            tabela.insert("", "end", values=(linha[0], linha[1], linha[2], linha[3], linha[4]))

        
        #criando pesquisa
        entrada_pesquisa = tk.Entry(janela_consulta_clientes, width=50)
        entrada_pesquisa.grid(row=0, column=0, padx=10, pady=10)
    
        #criando o botão de pesquisar
        botao_pesquisar = tk.Button(janela_consulta_clientes, text="Pesquisar", command=lambda: pesquisar_cliente())
        botao_pesquisar.grid(row=0, column=1, columnspan=1, padx=10, pady=10)

        #criando o botão de editar
        botao_editar = tk.Button(janela_consulta_clientes, text="Editar", command=lambda: editar_cliente(tabela))
        botao_editar.grid(row=3, column=0, columnspan=1, padx=10, pady=10)

        #criando o botão de excluir
        botao_excluir = tk.Button(janela_consulta_clientes, text="Excluir", command=lambda: excluir_cliente(tabela.item(tabela.selection())["values"][0]))
        botao_excluir.grid(row=3, column=1, columnspan=1, padx=10, pady=10)

        
        #função para pesquisar clientes
        def pesquisar_cliente():
            tabela.selection_set("")
            nome = entrada_pesquisa.get()
            nome= str(nome)
            for linha in tabela.get_children():
                if nome in tabela.item(linha)["values"][1]:
                    tabela.selection_set(linha)
                    tabela.focus(linha)
                    break
        
        #função para editar clientes
        def editar_cliente(tabela):
            #pegando os dados da linha selecionada
            id = tabela.item(tabela.selection())["values"][0]
            nome = tabela.item(tabela.selection())["values"][1]
            telefone = tabela.item(tabela.selection())["values"][2]
            email = tabela.item(tabela.selection())["values"][3]
            endereco = tabela.item(tabela.selection())["values"][4]
            
            #criando a janela de edição
            janela_editar_cliente = tk.Toplevel()
            janela_editar_cliente.title("SisGen - Editar cliente")
            janela_editar_cliente.geometry("400x300")
            janela_editar_cliente.resizable(False, False)
            janela_editar_cliente.configure(background="#ffffff")
            
            #criando o label de título
            label_titulo = tk.Label(janela_editar_cliente, text="Editar cliente", bg="#ffffff", fg="#000000")
            label_titulo.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
            
            label_nome = tk.Label(janela_editar_cliente, text="Nome:", bg="#ffffff", fg="#000000")
            label_nome.grid(row=1, column=0, padx=10, pady=10)
            entrada_nome = tk.Entry(janela_editar_cliente)
            entrada_nome.grid(row=1, column=1, padx=10, pady=10)
            entrada_nome.insert(0, nome)
            label_telefone = tk.Label(janela_editar_cliente, text="Telefone:", bg="#ffffff", fg="#000000")
            label_telefone.grid(row=2, column=0, padx=10, pady=10)
            entrada_telefone = tk.Entry(janela_editar_cliente)
            entrada_telefone.grid(row=2, column=1, padx=10, pady=10)
            entrada_telefone.insert(0, telefone)
            label_email = tk.Label(janela_editar_cliente, text="E-mail:", bg="#ffffff", fg="#000000")
            label_email.grid(row=3, column=0, padx=10, pady=10)
            entrada_email = tk.Entry(janela_editar_cliente)
            entrada_email.grid(row=3, column=1, padx=10, pady=10)
            entrada_email.insert(0, email)
            label_endereco = tk.Label(janela_editar_cliente, text="Endereço:", bg="#ffffff", fg="#000000")
            label_endereco.grid(row=4, column=0, padx=10, pady=10)
            entrada_endereco = tk.Entry(janela_editar_cliente)
            entrada_endereco.grid(row=4, column=1, padx=10, pady=10)
            entrada_endereco.insert(0, endereco)
            label_info = tk.Label(janela_editar_cliente, text="", bg="#ffffff", fg="#000000")
            label_info.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
            
            #função para salvar a edição
            def salvar_edicao(id, nome, telefone, email, endereco, janela):
                comando_sql = "UPDATE clientes SET nome='{}', telefone='{}', email='{}', endereco='{}' WHERE id={}".format(nome, telefone, email, endereco, id)
                conectar(comando_sql)
                label_info["text"] = "Cliente editado com sucesso!"
                time.sleep(1)
                label_info["text"] = ""
                janela_editar_cliente.destroy()
                gerar_tabela()

            #criando o botão de salvar
            botao_salvar = tk.Button(janela_editar_cliente, text="Salvar", command=lambda: salvar_edicao(id, entrada_nome.get(), entrada_telefone.get(), entrada_email.get(), entrada_endereco.get(), janela_editar_cliente))
            botao_salvar.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
            
        
        #função para excluir clientes
        def excluir_cliente(id):
            comando_sql = "DELETE FROM clientes WHERE id={}".format(id)
            conectar(comando_sql)
            tabela.delete(tabela.selection())
            gerar_tabela()



            
    #criando a janela
    janela_consulta_clientes = tk.Toplevel()
    janela_consulta_clientes.title("SisGen - Consultar e editar clientes")
    janela_consulta_clientes.geometry("870x500")
    janela_consulta_clientes.resizable(False, False)
    janela_consulta_clientes.configure(background="#ffffff")
    
    gerar_tabela()

    








#criando a janela principal
janela = tk.Tk()
janela.title("SisGen - Sistema de gerenciamento para logistas")
janela.geometry("800x600")
janela.state("zoomed")
janela.resizable(True, True)
janela.configure(background="#000000")
data_hora = time.strftime("%d/%m/%Y %H:%M:%S")
rodape = tk.Label(janela, text="Data e hora: " + data_hora, bg="#000000", fg="#ffffff")
rodape.pack(side="bottom", fill="x")

#mosta uma imagem na janela
plano_de_fundo = Image.open("arquivos/plano_de_fundo.jpg")
plano_de_fundo = ImageTk.PhotoImage(plano_de_fundo)
plano_de_fundo_label = tk.Label(janela, image=plano_de_fundo)
plano_de_fundo_label.place(x=0, y=0, relwidth=1, relheight=1)


#criando o menu
menu = tk.Menu(janela)
janela.config(menu=menu)

#criando o menu clientes
menu_clientes = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Clientes", menu=menu_clientes)
menu_clientes.add_command(label="Cadastrar", command=janela_cadastrar_cliente)
menu_clientes.add_command(label="Consultar e Editar", command=janela_consultar_editar_cliente)


#criando o menu fornecedores
menu_fornecedores = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Fornecedores", menu=menu_fornecedores)
menu_fornecedores.add_command(label="Cadastrar")
menu_fornecedores.add_command(label="Consultar e Editar")

#criando o menu produtos
menu_produtos = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Produtos", menu=menu_produtos)
menu_produtos.add_command(label="Cadastrar")
menu_produtos.add_command(label="Consultar e Editar")

#criando o menu vendas
menu_movimentacoes = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Movimentações", menu=menu_movimentacoes)
menu_movimentacoes.add_command(label="Vendas")
menu_movimentacoes.add_command(label="Compras")
menu_movimentacoes.add_command(label="Relatórios")

#criando o menu ajuda
menu_ajuda = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Ajuda", menu=menu_ajuda)
menu_ajuda.add_command(label="Sobre")

janela.mainloop()