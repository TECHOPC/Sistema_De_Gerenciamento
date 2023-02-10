#programa de gerenciamento de clientes e ordens de serviço
#autor:leonardo da silva de jesus

#instalar o pandas e o tkinter para rodar o programa
#pip install pandas
#pip install tkinter

#bibliotecas
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

#listar cliente
def listar_clientes():
    #criando a janela
    janela_listar_clientes = tk.Tk()
    janela_listar_clientes.title("Listar Clientes")
    janela_listar_clientes.geometry("525x300")
    #background cor branca
    janela_listar_clientes.configure(background="#ffffff")


    #criando uma tabela para mostrar os clientes, com 4 colunas
    tabela_clientes = ttk.Treeview(janela_listar_clientes, columns=("id", "nome", "telefone", "endereco"))
    #definindo o tamanho das colunas
    tabela_clientes.column("#0", width=0)
    tabela_clientes.column("id", width=50)
    tabela_clientes.column("nome", width=150)
    tabela_clientes.column("telefone", width=150)
    tabela_clientes.column("endereco", width=150)
    #definindo o nome das colunas
    tabela_clientes.heading("#0", text="")
    tabela_clientes.heading("id", text="ID")
    tabela_clientes.heading("nome", text="Nome")
    tabela_clientes.heading("telefone", text="Telefone")
    tabela_clientes.heading("endereco", text="Endereço")
    #posicionando a tabela
    tabela_clientes.place(x=10, y=40)

    #função para mostrar os clientes na tabela
    def mostrar_clientes():
        #conectando ao banco de dados
        conn = sql.connect("data.db")
        #criando o cursor
        cursor = conn.cursor()
        #buscando os dados na tabela clientes
        cursor.execute("SELECT * FROM clientes")
        #pegando os dados
        dados = cursor.fetchall()
        #fechando a conexão
        conn.close()
        #limpando a tabela
        tabela_clientes.delete(*tabela_clientes.get_children())
        #mostrando os clientes na tabela
        for i in dados:
            tabela_clientes.insert("", tk.END, values=i)

    #mostrando os clientes na tabela
    mostrar_clientes()
           
#excluir cliente
def excluir_cliente():
    #editar cliente
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

    #criando o botão de excluir
    botao_editar = tk.Button(janela_editar_cliente, text="excluir", command=lambda: excluir_cliente_bd(campo_nome.get(), campo_telefone.get(), campo_endereco.get(), campo_id["text"]))
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

    #função para excluir o cliente
    def excluir_cliente_bd(nome, telefone, endereco, id):
        #conectando ao banco de dados
        conn = sql.connect("data.db")
        #criando o cursor
        cursor = conn.cursor()
        #buscando os dados na tabela clientes
        cursor.execute("DELETE FROM clientes WHERE id = ?", (id,))
        #salvando as alterações
        conn.commit()
        #fechando a conexão
        conn.close()
        #limpando os campos de texto
        campo_nome.delete(0, tk.END)
        campo_telefone.delete(0, tk.END)
        campo_endereco.delete(0, tk.END)
        campo_id["text"] = []
        #mostrando a mensagem de sucesso
        label_info["text"] = "Cliente excluído com sucesso!"

    #mostrando a janela
    janela_editar_cliente.mainloop()

#Cadastrar ordem de serviço
def cadastrar_ordem():
    #criando a janela
    janela_cadastrar_ordem = tk.Toplevel(janela)
    janela_cadastrar_ordem.title("GCOS - Cadastrar ordem de serviço")
    janela_cadastrar_ordem.geometry("300x300")
    #background cor branca
    janela_cadastrar_ordem.configure(background="#ffffff")

    #criando os labels
    label_cliente = tk.Label(janela_cadastrar_ordem, text="Cliente", bg="#ffffff")
    label_cliente.place(x=10, y=10)

    label_cliente_id = tk.Label(janela_cadastrar_ordem, text="ID", bg="#ffffff")
    label_cliente_id.place(x=10, y=40)

    label_descricao = tk.Label(janela_cadastrar_ordem, text="Descrição", bg="#ffffff")
    label_descricao.place(x=10, y=70)

    label_data = tk.Label(janela_cadastrar_ordem, text="Data", bg="#ffffff")
    label_data.place(x=10, y=130)

    label_info = tk.Label(janela_cadastrar_ordem, text="", bg="#ffffff")
    label_info.place(x=10, y=160)

    #criando os campos de texto
    #o campo de texto do cliente será um combobox
    combobox_clientes = ttk.Combobox(janela_cadastrar_ordem)
    combobox_clientes.place(x=100, y=10)
        
    #mostrando os nomes dos clientes no combobox
    def pegar_lista_clientes():
        #conectando ao banco de dados
        conn = sql.connect("data.db")
        #criando o cursor
        cursor = conn.cursor()
        #buscando os dados na tabela clientes
        cursor.execute("SELECT nome FROM clientes")
        #pegando os dados
        dados = cursor.fetchall()
        #buscando os dados na tabela id
        cursor.execute("SELECT id FROM clientes")
        #pegando os dados
        dados_id = cursor.fetchall()
        #fechando a conexão
        conn.close()
        #criando uma lista para armazenar os nomes dos clientes
        lista_clientes = []
        #criando uma lista para armazenar os ids dos clientes
        lista_id = []
        #adicionando os nomes dos clientes na lista
        for i in dados:
            lista_clientes.append(i[0])
        #adicionando os ids dos clientes na lista
        for i in dados_id:
            lista_id.append(i[0])
        #retornando a lista de clientes
        return lista_clientes, lista_id

    #pegando os dados dos clientes
    dados_clientes = pegar_lista_clientes()

    #função para preencher os campos de texto com os dados do cliente selecionado
    def selecionar_cliente(event):
        #pegando o nome do cliente selecionado
        nome_cliente = combobox_clientes.get()
        #pegando o id do cliente selecionado
        id_cliente = dados_clientes[1][dados_clientes[0].index(nome_cliente)]
        #mostrando o id do cliente no campo de texto
        campo_id["text"] = id_cliente

    #mostrando os nomes dos clientes no combobox
    combobox_clientes["values"] = dados_clientes[0]
    #chamando a função para preencher os campos de texto com os dados do cliente selecionado
    combobox_clientes.bind("<<ComboboxSelected>>", selecionar_cliente)
    
    campo_id = tk.Label(janela_cadastrar_ordem, text="", bg="#ffffff")
    campo_id.place(x=100, y=40)

    #mostrando o id do cliente no campo de texto
    campo_id["text"] = dados_clientes[1][0]

    #campo_descricao deve ser um Text, para que o usuário possa digitar mais de uma linha
    campo_descricao = tk.Text(janela_cadastrar_ordem, width=40, height=3)
    campo_descricao.place(x=100, y=70)

    #campo_data deve ser um Entry, para que o usuário possa digitar a data
    campo_data = tk.Entry(janela_cadastrar_ordem)
    campo_data.place(x=100, y=130)

      #depois de apertar o botão de cadastrar fechar a janela depois de 1 segundo
    def botão_cadastrar_os():
        cadastrar_ordem_bd(combobox_clientes.get(), campo_descricao.get("1.0", tk.END), campo_data.get(), label_info)
        janela_cadastrar_ordem.after(1000, janela_cadastrar_ordem.destroy)

    #criando o botão de cadastrar
    botao_cadastrar = tk.Button(janela_cadastrar_ordem, text="Cadastrar", command=lambda: botão_cadastrar_os())
    botao_cadastrar.place(x=10, y=200)
 
    #função para cadastrar a ordem de serviço no banco de dados
    def cadastrar_ordem_bd(nome_cliente, descricao, data, label_info):
        #conectando ao banco de dados
        conn = sql.connect("data.db")
        #criando o cursor
        cursor = conn.cursor()
        #buscando o id do cliente
        cursor.execute("SELECT id FROM clientes WHERE nome = ?", (nome_cliente,))
        #pegando o id
        id_cliente = cursor.fetchone()[0]
        #inserindo os dados na tabela ordens
        cursor.execute("INSERT INTO ordens VALUES (NULL, ?, ?, ?, ?)", (id_cliente, descricao, data, "Em aberto"))
        #salvando as alterações
        conn.commit()
        #fechando a conexão
        conn.close()
        #mostrando uma mensagem de sucesso
        label_info["text"] = "Ordem de serviço cadastrada com sucesso!"
    
    #mostrando a janela
    janela_cadastrar_ordem.mainloop()

#função para listar as ordens de serviço
def listar_ordens():
    #criando a janela
    janela_listar_ordens = tk.Toplevel()
    janela_listar_ordens.title("Listar Ordens de Serviço")
    janela_listar_ordens.geometry("800x600")
    janela_listar_ordens.configure(background="#ffffff")

    #cria tabela para mostrar os dados
    tabela = ttk.Treeview(janela_listar_ordens, columns=("id", "cliente", "descricao", "data", "status"))
    #define o tamanho das colunas
    tabela.column("#0", width=0)
    tabela.column("id", width=50)
    tabela.column("cliente", width=200)
    tabela.column("descricao", width=200)
    tabela.column("data", width=100)
    tabela.column("status", width=100)
    #define o nome das colunas
    tabela.heading("#0", text="")
    tabela.heading("id", text="ID")
    tabela.heading("cliente", text="Cliente")
    tabela.heading("descricao", text="Descrição")
    tabela.heading("data", text="Data")
    tabela.heading("status", text="Status")
    #mostra a tabela
    tabela.place(x=10, y=10)

    #função para pegar os dados das ordens de serviço do banco de dados
    def pegar_lista_ordens():
        #conectando ao banco de dados
        conn = sql.connect("data.db")
        #criando o cursor
        cursor = conn.cursor()
        #buscando os dados das ordens de serviço
        cursor.execute("SELECT ordens.id, clientes.nome, ordens.descricao, ordens.data, ordens.status FROM ordens INNER JOIN clientes ON ordens.id_cliente = clientes.id")
        #pegando os dados
        dados = cursor.fetchall()
        #fechando a conexão
        conn.close()
        #retornando os dados
        return dados
    
    #pegando os dados das ordens de serviço
    dados_ordens = pegar_lista_ordens()
    #inserindo os dados na tabela
    for ordem in dados_ordens:
        tabela.insert("", tk.END, values=ordem)

    #mostrando a janela
    janela_listar_ordens.mainloop()

    




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
submenu.add_command(label="Cadastrar", command=cadastrar_cliente)
submenu.add_command(label="Listar", command=listar_clientes)
submenu.add_command(label="Editar", command=editar_cliente)
submenu.add_command(label="Excluir", command=excluir_cliente)

submenu = tk.Menu(menu)
menu.add_cascade(label="Ordens de Serviço", menu=submenu)
submenu.add_command(label="Cadastrar", command=cadastrar_ordem)
submenu.add_command(label="Listar", command=listar_ordens)
submenu.add_command(label="Editar")
submenu.add_command(label="Excluir")

#rodando a janela
janela.mainloop()