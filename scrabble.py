import fichas_scrabble as fch

import matplotlib.pyplot as plt

import numpy as np

import gzip, random









def fichas_lan( lan = 'es' ):

    """
    Selecci\'on de fichas de acuerdo al idioma
    """

    fichas = {}

    alphabet = ''

    
    if lan == 'es':

        fichas = fch.fichas_es

        alphabet = ['a','b','c','ch','d','e','f','g','h','i','j','l','ll','m','n','ñ','o','p','q','r','rr','s','t','u','v','x','y','z']

        
    elif lan == 'en' :

        fichas = fch.fichas_en

        alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']        



    return fichas, alphabet









def diagrama( lan = 'es', out = '' ):

    
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


    for k in alphabet:

        for i in range( fichas[k][0] ):

            idx = idx + 1

            if idx > nx-1:

                idx = 0

                idy = idy + 1


            # Posicion de la ficha
                
            ax.text( 0.5 + idx, ny - 0.5 - idy, k.upper(), ha="center", va="center", size = 15, fontweight = 'bold' )

                
            # Valor de la ficha
                
            ax.text( 0.8 + idx, ny - 0.8 - idy, fichas[k][1], ha="center", va="center", size = 5, fontweight = 'bold' )
                
                



    if not out:
    
        plt.show()

    else:

        plt.savefig( out )
        

        
    
    pass





def countLetters( word, lan = 'es' ):

    """
    Conteo de letras en word y asignacion a diccionario

    Devuelve diccionario con cantidad de apariciones
    """


    # Cuenta las letras de manera individual
    
    count = {}

    for w in word:

        if w.lower() in count.keys():

            count[w.lower()] = count[w.lower()] + 1

        else:

            count[w.lower()] = 1
            


    # En el caso de idioma espanol, correccion por ch, ll y rr. Como solo hay una ficha de estas, se corrige por una unica aparicion
    # Por ejemplo, si aparece 'ch' se agrega esta entrada al diccionario y resta una cuenta a 'c' y 'h'

    if lan == 'es':


        if 'ch' in word:

            count['ch'] = 1

            count['c'] = count['c'] - 1

            if count['c'] == 0:

                count.pop('c')

            count['h'] = count['h'] - 1

            if count['h'] == 0:

                count.pop('h')


        if 'rr' in word: 

            count['rr'] = 1

            count['r'] = count['r'] - 2

            if count['r'] == 0:

                count.pop('r')


            
        if 'll' in word:

            count['ll'] = 1

            count['l'] = count['l'] - 2

            if count['l'] == 0:

                count.pop('l')
            

            
    return count





def checkSec( sec, lan = 'es' ):

    """
    Verificaci\'on de la secuencia de letras
    Cuenta cantidad de caracteres y si pertenecen al alfabeto correcpondiente
    Para el caso espanol, asume que si aparece por ej. 'ch', se toma como 'ch' y no como 'c' y 'h'

    Devuelve la secuencia correcta y un mensaje
    El mensaje esta vacio si la secuencia es correcta
    """
    

    # Remocion de comas

    newSec = sec.replace(',','').lower()


    
    msg = ''



    
    # Deteccion de cantidad incorrecta de caracteres. Hay que tener precaucion con los caracteres dobles del espanol

    if lan == 'en':

        if len(newSec) != 7:

            msg = msg + '  [ERROR]  Cantidad incorrecta de caracteres\n\n'


    else:

        count = 0

        # if 'ch' in newSec:

        #     count = count + 1

        # if 'll' in newSec:

        #     count = count + 1

        # if 'rr' in newSec:

        #     count = count + 1



        if (len(newSec) - count) != 7: 

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













def juego( secDict, lan = 'es' ):


    """
    Resolucion del juego en idioma lan, usando las letras del diccionario secDict

    Devuelve mensaje con info
    """

    # newSec, msg = checkSec(sec, lan)
    msg = ''

    
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

                
        
        for w in words:

            count = 0

            find = True

            wDict = countLetters( w.decode(), lan )


            for l in wDict.keys():

                if l in secDict.keys():

                    if secDict[l] >= wDict[l]:
                        
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






def secuencia_rnd( lan = 'es' ):

    
    """
    Determina n secuencias aleatorias
    
    Si durante el sorteo se elige una ficha 'blank', entonces se agregan todas las letras del alfabeto (para pedir su resolucion posterior)
    """

    
    fichas, alphabet = fichas_lan( lan )


        
    # Acomodan las fichas por secuencia

    chain = []
    
    for k in sorted( fichas.keys(), key=lambda word: [alphabet.index(c) for c in word[0]] ):

        for rep in range( fichas[k][0] ):

            chain.append(k)



    # Posiciones enteras aleatorias no repetidas

    rnd = []

    while( len(rnd) < 7 ):

        num = random.randint(0, len(chain) - 1)

        if not num in rnd:

            rnd.append(num)


            
    # Secuencia aleatoria

    sec = []

    for r in rnd:

        sec.append( chain[r] )




        
    # Verificacion de posicion de 'blank'

    bpos = []
    
    for i, s in enumerate(sec):

        if s == 'blank':

            bpos.append(i)


            
    # Incorporacion de la secuencia sin 'blank'

    rndSec = []
    
    if not bpos:

        str = ''

        for s in sec:

            str = str + s
            
        rndSec.append(str)



    # Aparicion simple de blank

    elif len(bpos) == 1:

        nsec = sec

        for c in alphabet:

            nsec[ bpos[0] ] = c

            str = ''

            for s in nsec:

                str = str + s
            
                rndSec.append(str)


    # Doble aparicion de blank
                
    elif len(bpos) == 2:

        nsec = sec

        for c in alphabet:

            nsec[ bpos[0] ] = c


            for cc in alphabet:

                nsec[ bpos[1] ] = cc
                

                str = ''

                for s in nsec:

                    str = str + s
            
                    rndSec.append(str)


        
        
    return rndSec
