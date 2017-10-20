import fichas_scrabble as fch

import matplotlib.pyplot as plt

import numpy as np

import gzip









def fichas_lan( lan = 'es' ):

    """
    Selecci\'on de fichas de acuerdo al idioma
    """

    fichas = {}

    alphabet = ''

    
    if lan == 'es':

        fichas = fch.fichas_es
        
        alphabet = 'abcdefghijklmnñopqrstuvwxyz'

        
    elif lan == 'en' :

        fichas = fch.fichas_en

        alphabet = 'abcdefghijklmnopqrstuvwxyz'                



    return fichas, alphabet









def diagrama( lan = 'es' ):

    
    """
    Creaci\'on del diagrama con las fichas de scrabble
    """

    # Seleccion de fichas de acuerdo al idioma

    fichas, alphabet = fichas_lan( lan )




    # Seleccion del ancho del casillero

    N = 0

    for key in fichas:

        if fichas[key] != 'blank':

            N = N + fichas[key][0]


    nx = int(  np.ceil( np.sqrt(N) )  )

    ny = nx
    
    if (nx * ny - nx) > N:

        ny = ny - 1

    
        

    # Creacion de la figura inicial

    fix, ax = plt.subplots()

    ax.axis( 'off' )

    ax.set_xlim((0,nx))

    ax.set_ylim((0,ny))

    plt.gca().set_aspect('equal', adjustable='box')

    ax.set_xticks([])

    ax.set_yticks([])
    



    # Lineas verticales

    for i in range(nx+1):

        ax.axvline( i, color = 'silver' )

        ax.axhline( i, color = 'silver' )






    idx = -1

    idy = 0

    
    for k in sorted( fichas.keys(), key=lambda word: [alphabet.index(c) for c in word[0]] ):

    # for k in sorted( fichas.keys() ):

        if k != 'blank' :

            for i in range( fichas[k][0] ):

                idx = idx + 1

                if idx > nx-1:

                    idx = 0

                    idy = idy + 1


                # Posicion de la ficha
                
                ax.text( 0.5 + idx, ny - 0.5 - idy, k.upper(), ha="center", va="center", size = 15, fontweight = 'bold' )

                
                # Valor de la ficha
                
                ax.text( 0.8 + idx, ny - 0.8 - idy, fichas[k][1], ha="center", va="center", size = 5, fontweight = 'bold' )
                
                


    
    plt.show()
    

        
    
    pass







def checkSec( sec, lan = 'es' ):

    """
    Verificaci\'on de la secuencia de letras

    Devuelve la secuencia correcta y un mensaje
    """
    

    # Remocion de comas

    newSec = sec.replace(',','').lower()


    
    msg = ''

    # Deteccion de caracteres faltantes

    if len(newSec) < 7:

        msg = msg + '  [ERROR]  Cantidad incorrecta de caracteres\n\n'


        

    # Deteccion de caracteres incorrectos (de acuerdo al idioma)

    msg2 = ''

    fichas, alphabet = fichas_lan( lan )

    for c in newSec:

        if c not in alphabet:

            msg2 = msg2 + ' ' + c



    if msg2:

        msg = msg + '  [ERROR]  Caracteres incorrectos para el idioma ' + lan + ':' + msg2 + '\n\n'


        
    return newSec, msg






def countLetters( word ):

    """
    Conteo de letras en word y asignacion a diccionario

    Devuelve diccionario con cantidad de apariciones
    """
    
    count = {}

    for w in word:

        if w.lower() in count.keys():

            count[w.lower()] = count[w.lower()] + 1

        else:

            count[w.lower()] = 1
            

    return count






def juego( sec, lan = 'es' ):


    """
    Resolucion del juego en idioma lan, usando las letras de la secuencia sec

    Devuelve mensaje con info
    """

    newSec, msg = checkSec(sec, lan)
    

    
    # Resolucion del juego si no hay mensaje de error

    result = {}


    # Lectura de la lista de palabras
    
    if not msg:

        
        if lan == 'es':

            with gzip.open('palabras.words.gz', 'rb') as f:
                
                words = f.read().splitlines()

                

        elif lan == 'en':

            with gzip.open('palabras_en.words.gz', 'rb') as f:
                
                words = f.read().splitlines()

                

        else:

            msg = msg + '  [ERROR]  Idioma ' + lan + ' no disponible\n\n'





    # B\'usqueda de palabras
 
    if not msg:

        
        secDict = countLetters( sec )
        
        
        for w in words:

            count = 0

            find = True

            wDict = countLetters( w.decode() )


            for l in wDict.keys():

                if l in secDict.keys():

                    if secDict[l] >= wDict[l]:

                        # print('{}  {}  {}  {}'.format(secDict,wDict,l, w))
                        
                        count = count + 1

                    else:

                        find = False

                        
                        
                else:

                    find = False



                    
            # Si la cantidad de letras coincidentes es mayor a dos, y todas las letras de wDict estan en secDict, entonces la palabra w es valida
                    
            if count > 1  and  find == True:


                # Puntaje para la palabra

                score = 0

                fichas, alphabet = fichas_lan( lan )

                for l in wDict.keys():

                    score = score + fichas[l][1] * wDict[l]

                
                
                msg = msg + '{} : {} puntos\n'.format(w.decode(), score)

                result[w.decode()] = score

                    
            
        


        



    return result, msg






# def secuencia_rnd( lan = 'es', n = 1 ):

#     """
#     Determina n secuencias aleatorias
    
#     Si durante el sorteo se elige una ficha 'blank', entonces se agregan todas las letras del alfabeto (para pedir su resolucion posterior)
#     """

#     fic
    
    
