#programa de gerenciamento de clientes e ordens de serviço
#autor:leonardo da silva de jesus

#instalar o pandas e o tkinter para rodar o programa
#pip install pandas
#pip install tkinter

#bibliotecas
import pandas as pd
import tkinter as tk
from tkinter import ttk
import time
import sqlite3 as sql

#criando o banco de dados clientes.db
conn = sql.connect("data.db")
#criando o cursor
cursor = conn.cursor()
#criando a tabela clientes
cursor.execute("CREATE TABLE IF NOT EXISTS clientes (id INTEGER PRIMARY KEY, nome TEXT, telefone TEXT, endereco TEXT)")
#criando a tabela ordens de serviço
cursor.execute("CREATE TABLE IF NOT EXISTS ordens (id INTEGER PRIMARY KEY, cliente TEXT, data TEXT, descricao TEXT, valor REAL)")
#salvando as alterações
conn.commit()
#fechando a conexão
conn.close()

#funçoes

#cadastrar cliente
def cadastrar_cliente():
    #criando a janela
    janela_cadastrar_cliente = tk.Tk()
    janela_cadastrar_cliente.title("GCOS - Cadastrar Cliente")
    janela_cadastrar_cliente.geometry("300x300")
    #background cor branca
    janela_cadastrar_cliente.configure(background="#ffffff")

    #criando os labels
    label_nome = tk.Label(janela_cadastrar_cliente, text="Nome", bg="#ffffff")
    label_nome.place(x=10, y=10)

    label_telefone = tk.Label(janela_cadastrar_cliente, text="Telefone", bg="#ffffff")
    label_telefone.place(x=10, y=40)

    label_endereco = tk.Label(janela_cadastrar_cliente, text="Endereço", bg="#ffffff")
    label_endereco.place(x=10, y=70)

    #criando os campos de texto
    campo_nome = tk.Entry(janela_cadastrar_cliente)
    campo_nome.place(x=100, y=10)

    campo_telefone = tk.Entry(janela_cadastrar_cliente)
    campo_telefone.place(x=100, y=40)

    campo_endereco = tk.Entry(janela_cadastrar_cliente)
    campo_endereco.place(x=100, y=70)

    #função para cadastrar cliente no banco de dados
    def cadastrar_cliente_bd(nome, telefone, endereco):
        #conectando ao banco de dados
        conn = sql.connect("data.db")
        #criando o cursor
        cursor = conn.cursor()
        #inserindo os dados na tabela clientes e gerando o id automaticamente
        cursor.execute("INSERT INTO clientes (nome, telefone, endereco) VALUES (?, ?, ?)", (nome, telefone, endereco))
        #salvando as alterações
        conn.commit()
        #fechando a conexão
        conn.close()
        #mostrando a mensagem de confirmação
        label_confirmacao["text"] = "Cliente cadastrado com sucesso!"
        #atualizando a janela
        janela_cadastrar_cliente.update()
        #esperando 1 segundos
        time.sleep(1)
        #fechando a janela
        janela_cadastrar_cliente.destroy()
   

    #label de confirmação
    label_confirmacao = tk.Label(janela_cadastrar_cliente, text="", bg="#ffffff")
    #posicionando a label abaixo do botão
    label_confirmacao.place(x=10, y=150)

    #criando o botão
    
    botao_cadastrar = tk.Button(janela_cadastrar_cliente, text="Cadastrar", command=lambda: cadastrar_cliente_bd(campo_nome.get(), campo_telefone.get(), campo_endereco.get()))
    botao_cadastrar.place(x=100, y=100)


#editar cliente
def editar_cliente():
    #criando a janela
    janela_editar_cliente = tk.Tk()
    janela_editar_cliente.title("GCOS - Editar Cliente")
    janela_editar_cliente.geometry("300x300")
    #background cor branca
    janela_editar_cliente.configure(background="#ffffff")

    #carregando a lista de clientes
    lista_clientes = []
    #conectando ao banco de dados
    conn = sql.connect("data.db")
    #criando o cursor
    cursor = conn.cursor()
    #buscando os dados na tabela clientes
    cursor.execute("SELECT nome FROM clientes")
    #pegando os dados
    dados = cursor.fetchall()
    #fechando a conexão
    conn.close()
    #adicionando os dados na lista
    for dado in dados:
        lista_clientes.append(dado[0])

    #disponibilizando a lista de clientes no combobox organizando por ordem alfabética
    combobox_clientes = ttk.Combobox(janela_editar_cliente, values=sorted(lista_clientes))
    combobox_clientes.place(x=10, y=10)

    #criando os labels
    label_nome = tk.Label(janela_editar_cliente, text="Nome", bg="#ffffff")
    label_nome.place(x=10, y=40)

    label_telefone = tk.Label(janela_editar_cliente, text="Telefone", bg="#ffffff")
    label_telefone.place(x=10, y=70)

    label_endereco = tk.Label(janela_editar_cliente, text="Endereço", bg="#ffffff")
    label_endereco.place(x=10, y=100)

    label_id = tk.Label(janela_editar_cliente, text="ID", bg="#ffffff")
    label_id.place(x=10, y=130)

    label_info = tk.Label(janela_editar_cliente, text="", bg="#ffffff")
    label_info.place(x=10, y=180)


    #criando os campos de texto
    campo_nome = tk.Entry(janela_editar_cliente)
    campo_nome.place(x=100, y=40)

    campo_telefone = tk.Entry(janela_editar_cliente)
    campo_telefone.place(x=100, y=70)

    campo_endereco = tk.Entry(janela_editar_cliente)
    campo_endereco.place(x=100, y=100)

    campo_id = tk.Label(janela_editar_cliente)
    campo_id.place(x=100, y=130)

    #criando o botão de salvar alterações
    botao_editar = tk.Button(janela_editar_cliente, text="Salvar Alterações", command=lambda: editar_cliente_bd(campo_nome.get(), campo_telefone.get(), campo_endereco.get(), campo_id["text"]))
    botao_editar.place(x=100, y=160)

        #função para selecionar o cliente
    def selecionar_cliente(event):
        #pegando o nome do cliente selecionado
        nome_cliente = combobox_clientes.get()
        #conectando ao banco de dados
        conn = sql.connect("data.db")
        #criando o cursor
        cursor = conn.cursor()
        #buscando os dados na tabela clientes
        cursor.execute("SELECT * FROM clientes WHERE nome = ?", (nome_cliente,))
        #pegando os dados
        dados = cursor.fetchall()
        #fechando a conexão
        conn.close()
        #pegando os dados do cliente
        nome_cliente_atual = dados[0][1]
        telefone_cliente_atual = dados[0][2]
        endereco_cliente_atual = dados[0][3]
        id_cliente_atual = dados[0][0]
        #limpando os campos de texto
        campo_nome.delete(0, tk.END)
        campo_telefone.delete(0, tk.END)
        campo_endereco.delete(0, tk.END)
        campo_id["text"] = []
        #mostrando o nome do cliente no campo de texto
        campo_nome.insert(0, nome_cliente_atual)
        #mostrando o telefone do cliente no campo de texto
        campo_telefone.insert(0, telefone_cliente_atual)
        #mostrando o endereço do cliente no campo de texto
        campo_endereco.insert(0, endereco_cliente_atual)
        #mostrando o id do cliente no campo de texto
        campo_id["text"] = id_cliente_atual
        return id_cliente_atual
    
    #quando o usuário selecionar um cliente, chama a função selecionar_cliente
    combobox_clientes.bind("<<ComboboxSelected>>", selecionar_cliente)

    #função para editar o cliente no banco de dados
    def editar_cliente_bd(nome_modificado, telefone_modificado, endereco_modificado, id_cliente_atual):
        #conectando ao banco de dados
        conn = sql.connect("data.db")
        #criando o cursor
        cursor = conn.cursor()
        #atualizando os dados do cliente
        cursor.execute("UPDATE clientes SET nome = ?, telefone = ?, endereco = ? WHERE id = ?", (nome_modificado, telefone_modificado, endereco_modificado, id_cliente_atual))
        #salvando as alterações
        conn.commit()
        #fechando a conexão
        conn.close()
        #mostrando a mensagem de sucesso
        label_info["text"] = "Cliente editado com sucesso!"
        #atualizando a tela
        janela_editar_cliente.update()
        #esperando 1 segundos
        time.sleep(1)
        #fechando a janela
        janela_editar_cliente.destroy()

    #mostrando a janela
    janela_editar_cliente.mainloop()



        
    



#criando a janela
janela = tk.Tk()
janela.title("GCOS - Gerenciamento de Clientes e Ordens de Serviço")
janela.geometry("800x600")
#background cor branca
janela.configure(background="#ffffff")

#criando o menu
menu = tk.Menu(janela)
janela.config(menu=menu)

#criando os submenus
submenu = tk.Menu(menu)
menu.add_cascade(label="Clientes", menu=submenu)
#se clicar no botão cadastrar, chama a função cadastrar_cliente
submenu.add_command(label="Cadastrar", command=cadastrar_cliente)
submenu.add_command(label="Listar")
submenu.add_command(label="Editar", command=editar_cliente)
submenu.add_command(label="Excluir")

submenu = tk.Menu(menu)
menu.add_cascade(label="Ordens de Serviço", menu=submenu)
submenu.add_command(label="Cadastrar")
submenu.add_command(label="Listar")
submenu.add_command(label="Editar")
submenu.add_command(label="Excluir")

#rodando a janela
janela.mainloop()
