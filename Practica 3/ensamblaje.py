import numpy as np
import heapq
import collections
import argparse

######################################################################
#
#                     GENERACIÓN DE INSTANCIAS
#
######################################################################

def genera_instancia(M, low=1, high=4, seed=42):
    np.random.seed(seed)
    return np.random.randint(low=low,high=high,
                             size=(M,M),dtype=int)

######################################################################
#
#                       ALGORITMOS VORACES
#
######################################################################

def compute_score(costMatrix, solution):
    return sum(costMatrix[pieza,instante]
               for pieza,instante in enumerate(solution))

def naive_solution(costMatrix):
    solution = list(range(costMatrix.shape[0]))
    return compute_score(costMatrix,solution), solution

def voraz_x_pieza(costMatrix):
 # costMatrix[i,j] el coste de situar pieza i en instante j
    #M = costMatrix.shape[0] # nº piezas

    # costMatrix[i,j] es el costo de situar la pieza i en el instante j
    M = costMatrix.shape[0]  # número de piezas
    N = costMatrix.shape[1]  # número de instantes

    solution = []
    score = 0
    usadas = set()
    #para cada pieza
    for fila in range(M):
        #extraemos piezas posibles
        valores_piezas_posibles = [valor for index, valor in enumerate(costMatrix[fila]) if index not in usadas]
        #coges el minimo de las piezas posibles
        minValor = min(valores_piezas_posibles)
        #Escoges las piezas cuyo valor es igual a min valor y no se encuentre en la lista de usadas
        piezas_posibles = [ index for index, x  in enumerate(costMatrix[fila]) if x == minValor and index not in usadas]
        #De las posibles piezas a añadir, escogemos la primera posible y la añadimos a la solucion
        score += minValor
        usadas.add(piezas_posibles[0])
        solution.append(piezas_posibles[0])
    return score, solution

def voraz_x_instante(costMatrix):
     # costMatrix[i,j] el coste de situar pieza i en instante j
    M = costMatrix.shape[0] # nº piezas
    N = costMatrix.shape[1] # nº tiempos
    solution = [None] * M
    usadas = set()
    score = 0
    #para cada instante de tiempo
    for columna in range(N):
            #creamos un array con el istante columna para cada una de las filas (coger la columna x de la tabla)
            instantes_posibles =  np.array([fila[columna] for fila in costMatrix])
            #peor de los casos
            best_score = np.inf
            #para cada pieza de las posibles
            for pieza in range(M):
                #si no esta en usadas
                if pieza not in usadas: 
                    #si el valor de esa pieza en el instante es menor al mejor score
                    if instantes_posibles[pieza] < best_score:
                        #actualizamos el best score y la pieza candidata a ser usada
                        best_score  = instantes_posibles[pieza]
                        pieza_usada = pieza
            #añadimos a la solucion
            solution[pieza_usada] = columna
            score += best_score
            usadas.add(pieza_usada)
        

    return score,solution

def voraz_x_coste(costMatrix):
    # costMatrix[i,j] el coste de situar pieza i en instante j
    M = costMatrix.shape[0] # nº piezas
    # COMPLETAR
    #Creación de tripletas  (coste, pieza, instante)
    tripletas = [(costMatrix[i][j], i, j) for i in range(M) for j in range(M)]
    #ordenamos las tripletas por coste
    tripletas.sort()

    i_usadas = set()
    p_usadas = set()
    score =  0
    solution = [0] * M
    #para cada tripleta
    for tripleta in tripletas:
        #si la el instante(tripleta[2]) no esta usado y la pieza tampoco esta en uso
        if tripleta[2] not in i_usadas and tripleta[1] not in p_usadas:
            #añandimos esa pieza a la solucion
            i_usadas.add(tripleta[2])
            p_usadas.add(tripleta[1])
            solution[tripleta[1]] = tripleta[2]
            score += tripleta[0]

    return score,solution

def voraz_combina(costMatrix):
    
    # COMPLETAR
    #sacamos el coste y la solucion de cada uno de los voraces y extraemos el minimo
    cp ,sp = voraz_x_pieza(costMatrix)
    ci, si = voraz_x_instante(costMatrix)
    cc, sc = voraz_x_coste(costMatrix)
    score = min(cp,ci,cc)
    #vemos que solucion coincide con el valor del score
    solution = sp if score == cp else (si if score == ci else sc) 
    
    return score,solution
        
######################################################################
#
#                       RAMIFICACIÓN Y PODA
#
######################################################################

class Ensamblaje:

    def __init__(self, costMatrix, initial_sol = None):
        '''
        costMatrix es una matriz numpy MxM con valores positivos
        costMatrix[i,j] es el coste de ensamblar la pieza i cuando ya
        se han ensamblado j piezas.
        '''
        # no haría falta pero por si acaso comprobamos que costMatrix
        # es una matriz numpy cuadrada y de costMatrix positivos
        assert(type(costMatrix) is np.ndarray and len(costMatrix.shape) == 2
               and costMatrix.shape[0] == costMatrix.shape[1]
               and costMatrix.dtype == int and costMatrix.min()>=0)
        self.costMatrix = costMatrix
        self.M = costMatrix.shape[0]
        # la forma más barata de ensamblar la pieza i si podemos
        # elegir el momento de ensamblaje que más nos convenga:
        self.minPieza = [costMatrix[i,:].min() for i in range(self.M)]
        self.x = initial_sol
        if initial_sol is None:
            self.fx = np.inf
        else:
            self.fx = compute_score(costMatrix,initial_sol)
        
    def branch(self, s_score, s):
        '''
        s_score es el score de s
        s es una solución parcial
        '''
        i = len(s) # i es la siguiente pieza a montar, i<M
        
        # costMatrix[i,j] coste ensamblar objeto i en instante j
        for j in range(self.M): # todos los instantes
            # si j no ha sido utilizado en s
            if j not in s: # NO es la forma más eficiente
                           # al ser lineal con len(s)
                new_score = s_score - self.minPieza[i] + self.costMatrix[i,j]
                yield (new_score, s + [j])

    def is_complete(self, s):
        '''
        s es una solución parcial
        '''
        return len(s) == self.M

    def initial_solution(self):
        return (sum(self.minPieza),[])

    def solve(self):
        A = [ self.initial_solution() ] # cola de prioridad
        iterations = 0 # nº iteraciones
        gen_states = 0 # nº estados generados
        podas_opt  = 0 # nº podas por cota optimista
        maxA       = 0 # tamaño máximo alzanzado por A
        # bucle principal ramificacion y poda (PODA IMPLICITA)
        while len(A)>0 and A[0][0] < self.fx:
            iterations += 1
            lenA = len(A)
            maxA = max(maxA, lenA)
            s_score, s = heapq.heappop(A)
            for child_score, child in self.branch(s_score, s):
                gen_states += 1
                if self.is_complete(child): # si es terminal
                    # es factible (pq branch solo genera factibles)
                    # falta ver si mejora la mejor solucion en curso
                    if child_score < self.fx:
                        self.fx, self.x = child_score, child
                else: # no es terminal
                    # lo metemos en el cjt de estados activos si
                    # supera la poda por cota optimista:
                    if child_score < self.fx:
                        heapq.heappush(A, (child_score, child) )
                    else:
                        podas_opt += 1
                        
        stats = { 'iterations':iterations,
                  'gen_states':gen_states,
                  'podas_opt':podas_opt,
                  'maxA':maxA}
        return self.fx, self.x, stats

def functionRyP(costMatrix):
    e = Ensamblaje(costMatrix)
    fx,x,stats = e.solve()
    return fx,x

######################################################################
#
#                        EXPERIMENTACIÓN
#
######################################################################

cjtAlgoritmos = {'naif': naive_solution,
                 'x_pieza': voraz_x_pieza,
                 'x_instante': voraz_x_instante,
                 'x_coste': voraz_x_coste,
                 'combina': voraz_combina,
                 'RyP': functionRyP}


def probar_ejemplo():
    ejemplo = np.array([[7, 3, 7, 2],
                        [9, 9, 4, 1],
                        [9, 4, 8, 1],
                        [3, 4, 8, 4]], dtype=int)
    
    for label,function in cjtAlgoritmos.items():
        score,solution = function(ejemplo)
        print(f'Algoritmo {label:10}', solution, score)

def comparar_algoritmos(root_seed, low, high):
    print('talla',end=' ')
    for label in cjtAlgoritmos:
        print(f'{label:>10}',end=' ')
    print()
    numInstancias = 10
    for talla in range(5,15+1):
        dtalla = collections.defaultdict(float)

        np.random.seed(root_seed)
        seeds = np.random.randint(low=0, high=9999, size=numInstancias)

        for seed in seeds:
            cM = genera_instancia(talla, low=low, high=high, seed=seed)
            for label,function in cjtAlgoritmos.items():
                score,solution = function(cM)
                dtalla[label] += score

        print(f'{talla:>5}',end=' ')
        for label in cjtAlgoritmos:
            media = dtalla[label]/numInstancias
            print(f'{media:10.2f}', end=' ')
        print()

def comparar_sol_inicial(root_seed, low, high):
    # COMPLETAR
    
    #primeras estadísticas
    print('talla',end=' ')
    #imprimir titulos de las columnas
    for label in cjtAlgoritmos:
        print(f'{label:>10}',end=' ')
    print()
    #numero de instancias a establecer
    numInstancias = 10
    #Por cada talla 
    for talla in range(5,15+1):
       #creamos un diccionario para guardar las estadisticas
        dtalla = collections.defaultdict(float)

        #cogemos una semilla
        np.random.seed(root_seed)
        seeds = np.random.randint(low=0, high=9999, size=numInstancias)
        #para cada semilla 
        for seed in seeds:
            #creamos una instancia
            cM = genera_instancia(talla, low=low, high=high, seed=seed)
            for label,function in cjtAlgoritmos.items():
                score,solution = function(cM)
                #añadimos al diccionario la score en la entrada labal(nombre de la columna)
                dtalla[label] += score
    #imprimimps los valores del diccionario haciendo la media para cada columna
        print(f'{talla:>5}',end=' ')
        for label in cjtAlgoritmos:
            media = dtalla[label]/numInstancias
            print(f'{media:10.2f}', end=' ')
        print()
    print()
        
    #iteramos sobre las estadísticas a ver, nueva parte
    estadisticas = ['iterations', 'gen_states', 'podas_opt', 'maxA']
    for estadistica in estadisticas:
        print(f'{" " + estadistica + " ":-^100}')
        print('talla',end=' ')
        
        for label in cjtAlgoritmos:
            print(f'{label + "+RyP" if label != "RyP" else "RyP":>15}',end=' ')         
        print()
        
        numInstancias = 10
        
        for talla in range(5,15+1):
            dtalla = collections.defaultdict(float)

            np.random.seed(root_seed)
            seeds = np.random.randint(low=0, high=9999, size=numInstancias)

            for seed in seeds:
                cM = genera_instancia(talla, low=low, high=high, seed=seed)                   
                for label,function in cjtAlgoritmos.items():
                    
                    intial_c, initial_sol = function(cM)
                    #si es RyP no hagas solucion inicial  
                    if label == 'RyP':
                        initial_c, initial_sol = np.inf, None
                    
                    problema = Ensamblaje(cM, initial_sol)
                    fx, x, stats = problema.solve()
                    dtalla[label] += stats[estadistica]

            print(f'{talla:>5}',end=' ')
            for label in cjtAlgoritmos:
                media = dtalla[label]/numInstancias
                print(f'{media:>15.2f}', end=' ')           
            print()
        print()
    
def probar_ryp():
    ejemplo = np.array([[7, 3, 7, 2],
                        [9, 9, 4, 1],
                        [9, 4, 8, 1],
                        [3, 4, 8, 4]], dtype=int)
    # scorevoraz, solvoraz = voraz_combina(ejemplo)
    # bb = Ensamblaje(ejemplo, solvoraz)
    bb = Ensamblaje(ejemplo)
    fx, x, stats = bb.solve()
    print(x,fx,compute_score(ejemplo,x))
    print(stats)

######################################################################
#
#                             PRUEBAS
#
######################################################################
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Soluciones iniciales voraces al problema del ensamblaje por RyP.')
    
    parser.add_argument('-S', '--seed', dest='seed', action='store', type=int, default=42, 
                        help='Semilla para la generación de instancias.')
    
    parser.add_argument('-L', '--low', dest='low', action='store', type=int, default=1, 
                        help='Valor inferior para generación de instancias.')
    
    parser.add_argument('-H', '--high', dest='high', action='store', type=int, default=4, 
                        help='Valor superior (no incluído) para generación de instancias.')

    parser.add_argument('-R', '--ryp', dest='ryp', action='store_true', default=False, 
                        help='Prueba RyP.')

    parser.add_argument('-A', '--algoritmos', dest='algoritmos', action='store_true', default=False, 
                        help='Comparar algoritmos voraces con RyP.')
    
    parser.add_argument('-I', '--inicial', dest='inicial', action='store_true', default=False, 
                        help='Comparar soluciones iniciales voraces en RyP.')

    args = parser.parse_args()

    SEED = args.seed
    LOW  = args.low
    HIGH = args.high

    if args.ryp:
        probar_ryp()
        
    if args.algoritmos:
        comparar_algoritmos(root_seed=SEED, low=LOW, high=HIGH)
        
    if args.inicial:
        comparar_sol_inicial(root_seed=SEED, low=LOW, high=HIGH)

