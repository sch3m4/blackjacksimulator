## Simulador estadistico basico de BlackJack
* La banca se planta en 17
* No se permiten desdobles
* No se permiten apuestas seguras (la banca saca figura)
* Se conocen las cartas iniciales del croupiere (no deberia...)

## Estrategias de juego:
 * Croupiere => Simula el juego del croupiere
 * Interactivo => El usuario participa en el juego
 * Estadistico => Decide la jugada por estadistica (ajustar logica en el codigo)

## Ejemplo de salida ronda 
    Ronda 8  [  Jugador 0 (18) >G: 3 P: 4<  |  Jugador 1 (10) >G: 4 P: 3<  |  Jugador 2 (17) >G: 5 P: 1<  |  Jugador 3 (17) >G: 3 P: 4<  |  Croupiere (20) >G: 12 P: 15<  ]
    
    [i] Mano actual:  [2, 4, 2, 12]
    [i] Puntos:       18

    [i] Probabilidades:
    	2 = 4.8276% (Sumaria 20)
    	3 = 11.0345% (Sumaria 21)
    	4 = 7.5862% (Sumaria 22)
    	5 = 8.2759% (Sumaria 23)
    	6 = 5.5172% (Sumaria 24)
    	7 = 8.2759% (Sumaria 25)
    	8 = 7.5862% (Sumaria 26)
    	9 = 6.2069% (Sumaria 27)
    	10 = 8.9655% (Sumaria 28)
    	11 = 7.5862% (Sumaria 29)
    	12 = 9.6552% (Sumaria 30)
    	13 = 8.2759% (Sumaria 31)
    	1 = 6.2069% (Sumaria 19)
    
    + Prob. Alta:   40.6897% (Sumaria 28)
    + Prob. Baja:   37.2414% (Max. 24)
    + Prob. Neutra: 22.0690% (Max. 27)
    
    [i] Probabilidad de fallo: 77.9310%
    
    [i] Conteo:
        - HI-LO:    5
        - KnockOut: 13
        - Uston SS: 7
    
    [i] Jugada recomendada: Pasar
    
    [i] Carta? (s/n)[s]: 

## Ejemplo de salida (final)
    Ronda 9  [  Jugador 0 (18) >G: 3 P: 5<  |  Jugador 1 (17) >G: 4 P: 4<  |  Jugador 2 (23) >G: 5 P: 2<  |  Jugador 3 (18) >G: 3 P: 5<  |  Croupiere (13) >G: 16 P: 15<  ]
    
    [i] Mano:          [3, 11]
    [i] Puntuacion:    13
    
    [i] Probabilidades:
        2 = 5.3846% (Sumaria 15)
        3 = 9.2308% (Sumaria 16)
    	4 = 6.9231% (Sumaria 17)
    	5 = 8.4615% (Sumaria 18)
    	6 = 6.1538% (Sumaria 19)
    	7 = 9.2308% (Sumaria 20)
    	8 = 7.6923% (Sumaria 21)
    	9 = 6.9231% (Sumaria 22)
    	10 = 9.2308% (Sumaria 23)
    	11 = 5.3846% (Sumaria 24)
    	12 = 10.0000% (Sumaria 25)
    	13 = 8.4615% (Sumaria 26)
    	1 = 6.9231% (Sumaria 14)
    
    + Prob. Alta:   40.0000% (Sumaria 23)
    + Prob. Baja:   36.1538% (Max. 19)
    + Prob. Neutra: 23.8462% (Max. 22)
    
    [i] Probabilidad de fallo: 40.0000%
    
    [i] Conteo:
    	- HI-LO:    5
    	- KnockOut: 13
    	- Uston SS: 0
    
    [i] Jugada recomendada: Pedir carta
    
    [i] Mano:        [3, 11, 10]
    [i] Puntuacion:  23
    
    La banca (23) pierde contra Jugador 0 (18)
    La banca (23) pierde contra Jugador 1 (17)
    Jugador 2 ya perdio en su turno
    La banca (23) pierde contra Jugador 3 (18)
    
    (Pulse intro para pasar a la siguiente ronda) 