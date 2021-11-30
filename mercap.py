DIAS_SEMANA = ["lunes","martes","miercoles","jueves","viernes"]
HORAS_HABILES = [8,9,10,11,12,13,14,15,16,17,18,19,20]

class Cliente:
    "Representa el estado de los datos personales de un cliente."
    def __init__(self, nombre, apellido):
        self.nombre = nombre
        self.apellido = apellido

    def __str__(self):
        return str(self.nombre)+" "+str(self.apellido)+"\n" #cambiar a f
    
class Llamada:
    '''
    Representa el estado de una llamada telefónica.
    '''
    def __init__(self, id_cliente,hora,dia, mes, duracion, tipo):
        self.id_cliente = id_cliente
        self.hora = hora
        self.dia = dia
        self.mes = mes
        self.duracion = duracion
        self.tipo = tipo

class Facturas:
    '''
    Representa el estado de una factura telefónica.
    '''
    def __init__(self):
        self.id_cliente = 0
        self.id_llamada = 0
        self.clientes = {} #clientes = {id_cliente1: Cliente(nombre,apellido), id_cliente2: Cliente(nombre,apellido)}
        self.llamadas = {} #llamadas = {id_llamada1: Llamada(id_cliente,dia,duracion,tipo), id2:Llamada()}
        self.registros = {} #registros = {id_cliente1: {enero:[id_llamada,id_llamada2]},....}
        self.total_pagar = {} #total = {id_cliente1:{"abril":20,"enero":40},id_cliente2:{mes:15,mes:34},....}

    def __str__(self):
        return "Factura\nNº de cliente: "+str(self.id_cliente)+"\n"+str(self.clientes[self.id_cliente-1])

    def crear_cliente(self, nombre, apellido):
        '''
        Se ingresa el nombre y apellido del Cliente, generándose un id único para el mismo.
        '''
        self.clientes[self.id_cliente] = Cliente(nombre, apellido) 
        self.id_cliente += 1
        return self.id_cliente - 1

    def ingresar_llamada(self, hora,dia, mes, duracion, tipo):
        '''
        Se ingresan los datos de la llamada y se guardan.
        '''
        id_cli = self.id_cliente-1
        self.llamadas[self.id_llamada] = Llamada(id_cli,hora,dia,mes,duracion,tipo)

        if id_cli not in self.registros:
            self.registros[id_cli] = {}
        self.registros[id_cli][mes] = self.registros[id_cli].get(mes,[]) + [Llamada(id_cli,hora,dia,mes,duracion,tipo)]
        
        self.id_llamada += 1
        return self.id_llamada - 1

    def buscar_cliente(self,id_cliente,mes):
        '''
        Según el id del cliente ingresado se busca información y las llamadas realizadas ese mes, 
        imprimiendo toda la información.
        '''
        i = 1
        if id_cliente-1 not in self.clientes or mes.lower() not in self.registros[self.id_cliente-1]:
            raise ValueError("El cliente no existe o no se realizaron llamadas ese mes.")
        
        print (f'Cliente: {self.clientes[id_cliente-1]}Llamadas realizadas mes de {mes.upper()}')

        for llamada in self.registros[id_cliente-1][mes]:
            print(f'\nLlamada Nº{i}\nDía: {llamada.dia}\nDuración: {llamada.duracion}\nTipo de llamada: {llamada.tipo}')
            i += 1

    def listar_clientes(self):
        '''
        Función que lista todos los clientes ingresados a la base de datos hasta el momento.
        '''
        print('\nClientes:')
        for cliente in self.clientes:
            print(f'Nº{cliente+1}: {self.clientes[cliente].nombre} {self.clientes[cliente].apellido}\n')

    def facturacion(self,id_cliente,mes):
        tarifa = 0
        if id_cliente-1 not in self.registros or mes not in self.registros[id_cliente-1]:
            raise ValueError("El cliente aún no se registro o en el mes indicado no se realizaro llamadas.")

        for llamada in self.registros[id_cliente-1][mes]:
            if llamada.tipo.lower() == "local":
                if llamada.dia.lower() in DIAS_SEMANA and llamada.hora in HORAS_HABILES:
                    tarifa += 0.20 * llamada.duracion
                else:
                    tarifa += 0.10 * llamada.duracion

            elif llamada.tipo.lower() == "nacional":
                tarifa += 1.5 * llamada.duracion

            elif llamada.tipo.lower() == "internacional":
                tarifa += 5.2 * llamada.duracion

        if id_cliente-1 not in self.total_pagar:
            self.total_pagar[id_cliente-1] = {}
        self.total_pagar[id_cliente-1][mes] = self.total_pagar[id_cliente-1].get(mes,0) + round(tarifa,2) 
        
        print(f'\nCliente: nº{id_cliente} {self.clientes[id_cliente-1]}Total a pagar:{self.total_pagar[id_cliente-1][mes]}')

f = Facturas()
f.crear_cliente("Anggie","Miranda")
f.ingresar_llamada(8,"Martes","noviembre",4,"Local")
f.ingresar_llamada(15,"Sabado","noviembre",1,"Internacional")
f.ingresar_llamada(20,"Viernes","noviembre",8,"Local")
f.ingresar_llamada(10,"Jueves","noviembre",6,"Local")
f.facturacion(1,"noviembre")

f.crear_cliente("Pamela","Miranda")
f.ingresar_llamada(8,"Martes","noviembre",4,"Local")
f.ingresar_llamada(15,"Sabado","enero",1,"Local")
f.ingresar_llamada(20,"Viernes","enero",8,"Local")
f.ingresar_llamada(10,"Jueves","noviembre",6,"Local")
f.facturacion(2,"enero")

f.crear_cliente("Carmen","Rivera")
f.ingresar_llamada(8,"Martes","noviembre",4,"Local")
f.ingresar_llamada(15,"Sabado","enero",1,"Local")
f.ingresar_llamada(20,"Viernes","noviembre",8,"Local")
f.ingresar_llamada(10,"Jueves","noviembre",6,"Local")
f.facturacion(3,"noviembre")


f.buscar_cliente(2,"noviembre")
f.listar_clientes()