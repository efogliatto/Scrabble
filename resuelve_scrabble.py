import scrabble as sc

import argparse


if __name__ == "__main__":


    # Argumentos de consola
    
    parser = argparse.ArgumentParser(description='Resolución de scrabble')

    parser.add_argument("--fichas", help="Impresión de las fichas, sin resolución del juego", action = "store_true")

    parser.add_argument("--lan", help="Idioma", choices = ['es', 'en', 'it', 'fr', 'ar'], default = 'es')

    parser.add_argument("secuencia", help="Secuencia de letras", default = '')

    parser.add_argument("-n", help="Cantidad de secuencias aleatorias", default = 0)
    
    
    args = parser.parse_args()



    # Muestra las fichas
    
    if args.fichas:

        sc.diagrama( args.lan )


    # Resuelve para una secuencia por consola

    elif args.n == 0:

        result, msg = sc.juego( args.secuencia, args.lan )
        
        print( msg )
        


    # Resuelve para n secuencias aleatorias

    else:

        pass


