import simpy
import queue
import random 

#clase que representa un proceso del Sistema operativo
class Proceso:
    
    def __init__(self, lleg, mins, Mins, mRAM, MRAM):
        self.instrucciones = random.randint(mins,Mins)
        self.llegada = lleg
        self.memoria = random.randint(mRAM, MRAM)

class SistemaOperativo:
    
    def __init__(self,env, procesos_tot, cpu_instrucciones):
        #variables para almacenamineto de parametros del SO
        self.num_procesos = procesos_tot
        self.cpu_lim = cpu_instrucciones
        self.procesos_terminados = 0
        self.enviroment = env
        self.RAM = simpy.Container(env, init=100, capacity=100)
        self.CPU = simpy.Resource(env, capacity=1)

    #Crea los procesos y los asigna en un array
    #siendo "a" el numero de procesos de la simulacion
    #regresa una Queue que contine procesos 
    def creacion(self, intervalo, min_instrucciones, max_instrucciones, min_RAM, max_RAM):
        
        #Variables del metodo para la creacion
        tiempo = 0
        self.procesos = []
        
        for x in range(self.num_procesos):
            tiempo =+ random.expovariate(1.0 / intervalo)
            proc = Proceso(tiempo, min_instrucciones, max_instrucciones, min_RAM, max_RAM)
            self.procesos.put(proc)
    
    def simulacion(self):
    
        if(self.procesos is null):
            print("No hay procesos para realizar")
        else:
        
            waiting = []
            ready = []
            
            while(self.procesos_terminados < self.procesos_tot):
                if not ready:
                    ready[0].instrucciones
                    

                #para saber si las colas estan vacias
                if not waiting:
                    if waiting[0].memoria <= self.RAM.level:
                        self.RAM.get(waiting[0].memoria)
                        ready.append(waiting[0])
                        del waiting[0]
                if not self.procesos:
                    if self.procesos[0].memoria <= self.RAM.level:
                        self.RAM.get(self.procesos[0].memoria)
                        ready.append(self.procesos[0])
                        del self.procesos[0]

#Parametros de la simulacion
cpu_instrucciones = 3
num_procesos = 25
intervalo = 10
min_instrucciones = 1
max_instrucciones = 10
min_RAM = 1
max_RAM = 10


#semilla para la creacion pseudo random
RANDOM_SEED = 20
random.seed(RANDOM_SEED)

env = simpy.Environment()


CPU = simpy.Resource(env, capacity=1)
req = CPU.request()
CPU.release(req)
print(CPU)