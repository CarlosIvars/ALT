# AUTORES:
# (poner aquí el nombre o 2 nombres del equipo de prácticas

def exact_cover(listaConjuntos, U=None):

    # permitimos que nos pasen U, si no lo hacen lo calculamos:
    if U is None:
        U = set().union(*listaConjuntos) 
        
    
    def backtracking(sol, cjtAcumulado):
        # consulta los métodos isdisjoint y union de la clase set,
        # podrías necesitarlos
        if len(sol) == len(listaConjuntos): #condicion de completitud
            if cjtAcumulado == U: #condicion de factibilidad
                yield sol.copy()
        else:
            cjt=listaConjuntos[len(sol)] #el conjunto a considerar ahora
            #ramificar,hemos desenrollado los 2 casos:
            #caso 1      
            if cjt.isdisjoint(cjtAcumulado):
                aux = cjtAcumulado
                sol.append(1)
                yield from backtracking(sol, cjtAcumulado.union(cjt)) 
                sol.pop()
                cjtAcumulado = aux

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
    
    datos = [{1,2,3},{2,3,4},{4,5},{1,5},{2,3}]
    
    for solucion in exact_cover(listaConjuntos):
        res = []
        for index,elem in enumerate(solucion):
            if elem == 1:
                res.append(listaConjuntos[index])
        print(res)
        
