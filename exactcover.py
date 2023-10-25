# AUTORES:
# (poner aquí el nombre o 2 nombres del equipo de prácticas

def exact_cover(listaConjuntos, U=None):

    # permitimos que nos pasen U, si no lo hacen lo calculamos:
    if U is None:
        U = set().union(*listaConjuntos) 
        print("Universo = " + str(U))
    
    def backtracking(sol, cjtAcumulado):
        # consulta los métodos isdisjoint y union de la clase set,
        # podrías necesitarlos
        if len(sol) == len(listaConjuntos):
            print("ojo piojo\n")
            if cjtAcumulado == U:
                print("ole!\n")
                yield sol.copy()
        else:
            cjt=listaConjuntos[len(sol)] #el conjunto a considerar ahora
            #ramificar,hemos desenrollado los 2 casos:
            #caso 1
            print("sol = " + str(sol))
            print("cjt = " + str(cjt))
            print("cjtAc = " + str(cjtAcumulado)+"\n")
            if cjt.isdisjoint(cjtAcumulado):
                yield from backtracking(sol.append(1), cjtAcumulado.union(cjt))  
                sol.pop()
                cjtAcumulado.remove(cjt)
            #caso 2
            yield from backtracking(sol.append(0), cjtAcumulado)

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
