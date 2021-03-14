import simpy
import queue
import random 
import time
import statistics as stats

#clase que representa un proceso del Sistema operativo
class Proceso:
    
    def __init__(self, mins, Mins, mRAM, MRAM, time):
        self.instrucciones = random.randint(mins,Mins)
        self.memoria = random.randint(mRAM, MRAM)
        self.tiempo= time

class SistemaOperativo:
    
    def __init__(self,env, procesos_tot, cpu_instrucciones,cpus, memRAM):
        #variables para almacenamineto de parametros del SO
        self.num_procesos = procesos_tot
        self.cpu_lim = cpu_instrucciones
        self.procesos_terminados = 0
        self.enviroment = env
        self.RAM = simpy.Container(env, init=memRAM, capacity=memRAM)
        self.CPU = simpy.Resource(env, capacity=cpus)
        self.distribution = []
        self.cpus = cpus

    #Crea los procesos y los asigna en un array
    #siendo "a" el numero de procesos de la simulacion
    #regresa una Queue que contine procesos 
    def creacion(self, intervalo): #min_instrucciones, max_instrucciones, min_RAM, max_RAM):
        
        #Variables del metodo para la creacion
        tiempo = 0
               
        for x in range(self.num_procesos):
            tiempo =+ random.expovariate(1.0 / intervalo)
            #proc = Proceso(tiempo, min_instrucciones, max_instrucciones, min_RAM, max_RAM)
            self.distribution.append(tiempo)
    
    def simulacion(self, min_instrucciones, max_instrucciones, min_RAM, max_RAM):
    
        tiempos = []
        
        if len(self.distribution) == 0:
            print("No hay procesos para realizar")
        else:
        
            tiempo = 0
            procesos = []
            waiting = []
            ready = []
            CPU_list = []
            
            while(self.procesos_terminados < self.num_procesos):
                for i in range(self.cpus):
                    if self.CPU.count > 0:
                        self.CPU.release(self.CPU.users[0])
                        procesado = CPU_list[0]
                        procesado.instrucciones =- self.cpu_lim

                        if procesado.instrucciones > 0:
                            wait = random.randint(1,2)
                            
                            if wait == 1:
                                ready.append(procesado)
                                self.RAM.get(procesado.memoria)
                            else:
                                waiting.append(procesado)
                        else:
                            self.procesos_terminados += 1
                            tiempos.append(time.time() - procesado.tiempo)
                        

                        CPU_list.pop(0)
                
                #para saber si las colas estan vacias
                if len(waiting) != 0:
                    if waiting[0].memoria <= self.RAM.level:
                        self.RAM.get(waiting[0].memoria)
                        ready.append(waiting[0])
                        del waiting[0]
                
                if (len(self.distribution) != 0):
                    
                    if(self.distribution[0] <= tiempo):
                        proceso = Proceso(min_instrucciones, max_instrucciones, min_RAM, max_RAM, time.time())
                        procesos.append(proceso)
                        self.distribution.pop(0)
                    
                if len(procesos) != 0:
                    proceso = procesos[0]
                    #print(proceso.memoria)
                    #print(self.RAM.level)

                    if proceso.memoria <= self.RAM.level:                      
                        self.RAM.get(proceso.memoria)
                        #print(self.RAM.level)
                        ready.append(proceso)
                        proceso.tiempo = time.time()
                        procesos.pop(0)

                if len(ready) > 0:
                    proceso = ready[0]
                    self.RAM.put(proceso.memoria)
                    CPU_list.append(proceso)
                    ready.pop(0)
                    self.CPU.request()
                
                tiempo += 1
                #print(tiempo)
        return tiempos

def average(lista):
    promedio = sum(lista)/len(lista)
    return promedio
    
#Parametros de la simulacion
memRAM = 100
cpus = 1
cpu_instrucciones = 3
intervalo = 1
num_procesos = [25,50,100,150,200]
min_instrucciones = 1
max_instrucciones = 10
min_RAM = 1
max_RAM = 10
file1 = open('Mem'+str(memRAM)+'Int'+str(intervalo)+'CPU'+str(cpus)+'Inst'+str(cpu_instrucciones)+'.csv', 'w') 

#semilla para la creacion pseudo random
RANDOM_SEED = 25

datas = "Procesos, Tiempo"
for i in range(len(num_procesos)):
    random.seed(RANDOM_SEED)
    env = simpy.Environment()
    so = SistemaOperativo(env, num_procesos[i], cpu_instrucciones, cpus, memRAM)
    so.creacion(intervalo)
    lista_tiempos = so.simulacion(min_instrucciones, max_instrucciones, min_RAM, max_RAM)
    x=average(lista_tiempos)
    est=stats.pstdev(lista_tiempos)
    print("El promedio para " +str(num_procesos[i])+" procesos es de " + str(x) +" y la desviacion estandar es de " + str(est) )
    datas += "\n" + str(num_procesos[i])+"," + str(x)
    
file1.write(datas)