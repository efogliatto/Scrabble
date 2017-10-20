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


    

    # Muestra las fichas
    
    if args.fichas:

        sc.diagrama( args.lan, args.o )


        

    # Resuelve para una secuencia por consola

    elif args.n == 0:
        
        result, msg = sc.juego( args.secuencia, args.lan )

        if not args.o:
        
            print( msg )

        else:

            with open( args.o, 'w' ) as f:

                f.write( msg )
            

        

    # Resuelve para n secuencias aleatorias

    else:

        global_result = {}

        for n in range( args.n ):
        
            rndSec = sc.secuencia_rnd( args.lan )
            
        
            for sec in rndSec:

                result, msg = sc.juego( sec, args.lan )

                
                # Se agrega solo el maximo puntaje para esta secuencia

                if result:
                    
                    global_result[ sec ] = sorted(result.items(), key = lambda x : x[1], reverse = True)[0]




        msg = ''
                    
        for key in global_result:

            msg = msg + '{} : {}\n'.format(key, global_result[key])

                

        if not args.o:
        
            print( msg )

        else:

            with open( args.o, 'w' ) as f:

                f.write( msg )            


