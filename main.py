#programa de gerenciamento de clientes e ordens de serviço
#autor:leonardo da silva de jesus

import pandas as pd
import tkinter as tk
from tkinter import ttk
import time

#verificando se o arquivo existe
try:
    df = pd.read_csv("clientes.csv")
except:
    df = pd.DataFrame(columns=["id","nome","telefone","endereco"])
    df.to_csv("clientes.csv", index=False)

try:
    df = pd.read_csv("ordens.csv")
except:
    df = pd.DataFrame(columns=["id","cliente","data","descricao"])
    df.to_csv("ordens.csv", index=False)

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
        #lendo o arquivo
        df = pd.read_csv("clientes.csv")
        #pegando o maior id
        last_id = df["id"].max()
        #criando o id
        id = last_id + 1
        #criando o dicionario
        dicionario = {"id":id, "nome":nome, "telefone":telefone, "endereco":endereco}
        #checando se o nome do cliente já existe
        if nome in df["nome"].values:
            #mostrando a mensagem de erro
            label_confirmacao["text"] = "Cliente já cadastrado!"
            #atualizando a janela
            janela_cadastrar_cliente.update()
            #esperando 1 segundos
            time.sleep(1)
            #fechando a janela
            janela_cadastrar_cliente.destroy()
            return
        #adicionando o dicionario no dataframe usando o concat
        df = pd.concat([df, pd.DataFrame([dicionario])], ignore_index=True)
        #salvando o dataframe no arquivo
        df.to_csv("clientes.csv", index=False)
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

    #carregando o arquivo de clientes
    df = pd.read_csv("clientes.csv")
    #criando a lista de clientes
    lista_clientes = []
    lista_clientesid = []
    #percorrendo o dataframe
    for i in range(len(df)):
        #adicionando o nome do cliente na lista e armazenando o id
        lista_clientes.append(df.loc[i, "nome"])
        lista_clientesid.append(df.loc[i, "id"])


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
        #lendo o arquivo
        df = pd.read_csv("clientes.csv")
        #filtrando o dataframe pelo nome do cliente
        df = df[df["nome"] == nome_cliente]
        #pegando o nome do cliente
        nome_cliente_atual = df.loc[df.index[0], "nome"]
        #pegando o telefone do cliente
        telefone_cliente_atual = df.loc[df.index[0], "telefone"]
        #pegando o endereço do cliente
        endereco_cliente_atual = df.loc[df.index[0], "endereco"]
        #pegando o id do cliente
        id_cliente_atual = df.loc[df.index[0], "id"]
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
    
    #quando o usuário selecionar um cliente, chama a função selecionar_cliente
    combobox_clientes.bind("<<ComboboxSelected>>", selecionar_cliente)

    #função para editar o cliente no banco de dados
    def editar_cliente_bd(nome_modificado, telefone_modificado, endereco_modificado, id_modificado):
        #lendo o arquivo
        df = pd.read_csv("clientes.csv")
        #procurando o cliente pelo id
        df.loc[df["id"] == int(id_modificado), "nome"] = nome_modificado
        df.loc[df["id"] == int(id_modificado), "telefone"] = telefone_modificado
        df.loc[df["id"] == int(id_modificado), "endereco"] = endereco_modificado
        #salvando o arquivo
        df.to_csv("clientes.csv", index=False)
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
