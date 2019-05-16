from pysnmp.hlapi import SnmpEngine, setCmd, CommunityData, UdpTransportTarget, ContextData, ObjectType, ObjectIdentity
from pysnmp.proto.rfc1902 import Integer



class SNMP():

    def __init__(self, udptarget=None):
        if udptarget is None:
            self.udptarget = '10.90.90.90'


    def altera_status(self, port, command):
        """
        Liga ou desliga porta via SNMP

        Params
            port: int, numero da porta fisica a ser desligada ou ligada
            command: int, 1 - liga porta, 2 - desliga porta
        """
        errorIndication, errorStatus, errorIndex, varBinds = next(
            setCmd(SnmpEngine(),
                CommunityData('private', mpModel=0),
                UdpTransportTarget((self.udptarget, 161)),
                ContextData(),
                ObjectType(ObjectIdentity('IF-MIB', 'ifAdminStatus', int(port)), Integer(int(command)))
                )
            )

        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        else:
            for varBind in varBinds:
                print(' = '.join([x.prettyPrint() for x in varBind]))
