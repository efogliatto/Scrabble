import fichas_scrabble as fch

import matplotlib.pyplot as plt

import numpy as np

import gzip, random

from matplotlib.ticker import MaxNLocator

import collections as col









def fichas_lan( lan = 'es' ):

    """
    Selecci\'on de fichas de acuerdo al idioma

    Devuelve las fichas y un alfabeto ordenado (por si se necesita algún odenamiento específico)
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

    fix, ax = plt.subplots(facecolor='white')

    ax.axis( 'off' )

    ax.set_xlim( (-1,nx+1) )

    ax.set_ylim( (-1,ny+1) )

    plt.gca().set_aspect('equal', adjustable='box')

    ax.set_xticks([])

    ax.set_yticks([])
    



    # Lineas verticales

    for i in range(nx+1):

        ax.vlines( i, color = 'silver', ymin = 0, ymax = ny )

        ax.hlines( i, color = 'silver', xmin = 0, xmax = nx )






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

    Devuelve diccionario con cantidad de apariciones por letra
    """


    # Cuenta las letras de manera individual
    
    count = {}

    for w in word:


        # Remocion de acentos para idioma espanol

        if lan == 'es':

            if w == 'á':

                w = 'a'

            if w == 'é':

                w = 'e'

            if w == 'í':

                w = 'i'                

            if w == 'ó':

                w = 'o'

            if w == 'ú':

                w = 'u'
        

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















def secToDict( sec, lan = 'es' ):

    
    """
    Verificaci\'on de la secuencia de letras
    Cuenta cantidad de caracteres y si pertenecen al alfabeto correcpondiente
    Para el caso espanol, asume que si aparece por ej. 'ch', se toma como 'ch' y no como 'c' y 'h'
    Como solo hay una ficha especial, se cuenta una vez

    Devuelve un diccionario con la cuenta de letras y un mensaje
    El mensaje esta vacio si la secuencia es correcta
    """
    

    # Remocion de comas

    newSec = sec.replace(',','').lower()
    
    msg = ''



    
    # Deteccion de caracteres incorrectos (de acuerdo al idioma)

    msg2 = ''

    fichas, alphabet = fichas_lan( lan )

    for c in newSec:

        if c not in alphabet:

            msg2 = msg2 + ' ' + c


    if msg2:

        msg = msg + '\n  [ERROR]  Caracteres incorrectos para el idioma ' + lan + ':' + msg2



        


    # Conversion a diccionario

    sdict = countLetters( newSec, lan )

    count = 0

    for key in sdict:

        count = count + sdict[key]
        

    if count != 7:
    
        msg = msg + '\n  [ERROR]  Cantidad incorrecta de caracteres'    
    


    if msg:

        msg = msg + '\n'
        
        
    return sdict, msg






def dictToSec( sdict ):

    """
    Toma un diccionario de letras, y devuelve un string
    """
    
    s = ''

    for key in sdict.keys():

        s = s + sdict[key] * key


    return s





def readWords( lan = 'es' ):

    """
    Lectura de la lista de palabras de diccionario.
    Conteo de letras por palabras y retorno en lista de diccionarios

    Devuelve lista de tuplas: (palabra segun idioma, diccionario de cuentas)
    """


    # Lectura de los diccionarios

    if lan == 'es':

        with gzip.open('palabras.words.gz', 'rb') as f:
                
            words = f.read().splitlines()
            

    elif lan == 'en':

        with gzip.open('palabras_en.words.gz', 'rb') as f:
                
            words = f.read().splitlines()



            
    wdict = []

    for w in words:

        wdict.append( (w.decode().lower(), countLetters( w.decode().lower(), lan )) )


        
    return wdict



            





def juego( secDict, words, lan = 'es' ):


    """
    Resolucion del juego en idioma lan, usando las letras del diccionario secDict

    Devuelve mensaje con info y lista de tuplas: (palabra, puntaje)
    """

    msg = '\n'

    
    # Resolucion del juego si no hay mensaje de error

    result = {}

              
        
    for word in words:

        count = 0

        find = True

        wDict = word[1]


        # La idea de resolucion es la siguiente: para cada palabra de words, se verifica que secDict contenga la cantidad de letras necesarias

        for l in wDict.keys():


            # Break para evitar busquedas innecesarias
            
            if find == False:

                break


            
            if l in secDict.keys():

                if secDict[l] >= wDict[l]:
                        
                    count = count + 1

                else:

                    find = False

                                                
            else:

                find = False



                    
        # Si todas las letras de wDict estan en secDict, entonces la palabra w es valida
                    
        if count > 1  and  find == True:
        

            # Puntaje para la palabra

            score = 0

            fichas, alphabet = fichas_lan( lan )

            for l in wDict.keys():

                score = score + fichas[l][1] * wDict[l]

                


            result[ word[0] ] = score




            
    # Ordenamiento de resultado, de mayor a menor puntaje

    ordResult = []
            
    for it in sorted(result.items(), key = lambda x : x[1], reverse = True):

        msg = msg + '{} : {} puntos\n'.format(it[0], it[1])

        ordResult.append(   ( it[0], it[1] )  )
            

        
    return ordResult, msg







def secuencia_rnd( lan = 'es' ):

    
    """
    Determina una secuencia aleatoria    
    Si durante el sorteo se eligen una fichas 'blank', entonces se agregan todas las letras del alfabeto (para pedir su resolucion posterior)

    Devuelve una lista de diccionarios, cada uno listo para usar en juego()
    """


    # Fichas para este alfabeto
    
    fichas, alphabet = fichas_lan( lan )


        
    # Se acomodan las fichas por secuencia

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




    # Generacion del diccionario inicial aleatorio

    sdict = {}

    for r in rnd:

        lt = chain[r]

        if lt in sdict.keys():

            sdict[lt] = sdict[lt] + 1

        else:

            sdict[lt] = 1





    # Verificacion de la existencia de fichas 'blank'

    rndSec = []

    

    # No hay fichas 'blank'
    
    if 'blank' not in sdict.keys():

        rndSec.append(sdict)

        

    else:

        # Copia de los elementos distintos de blank
        
        newSec = {}
        
        for key in sdict:

            if key != 'blank':

                newSec[key] = sdict[key]


                
                
        # 'blank' aparece solo una vez
                
        if sdict['blank'] == 1:
                

            # Agregamos una nueva letra del alfabeto

            for lt in alphabet:
            
                nndict = newSec.copy()

                if lt in nndict.keys():

                    nndict[lt] = nndict[lt] + 1

                else:

                    nndict[lt] = 1


                rndSec.append( nndict )
            

                

                
        # 'blank' aparece solo una vez
                
        elif sdict['blank'] == 2:
                

            # Agregamos una nueva letra del alfabeto

            for lt in alphabet:

                for nlt in alphabet:
            
                    nndict = newSec.copy()

                    if lt in nndict.keys():

                        nndict[lt] = nndict[lt] + 1

                    else:

                        nndict[lt] = 1

                        
                    if nlt in nndict.keys():

                        nndict[nlt] = nndict[nlt] + 1

                    else:

                        nndict[nlt] = 1


                    

                    rndSec.append( nndict )
                
        




        
        
    return rndSec







def hist_palabras( s, words, lan = 'es', out = '' ):

    """
    Realiza un histograma con el puntaje m\'aximo de s tiros aleatorios
    No se hace con s palabras, ya que tiros con 'blank' generan multiples secuencias posibles    
    """

    
    global_score = []
        
    for n in range( s ):
          
        maxScore = 0

        
        # Secuencia aleatoria (lista de secuencias si durante el sorteo salen fichas blank)
            
        rndSec = secuencia_rnd( lan )
            

        # Resolucion para cada secuencia de la lista rndSec
            
        for sec in rndSec:

            result, msg = juego( sec, words, lan )
                
                
            # Se agrega solo el maximo puntaje para esta secuencia

            if result:

                maxItem = result[0][1]
                    
                if maxItem >= maxScore  :

                    maxScore = maxItem


                    
        global_score.append( maxScore )


                




    # Grafico de barras (cada bin esta centrado en un puntaje)
    

    count = col.Counter(global_score)

    bins, data = [], []

    for c in sorted(count):

        bins.append( c )

        data.append( count[c])

        
    
    fig, axs = plt.subplots()

    axs.grid()
    
    axs.bar( bins, data, color = 'r', align = 'center' )

    axs.yaxis.set_major_locator(MaxNLocator(integer=True))

    axs.xaxis.set_major_locator(MaxNLocator(integer=True))
    
    axs.set_xlabel('Puntaje máximo')

    axs.set_xlim(-1)

    axs.set_ylabel('Repeticiones')

    axs.set_title('Histograma para {} secuencias'.format(s))

    


      
    
    if not out:
    
        plt.show()

    else:

        if( [x for x in ['eps','png','jpg','svg','pdf'] if x in out] ):

            plt.savefig( out )

        else:

            with open(out, 'w') as f:

                for b,d in zip(bins, data):
                
                    f.write( '{} {}\n'.format(b,d) )
        
    

    pass
