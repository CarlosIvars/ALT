# -*- coding: utf-8 -*-

# AUTORES:
# Álvaro Garabal Castro, Carlos Ivars Ferrer

import sys

def langford(N):
    N2   = 2*N
    seq  = [0]*N2
    def backtracking(num):
        if num<=0: #condicion de completitud y factibilidad
            yield "-".join(map(str, seq))
        else:
            #buscamos una posicion para situar una pareja num, ramificamos
            for i in range(N2-num-1): 
                    #posicion objetivo a rellenar    
                    j = i+num+1
                    #es valida es posicion?
                    if seq[i] == 0 and seq[j] == 0:
                        #efectuamos cambio
                        seq[i], seq[j] = num, num
                        if j-i-1 == num: #estado prometedor
                            yield from backtracking(num-1)
                        #deshacemos cambio en caso de fallo
                        seq[i], seq[j] = 0, 0
                    
                        
                        

    if N%4 in (0,3):
        yield from backtracking(N)
    ###modificacion mia
    else:
        print("No hay solución al problema")
if __name__ == "__main__":
    if len(sys.argv) not in (2,3):
        print('\nUsage: %s N [maxsoluciones]\n' % (sys.argv[0],))
        sys.exit()
    try:
        N = int(sys.argv[1])
    except ValueError:
        print('First argument must be an integer')
        sys.exit()
    numSolutions = None
    if len(sys.argv) == 3:
        try:
            numSolutions = int(sys.argv[2])
        except ValueError:
            print('Second (optional) argument must be an integer')
            sys.exit()

    i = 0
    for sol in langford(N):
        if numSolutions is not None and i>=numSolutions:
            break

        i += 1
        print(f'sol {i:4} ->',sol)
