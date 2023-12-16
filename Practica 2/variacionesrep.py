# AUTORES:
# Álvaro Garabal Castro, Carlos Ivars Ferrer

def variacionesRepeticion(elementos, cantidad):
    
    def backtracking(sol):
        if len(sol) == cantidad:
            yield sol.copy()
        else:
            for opcion in elementos:
                #condición de prometedor
                if opcion not in sol:
                    sol.append(opcion)
                    yield from backtracking(sol)
                    sol.pop()
                
    yield from backtracking([])

def combinaciones(elementos, cantidad):
    
    def backtracking(sol,i):
        if len(sol) == cantidad:
            yield sol.copy()
        else:
            #ramificamos con elementos posteriores
            for opcion in elementos[i:]:
                #condición de prometedor
                if opcion not in sol:
                    #obtencion de ínidice en la lista de elementos
                    indice = elementos.index(opcion)
                    sol.append(opcion)
                    yield from backtracking(sol,indice)
                    sol.pop()
                
    yield from backtracking([],0)

# COMPLETAR las actividades 1 y 2 para permutaciones y combinaciones
    
if __name__ == "__main__":
    for n in (1,2,3):
        print('Variaciones con repeticion n =',n)
        for x in variacionesRepeticion(['tomate','queso','anchoas'],n):
            print(x)

    print('Combinaciones con combinacion n =',3)
    for x in combinaciones(['tomate','queso','anchoas','aceitunas'],3):
        print(x)

    # probar las actividades 1 y 2 para permutaciones y combinaciones
