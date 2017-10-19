import fichas_scrabble as fch

import matplotlib.pyplot as plt

import numpy as np

import locale




def diagrama( lan = 'es' ):

    
    """
    Creaci\'on del diagrama con las fichas de scrabble
    """

    # Seleccion de fichas de acuerdo al idioma

    fichas = {}

    
    if lan == 'es':

        fichas = fch.fichas_es
        
        locale.setlocale(locale.LC_ALL, ('en_US', 'UTF-8'))

        
    elif lan == 'en' :

        fichas = fch.fichas_en

        locale.setlocale(locale.LC_ALL, ('en_US', 'UTF-8'))
                

    elif lan == 'it' :

        fichas = fch.fichas_it

        locale.setlocale(locale.LC_ALL, ('en_US', 'UTF-8'))


    elif lan == 'fr' :

        fichas = fch.fichas_fr

        locale.setlocale(locale.LC_ALL, ('en_US', 'UTF-8'))
        

    elif lan == 'ar' :

        fichas = fch.fichas_ar

        locale.setlocale(locale.LC_ALL, ('en_US', 'UTF-8'))
                
        





    # Seleccion del ancho del casillero

    nx = 0

    for key in fichas:

        nx = nx + fichas[key][0]

    nx = int(  np.ceil( np.sqrt(nx) )  )
        



    # Creacion de la figura inicial

    fix, ax = plt.subplots()

    ax.axis( 'off' )

    ax.set_xlim((0,nx))

    ax.set_ylim((0,nx))

    plt.gca().set_aspect('equal', adjustable='box')

    ax.set_xticks([])

    ax.set_yticks([])
    



    # Lineas verticales

    for i in range(nx+1):

        ax.axvline( i, color = 'silver' )

        ax.axhline( i, color = 'silver' )






    idx = -1

    idy = 0

    
    # for k in sorted( fichas.keys(), key=lambda word: [alphabet.index(c) for c in word[0]] ):

    for k in sorted( fichas.keys() ):

        if k != 'blank' :

            for i in range( fichas[k][0] ):

                idx = idx + 1

                if idx > nx-1:

                    idx = 0

                    idy = idy + 1


                # Posicion de la ficha
                
                ax.text( 0.5 + idx, 9.5 - idy, k.upper(), ha="center", va="center", size = 15, fontweight = 'bold' )

                
                # Valor de la ficha
                
                ax.text( 0.8 + idx, 9.2 - idy, fichas[k][1], ha="center", va="center", size = 5, fontweight = 'bold' )
                
                


    
    plt.show()
    

        
    
    pass
