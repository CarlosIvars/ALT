# AUTORES:
# Álvaro Garabal Castro, Carlos Ivars Ferrer

def exact_cover(listaConjuntos, U=None):

    # permitimos que nos pasen U, si no lo hacen lo calculamos:
    if U is None:
        U = set().union(*listaConjuntos) 
        
    
    def backtracking(sol, cjtAcumulado):
        # consulta los métodos isdisjoint y union de la clase set,
        # podrías necesitarlos
        if len(sol) == len(listaConjuntos): #condicion de completitud
            if cjtAcumulado == U:           #condicion de factibilidad
                #devolvemos los elementos que en el vector solcuión se encuentren a 1
                yield [v for v,s in zip(listaConjuntos,sol) if s==1]
        else:
            cjt=listaConjuntos[len(sol)]    #el conjunto a considerar ahora
            #caso 1      
            if cjt.isdisjoint(cjtAcumulado): #condicion de prometedor
                sol.append(1)
                yield from backtracking(sol, cjtAcumulado.union(cjt)) 
                sol.pop()
            #caso 2
            sol.append(0)
            yield from backtracking(sol, cjtAcumulado)
            sol.pop()

    yield from backtracking([], set())
    

if __name__ == "__main__":
    listaConjuntos = [{"casa","coche","gato"},
                      {"casa","bici"},
                      {"bici","perro"},
                      {"boli","gato"},
                      {"coche","gato","bici"},
                      {"casa", "moto"},
                      {"perro", "boli"},
                      {"coche","moto"},
                      {"casa"}]
    
    for solucion in exact_cover(listaConjuntos):
        print(solucion)
        
