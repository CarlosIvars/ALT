# AUTORES:
# (poner aquí el nombre o 2 nombres del equipo de prácticas

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

# COMPLETAR las actividades 1 y 2 para permutaciones y combinaciones
    
if __name__ == "__main__":
    for n in (1,2,3):
        print('Variaciones con repeticion n =',n)
        for x in variacionesRepeticion(['tomate','queso','anchoas'],n):
            print(x)

    # probar las actividades 1 y 2 para permutaciones y combinaciones
