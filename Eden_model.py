###                CODI PEL MODEL DE EDEN
#----------------------------------------------------------
# Comencem amb el import dels moduls que utilizarem:
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import copy
import random
#Aqui hauria d'anar el import del scipy, pero encara no tinc clar exactament
#quin submodul del scipy ens interessa importar, ja que no es recomana utili-
#tzar mai 'import scipy', perque això només dona la funcionalitat de 'numpy',
#algo que directament ja hem fet amb 'import numpy'.

#When will we consider that the simulation has ended?
#When all the positions in the colony have been occupied?

# Definim la colony. 1's pels estats buits, 0 pels estats ocupats. Tindrà size
# LxL:
L = 40
# La colonia està inicialment completament buida:
colony = np.ones((L,L), dtype = int)

#Hem d'introduir les coordenades de cada punt de la colonia (x,y) per tal de
#controlar els bacteris. Ho farem suposant que la part inferior esquerra del
#quadrat LxL té coordenades (0,0). Donat que les coordenades en sí de la
#colonia no canvien, sino que ho fa la seva ocupació, podem introduir aquestes
#coordenades mitjançant tuples:
col_coord = np.array([[(i, j) for j in range(L)] for i in range(L)])

#We have to define the position of the first bacteria. We will choose this
#randomly. Before we can do this we have to define a set of active sites.
#It is useful to define a set beacuse this allows to easily remove and add
#elements,avoiding multiple instances of the same active site. This set will
#initialy be empty:
active_coord = set()

#Now we add the first active position:
x_first = np.random.randint(0,L)
y_first = np.random.randint(0,L)
active_coord.add((x_first,y_first))
colony[x_first,y_first] = 0 #Perque ara aquesta posició està ocupada.

#Amb aquesta informació ja casi podem començar les iteracions en les que es va
#afegint un bacteri més. Ens queda definir una funció en la que es computin els
#veins d'una certa posició en la colonia, tenint en compte de no considerar com
#a veins posicions fora de la colonia, ja que volem utilitzar condicions de
#contorn tancades.
#Aquestes posicions les ha de computar, clar, per les active_coord, però això
#ja es definirà després en el bucle, aquí simplement hem de considerar una
#dummy coordinate, que no necessitem saber d'on prové.

def func_veins(coord,LL):
    #Transformem 'cord' en una llista per poder manipular-la més fàcilment:
    #veins_coord = [up, down, left, right]
    veins_coord =[]
    if coord[1]+1<=LL-1:
        veins_coord.append((coord[0],coord[1]+1))
    if coord[1]-1>=0:
        veins_coord.append((coord[0],coord[1]-1))
    if coord[0]-1>=0:
        veins_coord.append((coord[0]-1,coord[1]))
    if coord[0]+1<=LL-1:
        veins_coord.append((coord[0]+1,coord[1]))
    #I ara ja tenim els veins que estan dintre de la colonia:
    return veins_coord



#Ara ja si que podem començar els bucles per afegir bacteris.Per fer això hem
#de definir el bucle tal que acabi quan totes les posicions estiguin ocupades.
#Per fer això podem fer:
n = 1 # Ho utilizarem per veure si ha fet totes les iteracions que toquen.
      # Bàsicament n és una variable de control.
while n < 500:
    #1. Hem de guardar en una llista les posicions no ocupades dels veins de les
    #   posicions actives.
    #1.a) Per fer això primer simplement calculem les posicions veines de les
    #     posicions actives, sense preocupar-nos de si estan ocupades.
    veins = [] #La inicialitzem buida.
    for i in range(len(active_coord)):
        one_active_coord = list(active_coord)[i]
        veins_function = func_veins(one_active_coord,L)
        veins = veins + veins_function
    #Ho convertim en un set per eliminar els duplicats i ho tornem a
    #convertir en llista, per manipular-ho més fàcilment. Per fer això
    #abans hem de convertir les llistes dintre de la llista en tuples:
    veins = list(set(tuple(x) for x in veins))
    #1.b) Del set 'veins' hem d'eliminar les coordenades que ja estan ocupades:
        #act_veins = copy.deepcopy(veins)
    inact_veins = [veins[j] for j in range(len(veins)) if colony[veins[j]]==1]
    #for j in veins:
    #    act_veins = np.delete(act_veins,np.where(colony[j[0],j[1]]==0))
    #
    inact_veins = set(inact_veins)
    #2. Ara hem de escollir una coordenada aleatoria d'aquests veins i fer que
    #   una bacteria la ocupi.

    #Una opcio es new_active = random.choice(tuple(act_veins)), que ens dona
    #la sortida en tuple. Pero en la practica ens demana random.sample.
    #Un exemple de com funciona el random.sample es:
      #prov = [[0,0],[1,1],[2,2]]
      #print(prov)
      #act_veins1 = set(tuple(x) for x in prov)
      #print(act_veins1)
      #new_active = random.sample(act_veins1,1)
      #Lo de la linea anterior ens dona el tuple de coordenades dins una llista
      #Si volem simplement el tuple de coordenades hem de fer:
      #new_active = random.sample(act_veins1,1)[0]
      #print(new_active)
    #D'aquesta manera hem de fer:
    new_active = random.sample(inact_veins,1)[0]
    #
    #3. Ara que ja tenim la posicio a omplir, simplement la hem d'ocupar:
    colony[new_active] = 0
    active_coord.add(new_active)
    # I canviem 'n' per monitoritzar les iteracions realitzades:
    n = n + 1

#En principi, arribats a aquest punt el codi ja ha fet totes les iteracions
#fins a omplir tota la colonia:
print('RESULTATS')
print('---------')
print('first point')
print([x_first,y_first])
print('------------')
print('iterations')
print(n)

plt.imshow(colony, interpolation="none", cmap="gray")
