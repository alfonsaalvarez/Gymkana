#!/usr/bin/python3

from socket import *
import urllib.request
import struct
import time
import _thread 

import ast


def etapa0():
	sock = socket(AF_INET, SOCK_STREAM)
	sock.connect(('atclab.esi.uclm.es', 2000))
	msg = sock.recv(1024).decode()
	print(msg + '\n')
	sock.close()

	codigo = msg.split('\n')
	return codigo[0]

def etapa1(codigo):

	socketUDP = socket(AF_INET, SOCK_DGRAM)
	socketUDP.bind(('', 1000))

	msgco = codigo +" 1000"
	
	socketUDP.sendto(msgco.encode(),(('atclab.esi.uclm.es', 2000)))
	msg = socketUDP.recv(1024).decode()
	
	print(msg)
	puerto=msg.split('\n')
	return puerto[0]
	sockeUDP.close()

def operacion(cadena): 
	return resolver(ast.parse(cadena, mode='eval').body)
	

def resolver(mensaje): 
	if (isinstance(mensaje, ast.Num)):
		return mensaje.n
	if (isinstance(mensaje, ast.BinOp)):
		left= resolver(mensaje.left)
		right=resolver(mensaje.right)	
		if isinstance(mensaje.op, ast.Add):
			return left + right
		elif isinstance(mensaje.op, ast.Sub):
			return left - right
		elif isinstance(mensaje.op, ast.Mult):
			return left*right
		elif isinstance(mensaje.op, ast.Div):
			return left//right


def etapa2(puerto):

	socketTCP=socket(AF_INET,SOCK_STREAM)
	socketTCP.connect(('atclab.esi.uclm.es', int( puerto)))
	cadena= ''

	while 1:
		cadena = cadena + socketTCP.recv(1024).decode()
		if cadena[0]=='(':
			if cadena.count('(')==cadena.count(')'):

				resultado=('('+str(operacion(cadena))+')')
				print('La operación matemática es: ' + cadena+ ' y su resultado: ' + resultado + '\n')	
				socketTCP.sendto(resultado.encode(),('atclab.esi.uclm.es', int( puerto)))
				cadena=''
		
		else:
			print (cadena+ '\n')
			cadena=cadena.split('\n')
			return cadena[0]
	socketTCP.close()

  
def etapa3(cadena):
    direccion="http://atclab.esi.uclm.es:5000/"+cadena
    respuesta=urllib.request.urlopen(direccion)
    puerto1=respuesta.read().decode()
    print (puerto1+'\n')
    respuesta.close()
    return puerto1.split('\n')[0]


def etapa4(puerto1):
    sockRAW = socket(AF_INET, SOCK_RAW, getprotobyname("icmp"))
    
    header = struct.pack('!bbHhh', 8, 0, 0, 1110, 1)
    tiempo = time.time()
    timestamp = struct.pack('!d', tiempo)
   
    checksum = cksum(header+timestamp+puerto1.encode())
    paquete=struct.pack('!bbHhh', 8, 0, checksum, 1110, 1)+timestamp+puerto1.encode()
    sockRAW.sendto(paquete , ('atclab.esi.uclm.es', 80))
    
    sockRAW.recv(2048)
    identificador = (sockRAW.recv(2048)[36:]).decode()
    print(identificador)
    return identificador.split('\n')[0]



def cksum(data):

    def sum16(data):
        "sum all the the 16-bit words in data"
        if len(data) % 2:
            data = data + '\0'.encode()

        return sum(struct.unpack("!%sH" % (len(data) // 2), data))

    retval = sum16(data)                       
    retval = sum16(struct.pack('!L', retval))  
    retval = (retval & 0xFFFF) ^ 0xFFFF        
    return retval

 

def main():
  
    print ('                     GYMKANA: ALFONSA ÁLVAREZ BELLÓN')

    print('Ejecucion etapa 0')
    codigo = etapa0()

    print('Ejecucion etapa 1: UDP')
    puerto= etapa1(codigo)

    print('Ejecucion etapa 2: Aritmetica')
    cadena=etapa2(puerto)
      
    print('Ejecucion etapa 3: Cliente HTTP')
    puerto1= etapa3(cadena)

    print('Ejecucion etapa 4: ICMP')
    identificador=etapa4(puerto1)
  
main()
