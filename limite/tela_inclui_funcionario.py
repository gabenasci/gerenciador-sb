import PySimpleGUI as sg


class TelaIncluiFuncionario:
    def __init__(self, controlador_funcionario):
        self.__controlador = controlador_funcionario
        self.__window = None
        self.init_components()


    def init_components(self):
        sg.ChangeLookAndFeel('Reddit')

        layout = [
                    [sg.Text('Cadastro de Funcionário', size=(30, 1), font=("Helvetica", 25))],
                    [sg.Text('Nome: ', size=(40, 1)), sg.InputText('', key='it_nome')],
                    [sg.Text('Data de Nascimento (DIA/MES/ANO): ', size=(40, 1)), sg.InputText('', key='it_data_nascimento')],
                    [sg.Text('Telefone: ', size=(40, 1)), sg.InputText('', key='it_telefone')],
                    [sg.Text('Data de contratação: ', size=(40, 1)), sg.InputText('', key='it_data_contratacao')],
                    #[sg.Output('')]
                    [sg.Submit('Salvar'), sg.Cancel('Voltar')]
                ]

        self.__window = sg.Window('Cadastro de funcionário', default_button_element_size=(40, 1)).Layout(layout)

    def open(self):
        button, values = self.__window.Read()
        return button, values

    def close(self):
        self.__window.Close()