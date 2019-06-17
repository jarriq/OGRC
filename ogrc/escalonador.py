
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
        data = self.converte_data(agend)
        self.sched.add_job(lambda: self.executa_agendamento(agend),
                           'date', run_date=data)

    def executa_agendamento(self, agend):
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
        print(agend)
        dia = agend['data']
        hora = agend['horario']
        data  = dt.datetime.strptime(dia + " " + hora, r'%d/%m/%Y %H:%M')
        return data


if __name__=="__main__":
    e = Escalonador()
    print(e.converte_data({"data":"14/06/2017","hora":"16:00"}))
    #sudo ip a add 10.0.0.133/8 dev enp2s0
