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
import datetime

#criando o banco de dados clientes.db
conn = sql.connect("data.db")
#criando o cursor
cursor = conn.cursor()
#criando a tabela clientes
cursor.execute("CREATE TABLE IF NOT EXISTS clientes (id INTEGER PRIMARY KEY, nome TEXT, telefone TEXT, endereco TEXT)")
#criando a tabela ordens de serviço
cursor.execute("CREATE TABLE IF NOT EXISTS ordens (id INTEGER PRIMARY KEY, clienteid TEXT, nomecliente TEXT , data TEXT, descricao TEXT, valor TEXT, status TEXT)")
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
    #(id INTEGER PRIMARY KEY, clienteid TEXT, nomecliente TEXT , data TEXT, descricao TEXT, valor TEXT, status TEXT)
    label_cliente = tk.Label(janela_cadastrar_ordem, text="Cliente", bg="#ffffff")
    label_cliente.place(x=10, y=10)

    label_data = tk.Label(janela_cadastrar_ordem, text="Data", bg="#ffffff")
    label_data.place(x=10, y=40)

    label_descricao = tk.Label(janela_cadastrar_ordem, text="Descrição", bg="#ffffff")
    label_descricao.place(x=10, y=70)

    label_valor = tk.Label(janela_cadastrar_ordem, text="Valor", bg="#ffffff")
    label_valor.place(x=10, y=100)

    label_status = tk.Label(janela_cadastrar_ordem, text="Status", bg="#ffffff")
    label_status.place(x=10, y=130)

    #função para pegar os clientes do banco de dados
    def pegar_clientes():
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
        #criando uma lista para armazenar os nomes dos clientes
        lista_clientes = []
        lista_id = []
        #pegando os nomes dos clientes

        print(dados)

        for cliente in dados:
            lista_clientes.append(cliente[1])        
        return lista_clientes
    
    #criando os campos de texto
    #criando o combobox
    combobox_clientes = ttk.Combobox(janela_cadastrar_ordem, values=pegar_clientes())
    combobox_clientes.place(x=100, y=10)

    #criando o campo de texto para a data (dia/mês/ano) usando a data atual
    campo_data = tk.Entry(janela_cadastrar_ordem)
    campo_data.place(x=100, y=40)
    campo_data.insert(0, datetime.datetime.now().strftime("%d/%m/%Y"))

    #criando o campo de texto para a descrição
    #campo de texto com várias linhas
    campo_descricao = tk.Text(janela_cadastrar_ordem, width=30, height=5)
    campo_descricao.place(x=100, y=70)

    #criando o campo de texto para o valor
    #valor padrão 0 (zero) com duas casas decimais, formato monetário
    campo_valor = tk.Entry(janela_cadastrar_ordem)
    campo_valor.place(x=100, y=100)
    campo_valor.insert(0, "0,00")

    #criando o campo de texto para o status
    #valor padrão "Aguardando"
    campo_status = tk.Entry(janela_cadastrar_ordem)
    campo_status.place(x=100, y=130)
    campo_status.insert(0, "Aguardando")

    #criando o label para mostrar as mensagens de erro
    label_info = tk.Label(janela_cadastrar_ordem, text="", bg="#ffffff")
    label_info.place(x=10, y=160)

    #função para cadastrar a ordem de serviço
    def cadastrar_ordem_bd():
        #pegando os dados dos campos de texto
        cliente = combobox_clientes.get()
        #pega o index do cliente selecionado
        index = combobox_clientes.current()
        data = campo_data.get()
        descricao = campo_descricao.get("1.0", tk.END)
        valor = campo_valor.get()
        status = campo_status.get()
        #verificando se os campos estão vazios
        if cliente == "" or data == "" or descricao == "" or valor == "" or status == "":
            label_info["text"] = "Preencha todos os campos!"
        else:
            #conectando ao banco de dados
            conn = sql.connect("data.db")
            #criando o cursor
            cursor = conn.cursor()
            #buscando os dados na tabela clientes
            cursor.execute("INSERT INTO ordens (clienteid, nomecliente, data, descricao, valor, status) VALUES (?, ?, ?, ?, ?, ?)", (index, cliente, data, descricao, valor, status))
            #salvando as alterações
            conn.commit()
            #fechando a conexão
            conn.close()
            #limpando os campos de texto
            combobox_clientes.delete(0, tk.END)
            campo_data.delete(0, tk.END)
            campo_descricao.delete("1.0", tk.END)
            campo_valor.delete(0, tk.END)
            campo_status.delete(0, tk.END)
            #mostrando a mensagem de sucesso
            label_info["text"] = "Ordem de serviço cadastrada com sucesso!"
            #aguardando 1 segundo
            time.sleep(1)
            #fechando a janela
            janela_cadastrar_ordem.destroy()

    #criando o botão para cadastrar a ordem de serviço
    botao_cadastrar = tk.Button(janela_cadastrar_ordem, text="Cadastrar", command=cadastrar_ordem_bd)
    botao_cadastrar.place(x=10, y=190)

#função para listar as ordens de serviço
def listar_ordens():
    #criando a janela
    janela_listar_ordens = tk.Toplevel()
    janela_listar_ordens.title("GCOS - Listar e Editar Ordens de Serviço")
    janela_listar_ordens.geometry("800x650")
    janela_listar_ordens.configure(background="#ffffff")

    #criando o label para mostrar as mensagens de erro
    label_info = tk.Label(janela_listar_ordens, text="", bg="#ffffff")
    label_info.place(x=10, y=10)

    #função para pegar os dados do banco de dados
    def pegar_ordens():
        #conectando ao banco de dados
        conn = sql.connect("data.db")
        #criando o cursor
        cursor = conn.cursor()
        #buscando os dados na tabela ordens
        cursor.execute("SELECT * FROM ordens")
        #pegando os dados
        dados = cursor.fetchall()
        #fechando a conexão
        conn.close()
        #retornando os dados
        return dados

    #criando o Treeview
    treeview = ttk.Treeview(janela_listar_ordens, columns=("id", "clienteid", "nomecliente", "data", "descricao", "valor", "status"), show="headings")
    #criando as colunas
    treeview.column("id", width=50, minwidth=50, anchor=tk.CENTER)
    treeview.column("clienteid", width=50, minwidth=50, anchor=tk.CENTER)
    treeview.column("nomecliente", width=200, minwidth=200, anchor=tk.CENTER)
    treeview.column("data", width=100, minwidth=100, anchor=tk.CENTER)
    treeview.column("descricao", width=200, minwidth=200, anchor=tk.CENTER)
    treeview.column("valor", width=100, minwidth=100, anchor=tk.CENTER)
    treeview.column("status", width=100, minwidth=100, anchor=tk.CENTER)
    #criando os cabeçalhos
    treeview.heading("id", text="ID")
    treeview.heading("clienteid", text="Cliente ID")
    treeview.heading("nomecliente", text="Nome do Cliente")
    treeview.heading("data", text="Data")
    treeview.heading("descricao", text="Descrição")
    treeview.heading("valor", text="Valor")
    treeview.heading("status", text="Status")
    #posicionando o Treeview
    treeview.place(x=10, y=40)
    #pegando os dados do banco de dados
    dados = pegar_ordens()
    #inserindo os dados no Treeview
    for i in dados:
        treeview.insert("", tk.END, values=i)

    #editar ordem de serviço quando clicar duas vezes no item
    def editar_ordem(event):
        #pegando os dados da linha selecionada
        linha = treeview.selection()
        #pegando os dados da linha
        dados = treeview.item(linha, "values")
        #pegando os dados da linha
        id = dados[0]
        clienteid = dados[1]
        nomecliente = dados[2]
        data = dados[3]
        descricao = dados[4]
        valor = dados[5]
        status = dados[6]
        #criando a janela
        janela_editar_ordem = tk.Toplevel()
        janela_editar_ordem.title("GCOS - Editar Ordem de Serviço")
        janela_editar_ordem.geometry("800x650")
        janela_editar_ordem.configure(background="#ffffff")
        #criando o label para mostrar as mensagens de erro
        label_info = tk.Label(janela_editar_ordem, text="", bg="#ffffff")
        label_info.place(x=10, y=10)
        #criando o label para o campo id
        label_id = tk.Label(janela_editar_ordem, text="ID:", bg="#ffffff")
        label_id.place(x=10, y=10)
        #criando o campo id
        campo_id = tk.Entry(janela_editar_ordem)
        campo_id.place(x=10, y=30)
        campo_id.insert(0, id)
        #criando o label para o campo clienteid
        label_clienteid = tk.Label(janela_editar_ordem, text="Cliente ID:", bg="#ffffff")
        label_clienteid.place(x=10, y=60)
        #criando o campo clienteid
        campo_clienteid = tk.Entry(janela_editar_ordem)
        campo_clienteid.place(x=10, y=80)
        campo_clienteid.insert(0, clienteid)
        #criando o label para o campo nomecliente
        label_nomecliente = tk.Label(janela_editar_ordem, text="Nome do Cliente:", bg="#ffffff")
        label_nomecliente.place(x=10, y=110)
        #criando o campo nomecliente
        campo_nomecliente = tk.Entry(janela_editar_ordem)
        campo_nomecliente.place(x=10, y=130)
        campo_nomecliente.insert(0, nomecliente)
        #criando o label para o campo data
        label_data = tk.Label(janela_editar_ordem, text="Data:", bg="#ffffff")
        label_data.place(x=10, y=160)
        #criando o campo data
        campo_data = tk.Entry(janela_editar_ordem)
        campo_data.place(x=10, y=180)
        campo_data.insert(0, data)
        #criando o label para o campo descricao
        label_descricao = tk.Label(janela_editar_ordem, text="Descrição:", bg="#ffffff")
        label_descricao.place(x=10, y=210)
        #criando o campo descricao
        campo_descricao = tk.Entry(janela_editar_ordem)
        campo_descricao.place(x=10, y=230)
        campo_descricao.insert(0, descricao)
        #criando o label para o campo valor
        label_valor = tk.Label(janela_editar_ordem, text="Valor:", bg="#ffffff")
        label_valor.place(x=10, y=260)
        #criando o campo valor
        campo_valor = tk.Entry(janela_editar_ordem)
        campo_valor.place(x=10, y=280)
        campo_valor.insert(0, valor)
        #criando o label para o campo status
        label_status = tk.Label(janela_editar_ordem, text="Status:", bg="#ffffff")
        label_status.place(x=10, y=310)
        #criando o campo status
        campo_status = tk.Entry(janela_editar_ordem)
        campo_status.place(x=10, y=330)
        campo_status.insert(0, status)
    

        
        #função para salvar a ordem editada
        def salvar_ordem_editada(clienteid, nomecliente, data, descricao, valor, status, id):
            #verificando se os campos estão vazios
            if id == "" or clienteid == "" or nomecliente == "" or data == "" or descricao == "" or valor == "" or status == "":
                label_info["text"] = "Preencha todos os campos!"
            else:
                #conectando ao banco de dados
                conn = sql.connect("data.db")
                #criando o cursor
                cursor = conn.cursor()
                #buscando os dados na tabela ordens
                cursor.execute("UPDATE ordens SET clienteid=?, nomecliente=?, data=?, descricao=?, valor=?, status=? WHERE id=?", (clienteid, nomecliente, data, descricao, valor, status, id))
                #salvando as alterações
                conn.commit()
                #fechando a conexão
                conn.close()
                #mostrando a mensagem de sucesso
                label_info["text"] = "Ordem de serviço editada com sucesso!"
                #aguardando 1 segundo
                time.sleep(1)
                #fechando a janela
                janela_editar_ordem.destroy()
                #atualizando os dados
                janela_listar_ordens.destroy()
                listar_ordens()
        #criando o botão para salvar
        botao_salvar = tk.Button(janela_editar_ordem, text="Salvar", command=lambda: salvar_ordem_editada(campo_clienteid.get(), campo_nomecliente.get(), campo_data.get(), campo_descricao.get(), campo_valor.get(), campo_status.get(), campo_id.get()))
        botao_salvar.place(x=10, y=450)


    #chamar a função editar_ordem quando clicar duas vezes no item
    treeview.bind("<Double-1>", editar_ordem)





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
submenu.add_command(label="Listar e Editar", command=listar_ordens)
submenu.add_command(label="Excluir")

#rodando a janela
janela.mainloop()