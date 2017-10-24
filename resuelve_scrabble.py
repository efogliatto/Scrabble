import scrabble as sc

import argparse


if __name__ == "__main__":


    
    # Argumentos de consola
    
    parser = argparse.ArgumentParser(description='Resolución de scrabble')

    parser.add_argument('-f','--fichas', help='Impresión de las fichas, sin resolución del juego', action = 'store_true', dest='fichas')

    parser.add_argument('-l','--language', help='Idioma', choices = ['es', 'en'], default = 'es', dest = 'lan')

    parser.add_argument('secuencia', help='Secuencia de letras', default = '', nargs = '?')

    parser.add_argument('-n', help='Cantidad de secuencias aleatorias', type = int, default = 0)

    parser.add_argument('-o', '--output', help='Salida opcional', default = '', dest = 'o')

    parser.add_argument('-s','--estadistica', help='Resuelve s secuencias aleatorias y realiza un hisograma', type = int, default = 0, dest = 's')
    
    
    args = parser.parse_args()

    
    # Si resuelve n veces, no se hace estadistica
    
    if args.n != 0:

        args.s = 0


        
    
    #########################
    
    # Solo muestra las fichas

    ########################

    
    if args.fichas:

        sc.diagrama( args.lan, args.o )


        

    #########################################

    # Resuelve para una secuencia por consola

    #########################################
    
    
    elif args.n == 0   and   args.s == 0 :

        
        # Convierte la secuencia a diccionario
        
        sdict, msg = sc.secToDict( args.secuencia, args.lan )

        
        # Resuelve si no hay mensaje de error
        
        if not msg:

            words = sc.readWords( args.lan )
        
            result, msg = sc.juego( sdict, words, args.lan )


        # Impresion de mensaje

        if not args.o:
        
            print( msg )

        else:

            with open( args.o, 'w' ) as f:

                f.write( msg )
            

                
                
        

    #######################################                
                
    # Resuelve para n secuencias aleatorias

    #######################################

        

    elif args.n != 0:


        global_result = []

        words = sc.readWords( args.lan )

        
        for n in range( args.n ):
            

            # Secuencia aleatoria (lista de secuencias si durante el sorteo salen fichas blank)
            
            rndSec = sc.secuencia_rnd( args.lan )
            

            # Resolucion para cada secuencia de la lista rndSec
            
            for sec in rndSec:

                result, msg2 = sc.juego( sec, words, args.lan )                            

                if result:

                    global_result = global_result + result



                        
            

        sorted_results = sorted(global_result, key=lambda x : x[1], reverse = True) 

        msg = '\n'        
        
        for elem in sorted_results:

            if elem[1] ==  sorted_results[0][1]:

                msg = msg + '{} : {} puntos\n'.format(elem[0], elem[1])

            else:

                break

                            

            
        if not args.o:
        
            print( msg )

        else:

            with open( args.o, 'w' ) as f:

                f.write( msg )            





    if args.s != 0:

        # Histograma. Puntaje total por tiro

        words = sc.readWords( args.lan )

        sc.hist_palabras( args.s, words, args.lan, args.o )
