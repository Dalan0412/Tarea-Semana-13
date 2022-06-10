import numpy as np
import random
import matplotlib.pyplot as plt

def defciudades(nciudades):
    #defciudades se encarga de definir las coordenadas de cada ciudad
    ciudades=[[]*2]*nciudades
    x=0
    y=0
    for i in range(nciudades):
        x=0.1*((9+13*(i+1)*(i+1))%200)
        y=0.1*((7+1371*(i+1))%200)
        ciudades[i]=[x,y]
    return ciudades


def poblacionsimple(npersonas,nciudades,cities):
    #Version simple de formar la poblacion
    #Solo ordena el orden de las ciudades de forma aleatoria
    ordenog=[]
    for i in range(nciudades):
        ordenog.append(i)
    poblacion=[ordenog]*npersonas
    for i in range(npersonas):
        random.shuffle(poblacion[i])
    return poblacion
    
def poblacion(npersonas,nciudades,cities):
    #Poblacion es la version modificada de la poblacion
    #Esta escoge una ciudad inicial y luego busca la más cercana
    #y asi sucesivamente hasta terminar la población
    poblacion=[[]*nciudades]*npersonas
    for i in range(npersonas):
        persona=[1000]*nciudades
        c=0
        rand=int(random.randint(0,nciudades-1))
        persona[c]=rand
        c=1
        while c<nciudades:
            exclude=persona.copy()
            punto=cities[int(persona[c-1])].copy()
            persona[c]=citymin(punto,cities,exclude)     
            c=c+1    
        poblacion[i]=persona
    return poblacion


def distancia(punto1,punto2):
    #Devuelve la distancia entre dos puntos
    return np.sqrt((punto1[0]-punto2[0])*(punto1[0]-punto2[0])+(punto1[1]-punto2[1])*(punto1[1]-punto2[1]))

def recorrido(persona,ciudades):
    #Calcula la distancia del recorrido para una sola persona
    ruta=0
    for i in range(len(persona)-1):
        ruta=ruta+distancia(ciudades[int(persona[i])],ciudades[int(persona[i+1])])
    ruta=ruta+distancia(ciudades[int(persona[0])],ciudades[int(persona[-1])])
    return ruta

def recmin(poblacion,ciudades):
    #Encuentra en toda la poblacion la persona que recorre la menor distancia
    #Además devuelve tambien el valor de dicha distancia
    indexmin=0
    dismin=recorrido(poblacion[0],ciudades)
    index=0
    for i in poblacion:
        dis=recorrido(i,ciudades)
        if dis<dismin:
            dismin=dis
            indexmin=index
        index=index+1
    return [dismin,poblacion[indexmin]]

def citymin(punto,cities,exclude):
    #dada una ciudad revisa cual es la ciudad más cercana a esta
    #ignorando aquellas ciudades que ya no estan disponibles
    index=0
    dismin=100000
    indexmin=0
    for i in cities:
        control=0
        for j in exclude:
            if index==int(j):
                control=control+1
        if control==0:
            dis=distancia(punto,i)
            if dis<dismin:
                dismin=dis
                indexmin=index
        index=index+1
    return indexmin

def creargraf(persona,dis,cities,gen):
    #Crea y guarda una grafica de la ruta
    fig = plt.figure()
    x=np.zeros(101)
    y=np.zeros(101)
    control=0
    for i in persona:
        x[control]=cities[int(i)][0]
        y[control]=cities[int(i)][1]
        control=control+1
    x[100]=cities[int(persona[0])][0]
    y[100]=cities[int(persona[0])][1]
    plt.plot(x,y,marker='o')
    plt.title("recorrido de "+str(round(dis,4))+" y ajuste de "+str(round(1/dis,5))+"\n"+"de la generacion "+str(gen))
    fig.savefig("recorrido min mod"+str(gen))
    return

def mutpersona(persona,cities):
    #Se encarga de realizar la mutacion
    #Resive una persona y realiza la mutacion
    #En caso de ser exitosa devuelve la mutacion
    pmut=0.50
    nuevo=persona.copy()
    many=random.randint(3,10)
    i=0
    tiro=0
    while i < many:
        control=nuevo.copy()
        c=0
        num1=int(random.randint(0,len(persona)-1))
        num2=int(random.randint(0,len(persona)-1))
        if int(nuevo[num1])==int(nuevo[num2]) or num1==num2:
            c=1
        if c==0:
            nuevo[num1]=control[num2]
            nuevo[num2]=control[num1]
            i=i+1
        tiro=1+tiro
        if tiro==200:
            print("help")
            print(nuevo)
        if recorrido(persona,cities)<=recorrido(nuevo,cities):
            prob=random.random()
            if prob > pmut:
                nuevo=persona.copy()
                
    return nuevo


#Ciudades,poblacion y número de generaciones a correr 
cities=defciudades(100)
gente=poblacion(25,100,cities)
gen=40000


#Posiciones iniciales graficadas
fig = plt.figure()
for i in cities:
    plt.scatter(i[0],i[1])
fig.savefig("Posiciones iniciales")
fig = plt.figure()
x=np.zeros(101)
y=np.zeros(101)


control=0
ajustep=[]
#Codigo que se encarga de correr cada generacion
for i in range(gen+1):
    genact=gente.copy()
    nuevo=gente.copy()
    minimos=recmin(genact,cities)
    index=0
    if i%1000==0:
      creargraf(minimos[1],minimos[0],cities,i)
      print(i)
    ajustep.append(1/minimos[0])
    for j in gente:
        if index==0 or index==1:
            genact[index]=minimos[1]
        elif index !=0 and index !=1:
            nuevo[index]=mutpersona(genact[index].copy(),cities).copy()
            genact[index]=nuevo[index].copy()
        index=index+1
    gente=genact.copy()

#Se crea el grafico de evolucion del ajuste
X=np.linspace(0,gen,len(ajustep))
fig = plt.figure()
plt.plot(X,ajustep)
fig.savefig("evolucion del ajuste")
  
    




        
    
