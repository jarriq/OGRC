from pysnmp.hlapi import  *
from pysnmp.proto.rfc1902 import Integer



class SNMP():

    def __init__(self, ip_switch=None, comunidade=None):
        self.ip_switch = ip_switch
        self.comunidade = comunidade

    def testa_conexao(self):
        """
        Verifica conexao atraves do protocolo SNMP
        """
        if self.ip_switch is None or self.comunidade is None:
            raise ValueError("IP ou comunidade não inicializados")

        eIndication, eStatus, eIndex, varBinds = next(
            getCmd(SnmpEngine(),
                   CommunityData(self.comunidade, mpModel=0),
                   UdpTransportTarget((self.ip_switch, 161)),
                   ContextData(),
                   ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)))
                   )

        return self._verifica_comando(eIndication,
                                       eStatus,
                                       eIndex,
                                       varBinds)


    def altera_porta(self, port, command):
        """
        Liga ou desliga porta via SNMP

        Params
            port: int, numero da porta fisica a ser desligada ou ligada
            command: int, 1 - liga porta, 2 - desliga porta
        """
        eIndication, eStatus, eIndex, varBinds = next(
            setCmd(SnmpEngine(),
                CommunityData(self.comunidade, mpModel=0),
                UdpTransportTarget((self.ip_switch, 161)),
                ContextData(),
                ObjectType(ObjectIdentity('IF-MIB','ifAdminStatus', int(port)), Integer(command)))
            )

        return self._verifica_comando(eIndication,
                                       eStatus,
                                       eIndex,
                                       varBinds)

    def altera_todas_as_portas(self, command):
        portas = list(range(2,24))

        for port in portas:
            if not self.altera_porta(port, command):
                break


    def _verifica_comando(self, eIndication,
                                eStatus,
                                eIndex,
                                varBinds):
        if eIndication:
            print(eIndication)
            return False
        elif eStatus:
            print('%s at %s' % (eStatus.prettyPrint(),
                                eIndex and varBinds[int(eIndex) - 1][0] or '?'))
            return False
        else:
            for varBind in varBinds:
                print(' = '.join([x.prettyPrint() for x in varBind]))
            return True
