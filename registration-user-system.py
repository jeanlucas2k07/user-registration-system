from customtkinter import *
import sqlite3 as sq
from PIL import Image
from tkinter import messagebox

class Banco():
    def conn_db(self):
        self.conn = sq.connect('acessos.db')
        self.cursor = self.conn.cursor()
        print('Banco conectado com sucesso!')

    def desconn_db(self):
        self.conn.close()
        print('Banco desconectado com sucesso!')

    def criar_tabela(self):
        self.conn_db()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS acessos (
                'email' text not null,
                'senha' text not null
            )
            ''')

        self.conn.commit()
        print('Tabela criada com sucesso!')
        self.desconn_db()

    def cadastro(self):
        self.email_cadastro = self.email_cad.get()
        self.senha_cadastro = self.senha_cad.get()

        self.conn_db()

        self.cursor.execute("INSERT INTO acessos VALUES (?, ?)",
                            (self.email_cadastro, self.senha_cadastro))

        a = 0

        for i in self.senha_cadastro:
            a += 1
        print(a)

        try:
            if a < 5:
                messagebox.showinfo(title='Login', message='Por favor, faça uma senha com mais de cinco caracteres.')
            else:
                self.conn.commit()
                messagebox.showinfo(title='Login', message='Cadastro efetuado com sucesso!\n'
                                                           ' Volte à tela de login para efetuá-lo')
                self.desconn_db()
                self.limpa_cadastro()
            if self.senha_cadastro == '' or self.email_cadastro == '':
                messagebox.showinfo(title='Login', message='Percebi que alguns espaços estão vazios. Preencha TODOS!')
            else:
                self.conn.commit()
                messagebox.showinfo(title='Login', message='Cadastro efetuado com sucesso!\n'
                                                           ' Volte à tela de login para efetuá-lo')
                self.desconn_db()
                self.limpa_cadastro()
        except:
            pass

    def login(self):
        self.email_log = self.email.get()
        self.senha_log = self.senha.get()

        self.conn_db()
        self.cursor.execute('''SELECT * FROM acessos WHERE email = ? AND senha = ?''',
                            (self.email_log, self.senha_log))

        self.resultado = self.cursor.fetchone()
        print('Validando dados')
        self.desconn_db()

        if self.resultado:
            messagebox.showinfo(title='Login', message='Login efetuado com sucesso.')
        else:
            messagebox.showinfo(title='Login', message='Ocorreu um erro, por favor, tente novamente.'
                                                       '\nCaso não tenha cadastro, cadastre-se!')

class app(CTk, Banco):
    def __init__(self):
        super().__init__()
        self.criar_tabela()
        self.janela_config()
        self.janela_login()

    def janela_config(self):
        self.geometry("700x400")
        self.resizable(width=False, height=False)

    def janela_login(self):
        self.title('Login de Usuário')
        self.frame_login = CTkFrame(self, width=300, height=385, corner_radius=30)
        self.frame_login.place(x=394, y=8)

        self.img_logo = os.path.join(os.path.dirname(__file__),
                                     r'images\img_logo.png')
        self.img_logo = CTkImage(light_image=Image.open(self.img_logo), size=(160, 160))
        self.img_logo = CTkLabel(self.frame_login, text='', image=self.img_logo)
        self.img_logo.place(relx=0.5, rely=0.12, anchor=CENTER)

        self.email = CTkEntry(master=self.frame_login, placeholder_text='Seu e-mail', width=200, height=40,
                              corner_radius=40, font=('archivo.ttf', 14))
        self.senha = CTkEntry(master=self.frame_login, placeholder_text='Sua senha', show='*', width=200,
                              height=40, corner_radius=40, font=('archivo.ttf', 14))

        check_box = CTkCheckBox(master=self.frame_login, text="Lembrar login", font=('archivo.ttf', 14),
                                corner_radius=30)
        check_box.place(relx=0.37, rely=0.55, anchor=CENTER)

        self.email.place(relx=0.5, rely=0.31, anchor=CENTER)
        self.senha.place(relx=0.5, rely=0.437, anchor=CENTER)

        self.label1 = CTkLabel(self, text="Faça login, ou cadastre-se, para acessar\n nossos serviços")
        self.label1.configure(font=('archivo.ttf', 17))
        self.label1.grid(row=0, column=0, padx=5, pady=25)

        self.image = os.path.join(os.path.dirname(__file__),
                                  r'images\img_login.png')
        self.image = CTkImage(light_image=Image.open(self.image), size=(300, 300))
        self.image = CTkLabel(self, text="", image=self.image)
        self.image.grid(row=1, column=0, padx=50, pady=0)

        botao_login = CTkButton(master=self.frame_login, text='Fazer Login', command=self.login, width=200, height=40,
                                corner_radius=40, font=('archivo.ttf', 14))

        botao_login.place(relx=0.5, rely=0.67, anchor=CENTER)

        text_cad = CTkLabel(master=self.frame_login, text="Caso não tenha cadastro, cadastre-se.",
                            font=('archivo.ttf', 14))
        text_cad.place(relx=0.5, rely=0.77, anchor=CENTER)

        botao_cadastro = CTkButton(self.frame_login, text="Cadastrar-se", fg_color='green', command=self.janela_cad,
                                   hover_color="dark green", width=200, height=40, corner_radius=40,
                                   font=('archivo.ttf', 14))

        botao_cadastro.place(relx=0.5, rely=0.87, anchor=CENTER)

    def janela_cad(self):

        self.frame_login.pack_forget()
        self.title('Cadastro de usuário')

        self.frame_cad = CTkFrame(self, width=300, height=385, corner_radius=30)
        self.frame_cad.place(x=394, y=8)

        self.img_logo = os.path.join(os.path.dirname(__file__),
                                     r'images\img_logo.png')
        self.img_logo = CTkImage(light_image=Image.open(self.img_logo), size=(160, 160))
        self.img_logo = CTkLabel(self.frame_cad, text='', image=self.img_logo)
        self.img_logo.place(relx=0.5, rely=0.12, anchor=CENTER)

        self.email_cad = CTkEntry(master=self.frame_cad, placeholder_text='Seu e-mail', width=200, height=40,
                                  corner_radius=40,
                                  font=('archivo.ttf', 14))

        self.senha_cad = CTkEntry(master=self.frame_cad, placeholder_text='Sua senha', show='*', width=200, height=40,
                                  corner_radius=40, font=('archivo.ttf', 14))

        check_box = CTkCheckBox(master=self.frame_cad, text="Mostrar senha", font=('archivo.ttf', 14), corner_radius=30,
                                fg_color='green', hover_color='dark green')
        check_box.place(relx=0.37, rely=0.55, anchor=CENTER)

        self.email_cad.place(relx=0.5, rely=0.31, anchor=CENTER)
        self.senha_cad.place(relx=0.5, rely=0.437, anchor=CENTER)

        botao_cad = CTkButton(master=self.frame_cad, text='Finalizar cadastro', command=self.cadastro, width=200,
                              height=40,
                              corner_radius=40, font=('archivo.ttf', 14), fg_color='green', hover_color='dark green')
        botao_cad.place(relx=0.5, rely=0.66, anchor=CENTER)

        botao_voltar = CTkButton(master=self.frame_cad, text='Voltar ao login', command=self.janela_login, width=200,
                                 height=40, corner_radius=40, font=('archivo.ttf', 14), fg_color='#444',
                                 hover_color='#333')
        botao_voltar.place(relx=0.5, rely=0.79, anchor=CENTER)

if __name__ == "__main__":
    janela = app()
    janela.mainloop()