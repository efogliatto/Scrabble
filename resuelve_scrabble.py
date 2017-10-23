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
    
    
    args = parser.parse_args()



    
    #########################
    
    # Solo muestra las fichas

    ########################

    
    if args.fichas:

        sc.diagrama( args.lan, args.o )


        

    #########################################

    # Resuelve para una secuencia por consola

    #########################################
    
    
    elif args.n == 0:

        
        # Convierte la secuencia a diccionario
        
        sdict, msg = sc.secToDict( args.secuencia, args.lan )

        
        # Resuelve si no hay mensaje de error
        
        if not msg:
        
            result, msg = sc.juego( sdict, args.lan )


        # Impresion de mensaje

        if not args.o:
        
            print( msg )

        else:

            with open( args.o, 'w' ) as f:

                f.write( msg )
            

                
                
        

    #######################################                
                
    # Resuelve para n secuencias aleatorias

    #######################################

        

    else:

        global_result = []

        
        for n in range( args.n ):

            global_result.append( ('','',0) )
            

            # Secuencia aleatoria (lista de secuencias si durante el sorteo salen fichas blank)
            
            rndSec = sc.secuencia_rnd( args.lan )
            

            # Resolucion para cada secuencia de la lista rndSec
            
            for sec in rndSec:

                result, msg = sc.juego( sec, args.lan )
                
                
                # Se agrega solo el maximo puntaje para esta secuencia

                if result:

                    maxitem = sorted(result.items(), key = lambda x : x[1], reverse = True)[0]
                    
                    if maxitem[1] >= global_result[-1][2]  :

                        global_result[-1] = ( sc.dictToSec(sec), maxitem[0], maxitem[1] )


                        
            

        msg = ''
                    
        for key in global_result:

            msg = msg + '{} : {} puntos\n'.format(key[0], key[2])

                

        if not args.o:
        
            print( msg )

        else:

            with open( args.o, 'w' ) as f:

                f.write( msg )            


