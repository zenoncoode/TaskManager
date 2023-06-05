import requests
import json
from functools import partial  # Importar a função partial
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen



link = "https://crazypython-1425d-default-rtdb.firebaseio.com/"

class GlobalVars:
    usuario_id = None
    tarefa_id = None
    password_id = None

Builder.load_string('''
<LoginScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: [40, 20, 40, 20]
        spacing: 0  # Espaçamento entre os widgets

        BoxLayout:
            orientation: 'vertical'
            size_hint: (None, None)
            size: (300, 150)
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}

            Label:
                text: 'Faça o Login'
                font_size: 24

        BoxLayout:
            orientation: 'vertical'
            size_hint: (None, None)
            size: (400, 170)
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            padding: [40, 20, 40, 20]
            spacing: 0  # Espaçamento entre os widgets
        
            TextInput:
                id: email_input
                hint_text: 'Email'
                multiline: False

            TextInput:
                id: password_input
                hint_text: 'Senha'
                multiline: False
                password: True

            Button:
                text: 'Entrar'
                size_hint: (None, None)
                size: (100, 50)
                background_color: 0, 0.5, 1, 1  # Cor de fundo azul (RGBA)
                on_press: root.login()

        BoxLayout:
            Label:
                text: '[color=0000FF][ref=Cadastro]Crie uma conta[/ref][/color]'
                font_size: 16
                markup: True
                on_ref_press: root.manager.current = 'cadastro'
                
        Label:
            id: login_status
            text: ''
            color: 1, 0, 0, 1  # Cor do texto vermelha

<CadastroScreen>:
    BoxLayout:
        orientation: 'vertical'
        size_hint: (None, None)
        size: (250, 250)
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}

        BoxLayout:
            orientation: 'vertical'
            size_hint: (None, None)
            size: (300, 170)
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        
            Label:
                text: 'Cadastre-se'
                font_size: 24

            
        BoxLayout:
            orientation: 'vertical'
            size_hint: (None, None)
            size: (300, 170)
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}

            TextInput:
                id: nome_input
                hint_text: 'Nome de Usuário'
                multiline: False

            TextInput:
                id: email_input
                hint_text: 'Email'
                multiline: False

            TextInput:
                id: password_input
                hint_text: 'Senha'
                multiline: False
                password: True

            Button:
                text: 'Cadastrar'
                size_hint: (None, None)
                size: (100, 50)
                background_color: 0, 0.5, 1, 1  # Cor de fundo azul (RGBA)
                on_press: root.cadastrar()

<PaginaInicialScreen>:
    
    BoxLayout:
        orientation: 'vertical'
        size_hint: (None, None)
        size: (200, 500)
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        spacing: 50

        Button:
            text: 'Cadastrar Tarefa'
            size_hint: (None, None)
            size: (200, 50)
            background_color: 0, 0.5, 1, 1  # Cor de fundo azul (RGBA)
            on_press: root.manager.current = 'cadastrar_tarefa'

        Button:
            text: 'Visualizar Tarefas'
            size_hint: (None, None)
            size: (200, 50)
            background_color: 0, 0.5, 1, 1  # Cor de fundo azul (RGBA)
            on_press: root.manager.current = 'visualizar_tarefas'

        Button:
            text: 'Histórico de Tarefas'
            size_hint: (None, None)
            size: (200, 50)
            background_color: 0, 0.5, 1, 1  # Cor de fundo azul (RGBA)
            on_press: root.manager.current = 'historico_tarefas'

        Button:
            text: 'Editar Dados de Acesso'
            size_hint: (None, None)
            size: (200, 50)
            background_color: 0, 0.5, 1, 1  # Cor de fundo azul (RGBA)
            on_press: root.manager.current = 'confirmar'

        Button:
            text: 'Sobre o App'
            size_hint: (None, None)
            size: (200, 50)
            background_color: 0, 0.5, 1, 1  # Cor de fundo azul (RGBA)
            on_press: root.manager.current = 'sobre'            

        BoxLayout:
            Label:
                text: '[color=0000FF][ref=Cadastro]Faça Logout[/ref][/color]'
                font_size: 16
                markup: True
                on_ref_press: root.logout()


<VisualizarTarefasScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: [40, 20, 40, 20]

        ScrollView:
            GridLayout:
                id: tarefas_grid
                cols: 1
                spacing: 10
                size_hint_y: None
                height: self.minimum_height

        Button:
            text: 'Voltar'
            size_hint: (None, None)
            size: (100, 50)
            background_color: 0, 0.5, 1, 1  # Cor de fundo azul (RGBA)
            on_press: root.manager.current = 'pagina_inicial'
                
<HistoricoTarefasScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: [40, 20, 40, 20]

        ScrollView:
            GridLayout:
                id: historico_grid
                cols: 1
                spacing: 10
                size_hint_y: None
                height: self.minimum_height

        Button:
            text: 'Voltar'
            size_hint: (None, None)
            size: (100, 50)
            background_color: 0, 0.5, 1, 1  # Cor de fundo azul (RGBA)
            on_press: root.manager.current = 'pagina_inicial'

<CadastrarTarefaScreen>:

    BoxLayout:
        orientation: 'vertical'
        size_hint: (None, None)
        size: (1000, 500)
        pos_hint: {'center_x': 0.5, 'center_y': 0.6}

            
        Label:
            text: 'Cadastro de Tarefa'
            font_size: 24

        
        BoxLayout:
            orientation: 'vertical'
            size_hint: (None, None)
            size: (400, 40)
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}

            TextInput:
                id: nome_tarefa_input
                hint_text: 'Nome da Tarefa'
                multiline: False

        BoxLayout:
            orientation: 'vertical'
            size_hint: (None, None)
            size: (400, 200)
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}

            TextInput:
                id: detalhes_tarefa_input
                hint_text: 'Detalhes da Tarefa'
                multiline: True

            Button:
                text: 'Cadastrar'
                size_hint: (None, None)
                size: (100, 50)
                background_color: 0, 0.5, 1, 1  # Cor de fundo azul (RGBA)
                on_press: root.cadastrar_tarefa()

            Button:
                text: 'Voltar'
                size_hint: (None, None)
                size: (100, 50)
                background_color: 0, 0.5, 1, 1  # Cor de fundo azul (RGBA)
                on_press: root.manager.current = 'pagina_inicial'

<EditarTarefaScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: [40, 20, 40, 20]

        Label:
            text: 'Editar Tarefa'
            font_size: 24

        BoxLayout:
            orientation: 'vertical'
            size_hint: (None, None)
            size: (400, 200)
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}

            TextInput:
                id: nome_tarefa_input
                hint_text: 'Nome da Tarefa'
                multiline: False

            TextInput:
                id: detalhes_tarefa_input
                hint_text: 'Detalhes da Tarefa'
                multiline: True

            Button:
                text: 'Editar'
                size_hint: (None, None)
                size: (100, 50)
                background_color: 0, 0.5, 1, 1  # Cor de fundo azul (RGBA)
                on_press: root.editar_tarefa()  

            Button:
                text: 'Voltar'
                size_hint: (None, None)
                size: (100, 50)
                background_color: 0, 0.5, 1, 1  # Cor de fundo azul (RGBA)
                on_press: root.manager.current = 'visualizar_tarefas'

<ConfirmarScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: [40, 20, 40, 20]
        spacing: 0  # Espaçamento entre os widgets

        BoxLayout:
            orientation: 'vertical'
            size_hint: (None, None)
            size: (300, 150)
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}

            Label:
                text: 'Confirmação com Senha'
                font_size: 24

        BoxLayout:
            orientation: 'vertical'
            size_hint: (None, None)
            size: (400, 140)
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            padding: [40, 20, 40, 20]
            spacing: 0  # Espaçamento entre os widgets

            TextInput:
                id: password_input
                hint_text: 'Senha'
                multiline: False
                password: True

            Button:
                text: 'Continuar'
                size_hint: (None, None)
                size: (100, 50)
                background_color: 0, 0.5, 1, 1  # Cor de fundo azul (RGBA)
                on_press: root.confirmar()
                
        Label:
            id: senha_status
            text: ''
            color: 1, 0, 0, 1  # Cor do texto vermelha


<EditarUsuarioScreen>:
    BoxLayout:
        orientation: 'vertical'
        size_hint: (None, None)
        size: (250, 250)
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}

        BoxLayout:
            orientation: 'vertical'
            size_hint: (None, None)
            size: (300, 170)
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        
            Label:
                text: 'Editar Dados'
                font_size: 24

            
        BoxLayout:
            orientation: 'vertical'
            size_hint: (None, None)
            size: (300, 210)
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}

            TextInput:
                id: nome_input
                hint_text: 'Nome de Usuário'
                multiline: False

            TextInput:
                id: email_input
                hint_text: 'Email'
                multiline: False

            TextInput:
                id: password_input
                hint_text: 'Senha'
                multiline: False
                password: True

            Button:
                text: 'Confirmar'
                size_hint: (None, None)
                size: (100, 50)
                background_color: 0, 0.5, 1, 1  # Cor de fundo azul (RGBA)
                on_press: root.editar()

            Button:
                text: 'Voltar'
                size_hint: (None, None)
                size: (100, 50)
                background_color: 0, 0.5, 1, 1  # Cor de fundo azul (RGBA)
                on_press: root.manager.current = 'pagina_inicial'


<SobreScreen>
    BoxLayout:
        orientation: 'vertical'
        size_hint: (None, None)
        size: (250, 250)
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}

        Label:
            font_size: 16
            text: 'Esse app tem como objetivo principal ajudar o usuário a gerenciar suas tarefas diárias.'
        
        Label:
            font_size: 16
            text: 'Foi desenvolvido por Noah Vinicius Aguiar Moura dos Santos.'
        
        Label:
            font_size: 16
            text: 'O desenvolvedor espera receber pontos suficientes para se formar na faculdade'
        Button:
            text: 'Voltar'
            size_hint: (None, None)
            size: (100, 50)
            background_color: 0, 0.5, 1, 1  # Cor de fundo azul (RGBA)
            on_press: root.manager.current = 'pagina_inicial'
                                
''')


class LoginScreen(Screen):
    def login(self):
        email = self.ids.email_input.text
        password = self.ids.password_input.text

        requisicao = requests.get(f'{link}Usuarios.json')
        usuarios = requisicao.json()

        for usuario_id, usuario in usuarios.items():
            if 'Email' in usuario and 'Senha' in usuario:
                if usuario['Email'].lower() == email.lower() and usuario['Senha'] == password:
                    print("Login realizado com sucesso!")
                    print("ID do usuário:", usuario_id) #exportar essa variavel para ser vista globalmente

                    GlobalVars.usuario_id = usuario_id
                    GlobalVars.password_id = password
                    self.manager.switch_to(self.manager.get_screen('pagina_inicial'))
                    return

        self.ids.login_status.text = 'Credenciais inválidas.'

        



class CadastroScreen(Screen):
    def cadastrar(self):
        email = self.ids.email_input.text
        senha = self.ids.password_input.text
        nome_usuario = self.ids.nome_input.text

        dados_cadastro = {'Nome de usuário': nome_usuario, 'Email': email, 'Senha': senha}

        requisicao = requests.post(f'{link}Usuarios/.json', data=json.dumps(dados_cadastro))  # criar um novo usuário
        if requisicao.status_code == 200:
            print("Cadastro realizado com sucesso!")
            self.manager.switch_to(self.manager.get_screen('login'))  # Mudar para a tela de login

        else:
            print("Erro ao cadastrar usuário.")



class CadastrarTarefaScreen(Screen):
    def cadastrar_tarefa(self):
        nome_tarefa = self.ids.nome_tarefa_input.text
        detalhes_tarefa = self.ids.detalhes_tarefa_input.text

        dados_tarefa = {'Nome': nome_tarefa, 'Detalhes': detalhes_tarefa}
        usuario_id = GlobalVars.usuario_id

        requisicao = requests.post(f'{link}Usuarios/{usuario_id}/Tarefas/Visualizar/.json', json=dados_tarefa)
        if requisicao.status_code == 200:
            print("Tarefa cadastrada com sucesso!")
            self.manager.current = 'pagina_inicial'  # Mudar para a tela de página inicial
        else:
            print("Erro ao cadastrar tarefa.")


class VisualizarTarefasScreen(Screen):

    def on_enter(self):
        self.carregar_tarefas()
    
    def carregar_tarefas(self):
        usuario_id = GlobalVars.usuario_id
        requisicao = requests.get(f'{link}Usuarios/{usuario_id}/Tarefas/Visualizar/.json')
        tarefas = json.loads(requisicao.content.decode())

        tarefas_grid = self.ids.tarefas_grid
        tarefas_grid.clear_widgets()

        for tarefa_id, tarefa in tarefas.items():
            nome_tarefa = tarefa['Nome']
            detalhes_tarefa = tarefa['Detalhes']

            tarefa_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=40)

            tarefa_label = Label(text=f'Nome: {nome_tarefa}\nDetalhes: {detalhes_tarefa}', size_hint=(0.7, None), height=40)
            tarefa_layout.add_widget(tarefa_label)

            botao_feito = Button(text='Feito', size_hint=(0.3, None), height=40)
            botao_feito.bind(on_press=partial(self.check_tarefa, tarefa_id))
            tarefa_layout.add_widget(botao_feito)

            botao_editar = Button(text='Editar', size_hint=(0.3, None), height=40)
            botao_editar.bind(on_press=lambda _, tarefa_id=tarefa_id: (setattr(GlobalVars, 'tarefa_id', tarefa_id), self.editar_tarefa(tarefa_id)))
            tarefa_layout.add_widget(botao_editar)

            tarefas_grid.add_widget(tarefa_layout)

    def check_tarefa(self, tarefa_id, *args):
        usuario_id = GlobalVars.usuario_id
        requisicao = requests.patch(f'{link}Usuarios/{usuario_id}/Tarefas/Visualizar/{tarefa_id}.json', json={'Check': True})
        
        if requisicao.status_code == 200:
            self.mover_tarefa(tarefa_id)
        else:
            print("Erro ao marcar tarefa como concluída.")

    def mover_tarefa(self, tarefa_id, *args):
        usuario_id = GlobalVars.usuario_id
        tarefa_url = f'{link}Usuarios/{usuario_id}/Tarefas/Visualizar/{tarefa_id}.json'
        historico_url = f'{link}Usuarios/{usuario_id}/Tarefas/Historico/{tarefa_id}.json'

        # Obter os dados da tarefa atual
        requisicao = requests.get(tarefa_url)
        tarefa = requisicao.json()

        # Adicionar a tarefa ao histórico
        requisicao = requests.put(historico_url, json=tarefa)

        if requisicao.status_code == 200:
            # Remover a tarefa da lista atual
            requisicao = requests.delete(tarefa_url)

            if requisicao.status_code == 200:
                self.carregar_tarefas()
                self.manager.get_screen('historico_tarefas').carregar_historico()
                self.manager.current = 'historico_tarefas'  # Transição para a tela de histórico
            else:
                print("Erro ao remover tarefa da lista atual.")
        else:
            print("Erro ao mover tarefa para o histórico.")

    def editar_tarefa(self, tarefa_id):
        self.manager.current = 'editar_tarefa'



class HistoricoTarefasScreen(Screen):

    def on_enter(self):
        self.carregar_historico()

    def carregar_historico(self):
        usuario_id = GlobalVars.usuario_id

        requisicao = requests.get(f'{link}Usuarios/{usuario_id}/Tarefas/Historico/.json')
        tarefas = json.loads(requisicao.content.decode())

        historico_grid = self.ids.historico_grid
        historico_grid.clear_widgets()

        for tarefa_id, tarefa in tarefas.items():
            nome_tarefa = tarefa['Nome']
            detalhes_tarefa = tarefa['Detalhes']


            tarefa_label = Label(text=f'Tarefa: {nome_tarefa}\nDetalhes: {detalhes_tarefa}', size_hint=(1, None), height=100)
            historico_grid.add_widget(tarefa_label)


class EditarTarefaScreen(Screen):
    def editar_tarefa(self):
        print(GlobalVars.tarefa_id)
        nome_tarefa = self.ids.nome_tarefa_input.text
        detalhes_tarefa = self.ids.detalhes_tarefa_input.text
        tarefa_id = GlobalVars.tarefa_id  # Obter o ID da tarefa

        # Atualizar os dados da tarefa
        usuario_id = GlobalVars.usuario_id
        requisicao = requests.patch(f'{link}Usuarios/{usuario_id}/Tarefas/Visualizar/{tarefa_id}.json', json={'Nome': nome_tarefa, 'Detalhes': detalhes_tarefa})

        if requisicao.status_code == 200:
            print("Tarefa editada com sucesso!")
            self.manager.current = 'visualizar_tarefas'  # Voltar para a tela de visualização de tarefas
        else:
            print("Erro ao editar tarefa.")

class ConfirmarScreen(Screen):
    def confirmar(self):
        password = self.ids.password_input.text

        if GlobalVars.password_id == password:
            print("Acesso permitido!")
            self.manager.switch_to(self.manager.get_screen('editar_usuario'))
            return

        self.ids.senha_status.text = 'Acesso negado.'

class EditarUsuarioScreen(Screen):
    def editar(self):
        email = self.ids.email_input.text
        senha = self.ids.password_input.text
        nome_usuario = self.ids.nome_input.text

        usuario_id = GlobalVars.usuario_id

        requisicao = requests.patch(f'{link}Usuarios/{usuario_id}/.json', json={'Email': email, 'Nome de Usuário': nome_usuario, 'Senha': senha})

        if requisicao.status_code == 200:
            print("Dados alterados com sucesso!")
            self.manager.switch_to(self.manager.get_screen('login'))  # Mudar para a tela de login

        else:
            print("Erro ao alterar dados de acesso.")

class SobreScreen(Screen):
    pass

class PaginaInicialScreen(Screen):
    def logout(self):
        GlobalVars.usuario_id = None
        self.manager.switch_to(self.manager.get_screen('login'))
    pass

sm = ScreenManager()
sm.add_widget(LoginScreen(name='login'))
sm.add_widget(CadastroScreen(name='cadastro'))
sm.add_widget(PaginaInicialScreen(name='pagina_inicial'))
sm.add_widget(ConfirmarScreen(name='confirmar'))
sm.add_widget(EditarUsuarioScreen(name='editar_usuario'))
sm.add_widget(LoginScreen(name='login'))
sm.add_widget(VisualizarTarefasScreen(name='visualizar_tarefas'))
sm.add_widget(EditarTarefaScreen(name='editar_tarefa'))
sm.add_widget(VisualizarTarefasScreen(name='visualizar_tarefas'))
sm.add_widget(HistoricoTarefasScreen(name='historico_tarefas'))
sm.add_widget(CadastrarTarefaScreen(name='cadastrar_tarefa'))
sm.add_widget(HistoricoTarefasScreen(name='historico_tarefas'))
sm.add_widget(PaginaInicialScreen(name='pagina_inicial'))
sm.add_widget(SobreScreen(name='sobre'))


class MeuApp(App):
    def build(self):
        return sm



if __name__ == '__main__':
    MeuApp().run()
