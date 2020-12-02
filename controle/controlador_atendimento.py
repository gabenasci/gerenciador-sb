from excecoes.funcionario_indisponivel import FuncionarioIndisponivelExcecao
from excecoes.objeto_nao_existe import ObjetoNaoExisteExcecao
from entidade.atendimento import Atendimento
from limite.tela_atendimento import TelaAtendimento
from limite.tela_inclui_atendimento import TelaIncluiAtendimento
from collections import Counter
import PySimpleGUI as sg
import datetime
from DAO.AtendimentoDAO import AtendimentoDAO


class ControladorAtendimento:
    __instance = None

    def __init__(self, controlador_sistema):
        self.__atendimento_dao = AtendimentoDAO()

        self.__controlador = controlador_sistema
        self.__tela_atendimento = TelaAtendimento(self)
        self.__tela_inclui_atendimento = TelaIncluiAtendimento(self)
        self.__continua_exibindo_tela = True

    def __new__(cls, controlador_sistema):
        if ControladorAtendimento.__instance is None:
            ControladorAtendimento.__instance = object.__new__(cls)
        return ControladorAtendimento.__instance

    def abre_tela(self):
        switcher = {'Voltar': self.retorna, 'Incluir': self.inclui_atendimento}

        while True:
            self.__tela_atendimento.init_components()
            button, values = self.__tela_atendimento.open()
            if button == 'Voltar' or button == sg.WIN_CLOSED:
                break
            elif button == 'Excluir':
                for atendimento in self.__atendimento_dao.get_all():
                    # verifica se checkbox está clicado
                    if values[atendimento.id] == True:
                        self.__atendimento_dao.remove(atendimento.id)
            elif button == 'Alterar':
                for atendimento in self.__atendimento_dao.get_all():
                    if values[atendimento.id] == True:
                        ano = str(atendimento.data.year)
                        mes = str(atendimento.data.month)
                        dia = str(atendimento.data.day)
                        data = dia + '/' + mes + '/' + ano
                        hora = str(atendimento.hora.hour)
                        min = str(atendimento.hora.minute)
                        horario = hora + ':' + min
                        self.altera_atendimento(atendimento.id, atendimento.cliente,
                                                atendimento.funcionario, data, horario, atendimento.valor, atendimento.pago, atendimento.realizado)
            else:
                funcao_escolhida = switcher[button]
                if funcao_escolhida == self.inclui_atendimento:
                    funcao_escolhida(None, None, None, None, None, None, None, None)

            self.__tela_atendimento.close()
        self.__tela_atendimento.close()

    def inclui_atendimento(self, id, cliente, funcionario, data, hora, valor, pago, realizado):
        self.__tela_inclui_atendimento.init_components(id, cliente, funcionario, data, hora, valor, pago, realizado)
        button, values = self.__tela_inclui_atendimento.open()
        if button == sg.WIN_CLOSED or button == 'Voltar':
            self.__tela_inclui_atendimento.close()

        cadastro = True
        if button == 'Salvar':
            while cadastro:
                try:
                    servico = values['it_servico']
                    if servico not in self.servicos():
                        raise ObjetoNaoExisteExcecao
                except ObjetoNaoExisteExcecao:
                    sg.Popup('Serviço não existe')
                    self.__tela_inclui_atendimento.close()
                    self.inclui_atendimento()
                    break
                try:
                    cliente = values['it_cliente']
                    if cliente not in self.clientes():
                        raise ObjetoNaoExisteExcecao
                except ObjetoNaoExisteExcecao:
                    sg.Popup('Cliente não existe')
                    self.__tela_inclui_atendimento.close()
                    self.inclui_atendimento()
                    break
                try:
                    funcionario = values['it_funcionario']
                    if funcionario not in self.funcionarios():
                        raise ObjetoNaoExisteExcecao
                except ObjetoNaoExisteExcecao:
                    sg.Popup('Funcionario não existe')
                    self.__tela_inclui_atendimento.close()
                    self.inclui_atendimento()
                    break
                try:
                    data = values['it_data']
                    dia, mes, ano = map(int, data.split('/'))
                    data_atendimento = datetime.date(ano, mes, dia)
                    if data_atendimento < datetime.date.today():
                        raise ValueError
                except ValueError:
                    sg.Popup("Data inválida!")
                    self.__tela_inclui_atendimento.close()
                    self.inclui_atendimento()
                try:
                    hora = values['it_hora']
                    h, m = map(int, hora.split(':'))
                    hora_atendimento = datetime.time(h, m)
                except ValueError:
                    sg.Popup("Horário inválido!")
                    self.__tela_inclui_atendimento.close()
                    self.inclui_atendimento()
                valor = values['it_valor']
                try:
                    valor = float(valor)
                except ValueError:
                    sg.Popup("Valor float inválido")
                    self.__tela_inclui_atendimento.close()
                    self.inclui_atendimento()
                pago = values['pago']
                realizado = values['realizado']

                try:
                    for atendimento in self.__atendimento_dao.get_all():
                        if atendimento.funcionario.nome == values["it_funcionario"] and atendimento.data == values["it_data"] and \
                                atendimento.hora == values["it_hora"]:
                            raise FuncionarioIndisponivelExcecao
                    #servico = self.__controlador.controlador_servico.busca_servico_nome(dados_atendimento["servico"])

                    for servico in self.__controlador.controlador_servico.servicos:
                        if servico.nome == values["it_servico"]:
                            servico = values['it_servico']
                    #dados_atendimento["servico"] = servico
                    for cliente in self.__controlador.controlador_cliente.clientes:
                        if cliente.nome == values["it_cliente"]:
                            cliente = values['it_cliente']
                    for funcionario in self.__controlador.controlador_funcionario.funcionarios:
                        if funcionario.nome == values["it_funcionario"]:
                            funcionario = values['it_funcionario']


                    novo_atendimento = Atendimento(servico, cliente, funcionario,
                                                   data, hora, valor, pago, realizado)
                    self.__atendimento_dao.add(novo_atendimento)
                    novo_atendimento.id = len(self.__atendimento_dao.get_all())
                    self.__tela_inclui_atendimento.close()
                    sg.Popup('Atendimento cadastrado')
                    cadastro = False
                    break
                except FuncionarioIndisponivelExcecao:
                    sg.Popup('Este funcionário não está disponível nesse horario!')
                    self.__tela_inclui_atendimento.close()
                    self.inclui_atendimento()
                    break

    def exclui_atendimento(self):
        button, values = self.__tela_atendimento.open()
        for atendimento in self.__atendimento_dao.get_all():
            if values[atendimento.id] == True:
                self.__atendimento_dao.remove(atendimento.id)


    def lista_atendimentos_cliente(self):
        cliente = self.__tela_atendimento.atendimento_cliente()
        for atendimento in self.__atendimentos:
            if atendimento.cliente.nome == cliente:
                self.__tela_atendimento.mostra_dados_atendimento(atendimento.id, atendimento.servico,
                                                                 atendimento.cliente, atendimento.funcionario,
                                                                 atendimento.data, atendimento.hora, atendimento.valor,
                                                                 atendimento.pago, atendimento.realizado)

    def lista_atendimentos_dia(self):
        dia = self.__tela_atendimento.atendimento_dia()
        for atendimento in self.__atendimentos:
            if atendimento.data == dia:
                self.__tela_atendimento.mostra_dados_atendimento(atendimento.id, atendimento.servico,
                                                                 atendimento.cliente, atendimento.funcionario,
                                                                 atendimento.data, atendimento.hora,
                                                                 atendimento.valor, atendimento.pago, atendimento.realizado)

    def altera_atendimento(self, id, cliente, funcionario, data, hora, valor, pago, realizado):
        self.__tela_inclui_atendimento.init_components(id, cliente, funcionario, data, hora, valor, pago, realizado)
        button, values = self.__tela_inclui_atendimento.open()
        if button == sg.WIN_CLOSED or button == 'Voltar':
            self.__tela_inclui_atendimento.close()

        cadastro = True
        if button == 'Salvar':
            while cadastro:
                try:
                    servico = values['it_servico']
                    if servico not in self.__controlador.controlador_servico.servicos():
                        raise ObjetoNaoExisteExcecao
                except ObjetoNaoExisteExcecao:
                    sg.Popup('Serviço não existe')
                    self.__tela_inclui_atendimento.close()
                    self.inclui_atendimento()
                    break
                try:
                    cliente = values['it_cliente']
                    if cliente not in self.__controlador.controlador_cliente.clientes():
                        raise ObjetoNaoExisteExcecao
                except ObjetoNaoExisteExcecao:
                    sg.Popup('Cliente não existe')
                    self.__tela_inclui_atendimento.close()
                    self.inclui_atendimento()
                    break
                try:
                    funcionario = values['it_funcionario']
                    if funcionario not in self.__controlador.controlador_funcionario.funcionarios():
                        raise ObjetoNaoExisteExcecao
                except ObjetoNaoExisteExcecao:
                    sg.Popup('Funcionario não existe')
                    self.__tela_inclui_atendimento.close()
                    self.inclui_atendimento()
                    break
                try:
                    data = values['it_data']
                    dia, mes, ano = map(int, data.split('/'))
                    data_atendimento = datetime.date(ano, mes, dia)
                    if data_atendimento < datetime.date.today():
                        raise ValueError
                except ValueError:
                    sg.Popup("Data inválida!")
                    self.__tela_inclui_atendimento.close()
                    self.inclui_atendimento()
                try:
                    hora = values['it_hora']
                    h, m = map(int, hora.split(':'))
                    hora_atendimento = datetime.time(h, m)
                except ValueError:
                    sg.Popup("Horário inválido!")
                    self.__tela_inclui_atendimento.close()
                    self.inclui_atendimento()
                valor = values['it_valor']
                try:
                    valor = float(valor)
                except ValueError:
                    sg.Popup("Valor float inválido")
                    self.__tela_inclui_atendimento.close()
                    self.inclui_atendimento()
                pago = values['pago']
                try:
                    if pago == "True":
                        pago = True
                    elif pago == "False":
                        pago = False
                except ValueError:
                    sg.Popup("Valor booleano inválido")
                    self.__tela_inclui_atendimento.close()
                    self.inclui_atendimento()
                realizado = values['realizado']
                try:
                    if realizado == 'True':
                        realizado = True
                    elif realizado == 'False':
                        realizado = False
                except ValueError:
                    sg.Popup("Valor booleano inválido")
                    self.__tela_inclui_atendimento.close()
                    self.inclui_atendimento()
                try:
                    for atendimento in self.__atendimento_dao.get_all():
                        if atendimento.funcionario.nome == values["it_funcionario"] and atendimento.data == values[
                            "it_data"] and \
                                atendimento.hora == values["it_hora"]:
                            raise FuncionarioIndisponivelExcecao
                    # servico = self.__controlador.controlador_servico.busca_servico_nome(dados_atendimento["servico"])

                    for servico in self.__controlador.controlador_servico.servicos:
                        if servico.nome == values["it_servico"]:
                            servico = values['it_servico']
                    # dados_atendimento["servico"] = servico
                    for cliente in self.__controlador.controlador_cliente.clientes:
                        if cliente.nome == values["it_cliente"]:
                            cliente = values['it_cliente']
                    for funcionario in self.__controlador.controlador_funcionario.funcionarios:
                        if funcionario.nome == values["it_funcionario"]:
                            funcionario = values['it_funcionario']

                    for atendimento in self.__atendimento_dao.get_all():
                        self.__atendimento_dao.remove(atendimento.id)
                    novo_atendimento = Atendimento(servico, cliente, funcionario,
                                                   data, hora, valor, pago, realizado)
                    self.__atendimento_dao.add(novo_atendimento)
                    novo_atendimento.id = len(self.__atendimento_dao.get_all())
                    self.__tela_inclui_atendimento.close()
                    sg.Popup('Atendimento alterado')
                    cadastro = False
                    break
                except FuncionarioIndisponivelExcecao:
                    sg.Popup('Este funcionário não está disponível nesse horario!')
                    self.__tela_inclui_atendimento.close()
                    self.inclui_atendimento()
                    break

        '''
        id_atendimento, dado, valor_dado = self.__tela_atendimento.altera_dados_atendimento()
        for atendimento in self.__atendimentos:
            if atendimento.id == id_atendimento:
                dados_atendimento = {"servico": atendimento.servico,
                                     "cliente": atendimento.cliente,
                                     "funcionario": atendimento.funcionario, "data": atendimento.data,
                                     "hora": atendimento.hora, "valor": atendimento.valor,
                                     "pago": atendimento.pago, "realizado": atendimento.realizado}
                dados_atendimento[dado] = valor_dado
                for servico in self.__controlador.controlador_servico.servicos:
                    if servico.nome == dados_atendimento["servico"]:
                        dados_atendimento["servico"] = servico
                for cliente in self.__controlador.controlador_cliente.clientes:
                    if cliente.nome == dados_atendimento["cliente"]:
                        dados_atendimento["cliente"] = cliente
                for funcionario in self.__controlador.controlador_funcionario.funcionarios:
                    if funcionario.nome == dados_atendimento["funcionario"]:
                        dados_atendimento["funcionario"] = funcionario
                index = self.__atendimentos.index(atendimento)
                self.__atendimentos.remove(atendimento)
                atendimento_alterado = Atendimento(dados_atendimento["servico"],
                                                   dados_atendimento["cliente"],
                                                   dados_atendimento["funcionario"], dados_atendimento["data"],
                                                   dados_atendimento["hora"], dados_atendimento["valor"],
                                                   dados_atendimento["pago"], dados_atendimento["realizado"])
                self.__atendimentos.insert(index, atendimento_alterado)
                atendimento_alterado.id = id_atendimento
        '''
    @property
    def atendimentos(self):
        return self.__atendimento_dao.get_all()

    def gera_relatorio_mes(self):
        mes = self.__tela_atendimento.relatorio_mes()
        atendimentos_mes = []
        for atendimento in self.__atendimentos:
            if atendimento.data.month == mes:
                atendimentos_mes.append(atendimento.servico.nome)
        contador_servicos = dict(Counter(atendimentos_mes))
        print("--- Número de atendimentos no mês "+str(mes)+": ---")
        for chave, valor in contador_servicos.items():
            print(chave+':', valor)

    def retorna(self):
        self.__continua_exibindo_tela = False

    def servicos(self):
        servicos_str = []
        for s in self.__controlador.controlador_servico.servicos:
            servicos_str.append(s.nome)
        return servicos_str

    def clientes(self):
        clientes_str = []
        for c in self.__controlador.controlador_cliente.clientes:
            clientes_str.append(c.nome)
        return clientes_str

    def funcionarios(self):
        funcionarios_str = []
        for c in self.__controlador.controlador_funcionario.funcionarios:
            funcionarios_str.append(c.nome)
        return funcionarios_str
