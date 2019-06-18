
from apscheduler.schedulers.background import BackgroundScheduler
import datetime as dt
import ogrc.db as db
from ogrc.snmp import SNMP
import json

class Escalonador():

    def __init__(self):
        print("Iniciando Escalonador...")
        self.sched = self.prepara_agendador()
        print("Pronto.")


    def prepara_agendador(self):
        """
        Busca agendamentos no banco de dados,
        retorna BackgroundScheduler, com agendamentos
        cadastrados no banco. Também iniciliza o
        atributo no Escalonador
        """
        sched = BackgroundScheduler()

        agendamentos = json.loads(db.lista_agendamentos())

        print("Total de " + str(len(agendamentos)) + " agendamentos encontrados")
        for agend in agendamentos:
            if not agend['executado']:
                data = self.converte_data(agend)
                sched.add_job(lambda: self.executa_agendamento(agend),
                            'date', run_date=data)
        return sched

    def adiciona_agendamento(self, agend):
        """
        Recebe um 'dict' com dados do agendamento,
        conforme formato do banco, e cadastra
        o mesmo no BackgroundScheduler, atributo do
        Escalonador
        """
        data = self.converte_data(agend)
        self.sched.add_job(lambda: self.executa_agendamento(agend),
                           'date', run_date=data)

    def executa_agendamento(self, agend):
        """
        Executa agendamento proveniente do 'dict' agend,
        alterando o status da porta, tanto fisicamente
        quanto no banco
        """
        print("Executando agendamento...")
        print(agend)

        snmp = SNMP(agend["ip_switch"], agend["comunidade"])

        if snmp.testa_conexao():
            print("Conectado")
            if agend['conectar']:
                comando = 1
            else:
                comando = 2

            if snmp.altera_porta(agend['porta'], comando):
                db.altera_status_porta(agend['porta'], agend['conectar'])
                print("Sucesso na execução do agendamento")
            else:
                print("Falha na execução do agendamento")

        db.altera_status_agendamento(agend)

    def converte_data(self, agend):
        """
        Converte o formato data recebido no formato
        'str' do agend para 'datetime'
        """
        dia = agend['data']
        hora = agend['horario']
        data  = dt.datetime.strptime(dia + " " + hora, r'%d/%m/%Y %H:%M')
        return data
