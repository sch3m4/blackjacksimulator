#!/usr/bin/env python
#
# Basic BlackJack Python Simulator
# http://github.com/sch3m4/blackjacksimulator
#
# Chema Garcia (a.k.a. sch3m4)
#    chema@safetybits.net
#    http://safetybits.net
#    @sch3m4

from __future__ import division

import os
import sys
import time
import random


class bcolors:
    """
    Clase para colorear la salida
    """

    def __init__(self):
        return

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''


class Perdido(Exception):
    """
    Excepcion de perdida de partida
    """

    idjugador = 0
    puntos = 0

    def __init__(self, idjugador=-1, puntos=0):
        self.idjugador = idjugador
        self.puntos = puntos
        return

    def __str__(self):
        return "El jugador %d ha perdido con %d puntos" % (self.idjugador, self.puntos)


class SinCartas(Exception):
    """
    Excepcion de fin de partida
    """

    def __init__(self):
        return

    def __str__(self):
        return "Fin de la partida"


class Jugador:
    """
    Modelizacion de un jugador
    """

    # maximo valor posible
    MAXPUNTOS = 21

    # victorias
    VICTORIAS = 0
    # derrotas
    DERROTAS = 0

    # dinero inicial
    DINERO = 0
    # apuesta
    APUESTA = 0

    # puntos actuales
    PUNTOS = 0
    # ronda actual
    RONDA = 0
    # mano del jugador
    CARTAS = None
    # ases
    NASES = 0  # por defecto valdran 11, si el jugador se pasa de 21 valdran 1
    # ha sacado blackjack?
    BLACKJACK = 0
    # id del jugador
    ID = None
    # nombre del jugador
    NOMBRE = None

    def __init__(self, idjugador, dinero=100):
        self.ID = idjugador
        self.CARTAS = []

        if idjugador < 0:
            self.NOMBRE = "Croupiere"
        else:
            self.NOMBRE = "Jugador %d" % idjugador

        self.DINERO = dinero

        return

    def getDinero(self):
        return self.DINERO

    def setApuesta(self, valor):
        if self.ID >= 0 and valor > self.DINERO:
            raise Perdido('No tiene dinero')
        self.DINERO -= valor
        self.APUESTA = valor

    def devolverApuesta(self):
        """
        Cuando el jugador empata
        """
        self.DINERO += self.APUESTA
        self.APUESTA = 0

    def setCarta(self, valor):
        """
        Guarda una carta
        """
        self.CARTAS.append(valor)

        # las figuras valen 10
        if valor > 9:
            valor = 10
        elif valor == 1:
            valor = 11
            self.NASES += 1

        self.PUNTOS += valor

        # mientras sobrepasemos 21 cambiamos los valores de los ases tomados
        # como 11 a 1
        while self.PUNTOS > self.MAXPUNTOS and self.NASES > 0:
            self.NASES -= 1
            self.PUNTOS -= 10  # la diferencia entre los dos valores del as

        # si se ha pasado lanzamos la excepcion
        # (en las dos primeras rondas no es posible que se pase)
        if self.PUNTOS > self.MAXPUNTOS:
            raise Perdido(self.ID, self.PUNTOS)

        self.RONDA += 1

        return

    def getId(self):
        return self.ID

    def agregarVictoria(self):
        self.VICTORIAS += 1
        self.DINERO += self.APUESTA * 2
        if self.getBlackJack():
            self.DINERO += self.APUESTA
        self.APUESTA = 0

    def getVictorias(self):
        return self.VICTORIAS

    def getDerrotas(self):
        return self.DERROTAS

    def agregarDerrota(self):
        self.DERROTAS += 1

    def getPuntos(self):
        return self.PUNTOS

    def getNombre(self):
        return self.NOMBRE

    def getMano(self):
        # si es el banca ocultamos la primera
        if self.ID < 0 and self.RONDA < 2:
            mano = []
            if len(self.CARTAS) > 0:
                mano.append('X')
                if len(self.CARTAS) > 1:
                    for i in range(1, len(self.CARTAS)):
                        mano.append(self.CARTAS[i])
        else:
            mano = self.CARTAS
        return mano

    def setBlackJack(self):
        self.BLACKJACK = 1

    def getBlackJack(self):
        return self.BLACKJACK

    def reiniciarMano(self):
        self.CARTAS = []
        self.NASES = 0
        self.PUNTOS = 0
        self.BLACKJACK = 0
        self.RONDA = 0


class Resultados:
    """
    Clase para almacenar los resultados y proceder a su posterior analisis
    """

    PIERDE = 1
    GANA = 2
    EMPATA = 3

    # numero de jugadores
    JUGADORES = 0

    # contiene las victorias de los jugadores segun las rondas
    VICTORIAS = None

    # contiene las jugadas
    JUGADAS = None

    def __init__(self):
        return

    def getJugadas(self):
        return self.JUGADAS

    def getResultados(self):
        return self.VICTORIAS

    def getJugadores(self):
        """
        Devuelve el NUMERO de jugadores
        """
        return self.JUGADORES

    def agregarJugador(self):
        """
        Agrega una dimension a los datos
        """
        if self.VICTORIAS is None:
            self.VICTORIAS = [[]]
            self.JUGADAS = [[]]
        else:
            self.VICTORIAS.append([])
            self.JUGADAS.append([])

        self.JUGADORES += 1
        return

    def agregarRonda(self):
        """
        Agrega una dimesion a los jugadores
        """
        if self.VICTORIAS is None:
            raise Exception('No se han agregado jugadores')
        for i in self.VICTORIAS:
            i.append([])
        for i in self.JUGADAS:
            i.append([])
        return

    def agregarResultado(self, jugador, ronda, resultado):
        if self.VICTORIAS is None:
            raise Exception('No se han agregado jugadores')
        if not resultado in [self.GANA, self.PIERDE, self.EMPATA]:
            raise Exception('Resultado no contemplado')
        self.VICTORIAS[jugador][ronda - 1] = resultado
        return

    def agregarJugada(self, jugador, ronda, jugada):
        if self.JUGADAS is None:
            raise Exception('No se han agregado jugadores')
        self.JUGADAS[jugador][ronda - 1] = jugada

    def mostrarResultados(self):
        if self.VICTORIAS is None:
            raise Exception('No hay resultados')

        # por cada jugador
        idjugador = 0
        for i in self.VICTORIAS:
            print "Jugador %d" % idjugador
            idronda = 0
            for j in i:
                print j
                print "\tRonda %d: %s" % (idronda, self.getStrval(j))
                idronda += 1
            print ""
            idjugador += 1

    def mostrarJugadas(self,):
        if self.JUGADAS is None:
            raise Exception('No hay jugadas')

        # por cada jugador
        idjugador = 0
        for i in self.JUGADAS:
            print "Jugador %d" % idjugador
            idronda = 0
            for j in i:
                print "\tRonda %d: %d" % (idronda, j)
                idronda += 1
            print ""
            idjugador += 1

    def limpiar(self):
        for i in self.VICTORIAS:
            idj = 0
            for j in i:
                if type(j) == type([]) and len(j) == 0:
                    i.pop(idj)
                idj += 1

        for i in self.JUGADAS:
            idj = 0
            for j in i:
                if type(j) == type([]) and len(j) == 0:
                    i.pop(idj)
                idj += 1

    def getModaResultados(self, idjugador=-1):
        """
        Devuelve la moda de los resultados
        """
        res = self.getFreqResultados(idjugador)
        val = -1
        ind = 1
        while val < 0:
            if res[ind - 1] == max(res):
                val = ind
            else:
                ind += 1
        return val

    def getStrval(self, resultado):
        if not resultado in [self.GANA, self.PIERDE, self.EMPATA]:
            raise Exception('Resultado no contemplado')
        return "Gana" if resultado == self.GANA else ("Pierde" if resultado == self.PIERDE else "Empata")

    def getFreqResultados(self, idjugador=-1):
        """
        Devuelve la frecuencia de los resultados
        """

        ret = [0, 0, 0]
        if idjugador < 0:
            for jugador in self.VICTORIAS:
                for ronda in jugador:
                    ret[ronda - 1] += 1
        else:
            for ronda in self.VICTORIAS[idjugador]:
                ret[ronda - 1] += 1
        return ret


class BlackJack:
    """
    Clase principal del juego
    """

    ##############################
    #    ESTRATEGIAS DE JUEGO    #
    ##############################
    class Estrategias:
        """
        Define las estrategias de juego disponibles
        """
        INTERACTIVA = 0
        CROUPIERE = 1
        ESTADISTICA = 2

        def __init__(self):
            return

    ################
    #    CONTEO    #
    ################
    class Conteo:
        HILO = 0
        KO = 0
        USTONSS = 0

        def __init__(self):
            return

        def cuentaHILO(self, valor):
            """
            Conteo HI-LO (sistema balanceado)
            """
            if valor in [10, 11, 12, 13, 1]:
                self.HILO -= 1
            elif valor in [2, 3, 4, 5, 6]:
                self.HILO += 1

        def getHILO(self):
            return self.HILO

        def cuentaKO(self, valor):
            """
            Conteo Knockout
            """
            if valor in [10, 11, 12, 13, 1]:
                self.KO -= 1
            elif valor in [2, 3, 4, 5, 6, 7]:
                self.KO += 1

        def getKO(self):
            return self.KO

        def cuentaUstonSS(self, valor):
            """
            Conteo Uston SS
            """
            if valor in [10, 11, 12, 13, 1]:
                self.USTONSS -= 2
            elif valor in [2, 4, 6]:
                self.USTONSS += 2
            elif valor == 5:
                self.USTONSS += 3
            elif valor == 7:
                self.USTONSS += 1
            elif valor == 9:
                self.USTONSS -= 1

        def getUstonSS(self):
            return self.USTONSS

        def conteo(self, valor):
            self.cuentaHILO(valor)
            self.cuentaKO(valor)
            self.cuentaUstonSS(valor)

    ####################
    #    CONSTANTES    #
    ####################
    # numero maximo de jugadores
    MAXJUGADORES = 7
    # numero de palos
    NPALOS = 4
    # numero de cartas de un palo
    NCARTASPALO = 13
    ###################
    #    VARIABLES    #
    ###################
    # apuesta minima
    APUESTAMINIMA = None
    # estrategia de juego
    ESTRATEGIA = None
    # estrategia de juego por defecto
    DEF_ESTRATEGIA = None
    # a que jugador/jugadores aplicar la estrategia de juego
    APLICAR_JUGADORES = None
    # conteo de cartas
    CONTEO = None
    # modo interactivo para repartir cartas iniciales, ver jugada final, etc.
    INTERACTIVO = 0
    # numero de barajas
    NBARAJAS = None
    # numero de cartas totales
    NCARTASTOTALES = None
    # cartas altas, consecutivas en orden creciente
    CARTAS_ALTAS = None
    # cartas bajas, consecutivas en orden creciente
    CARTAS_BAJAS = None
    # numero de ases
    NASES = None
    # numero de figuras (de valor 10)
    NFIGURAS = None
    # numero de cartas altas
    NALTAS = None
    # numero de cartas bajas
    NBAJAS = None
    # numero de cartas neutras
    NNEUTRAS = None
    # numero de jugadores
    NJUGADORES = None
    # el banca de la mesa
    IDBANCA = None
    # Jugadores
    JUGADOR = None
    # numero de cartas
    CARTAS = None
    # resultados
    RESULTADOS = None
    # numero de la ronda
    RONDA = 1
    # turno del jugador
    TURNO = 0

    baraja = []  # Baraja de cartas

    ###################################
    #    CALCULO DE PROBABILIDADES    #
    ###################################

    def __probAlta__(self):
        """
        Probabilidad de sacar una carta alta
        """
        return (self.NALTAS / self.NCARTASTOTALES) * 100

    def __probBaja__(self):
        """
        Probabilidad de sacar una carta baja
        """
        return (self.NBAJAS / self.NCARTASTOTALES) * 100

    def __probNeutra__(self):
        """
        Probabilidad de sacar una carta neutra
        """
        return (self.NNEUTRAS / self.NCARTASTOTALES) * 100

    def __probBlackJack__(self):
        """
        Devuelve la probabilidad de sacar blackjack de cada jugador.
        """
        return ((self.NASES / self.NCARTASTOTALES) * (self.NFIGURAS / (self.NCARTASTOTALES - 1))) * 100

    def __probCarta__(self, carta):
        return (self.CARTAS[carta - 1] / self.NCARTASTOTALES) * 100

    def __probFallo__(self, puntos, jugador=None):
        if jugador is not None:
            puntos = jugador.getPuntos()
        probfallo = 0
        for i in range(1, self.NCARTASPALO + 1):  # empezamos desde el 2
            if i == self.NCARTASPALO:  # el valor self.NCARTASPALO esta fuera del palo y lo tratamos como as
                i = 0
            if puntos + i + 1 > Jugador.MAXPUNTOS:
                probfallo += self.__probCarta__(i + 1)
        return probfallo

    def __init__(self, apuesta=5, interactivo=0, jugadores=1, barajas=1, defestrategia=Estrategias.CROUPIERE, estrategia=Estrategias.CROUPIERE, aplicarjugadores=-1, cartasbajas=[2, 3, 4, 5, 6], cartasaltas=[10, 11, 12, 13, 1]):
        """
        Inicializamos la baraja, jugadores, las manos de los jugadores, resultados, etc.
        ------------------------------------------
        apuesta => Apuesta minima
        interactivo => distinto de la estrategia, pide confirmacion para iniciar ronda
        jugadores => numero de jugadores
        barajas => numero de barajas
        defestrategia => estrategia por defecto
        estrategia => estrategia especifica para ciertos jugadores
        aplicarjugadores => jugadores a los que aplicar la estrategia anterior
        cartasbajas => cartas consideradas como bajas
        cartasaltas => cartas consideradas altas
        ------------------------------------------
        """

        try:
            jugadores = int(jugadores)
            barajas = int(barajas)
            interactivo = int(interactivo)
            apuesta = int(apuesta)
        except Exception, e:
            raise e

        # verificamos la apuesta minima
        if apuesta <= 0:
            raise Exception('Debe haber una apuesta minima')
        else:
            self.APUESTA = apuesta

        # verificamos la estrategia de juego
        if estrategia not in [self.Estrategias.INTERACTIVA, self.Estrategias.CROUPIERE, self.Estrategias.ESTADISTICA]:
            raise Exception('Estrategia desconocida')
        else:
            self.ESTRATEGIA = estrategia

        # verificamos la estrategia de juego por defecto
        if defestrategia not in [self.Estrategias.INTERACTIVA, self.Estrategias.CROUPIERE, self.Estrategias.ESTADISTICA]:
            raise Exception('Estrategia desconocida')
        else:
            self.DEF_ESTRATEGIA = defestrategia

        # verificamos el modo interactivo
        if interactivo < 0 or interactivo > 1:
            raise Exception('Valor "interactivo" fuera de rango')
        else:
            self.INTERACTIVO = interactivo

        # verificamos el numero de jugadores
        if jugadores <= 0:
            raise Exception('Debe haber al menos un jugador')
        elif jugadores > self.MAXJUGADORES:
            raise Exception('Demasiados jugadores (max = %d)' % self.MAXJUGADORES)

        # verificamos el numero de barajas
        if barajas <= 0:
            raise Exception('Debe haber al menos una baraja!')

        # asignamos las cartas altas/bajas
        self.CARTAS_ALTAS = cartasaltas
        self.CARTAS_BAJAS = cartasbajas

        # jugadores a los que aplicar la estrategia de juego
        if type(aplicarjugadores) == type([]):
            self.APLICAR_JUGADORES = aplicarjugadores

        self.NBARAJAS = barajas  # numero de barajas
        self.NCARTASTOTALES = self.NPALOS * self.NCARTASPALO * self.NBARAJAS  # numero de cartas
        self.NASES = self.NPALOS * self.NBARAJAS  # numero de ases
        self.NFIGURAS = 4 * self.NPALOS * self.NBARAJAS  # numero de figuras
        self.NALTAS = len(self.CARTAS_ALTAS) * self.NPALOS * self.NBARAJAS  # numero de cartas altas
        self.NBAJAS = len(self.CARTAS_BAJAS) * self.NPALOS * self.NBARAJAS  # numero de cartas bajas
        self.NNEUTRAS = self.NCARTASTOTALES - (self.NALTAS + self.NBAJAS)  # numero de cartas neutras
        self.NJUGADORES = jugadores  # numero de jugadores (banca incluida)

        # inicializamos los jugadores
        self.JUGADOR = [Jugador(i) for i in range(0, self.NJUGADORES)]  # jugadores ordinarios
        self.JUGADOR.append(Jugador(-1))  # el banca
        self.IDBANCA = self.NJUGADORES  # id de la banca

        # inicializamos la cantidad de cada carta
        self.CARTAS = []
        for i in range(0, self.NCARTASPALO):
            self.CARTAS.append(self.NPALOS * self.NBARAJAS)

        # inicializamos los resultados
        self.RESULTADOS = Resultados()
        #   agregamos los jugadores (banca no incluida)
        for i in range(0, self.NJUGADORES):
            self.RESULTADOS.agregarJugador()

        # inicializamos las barajas
        for i in range(1, self.NCARTASTOTALES + 1):
            val = i % self.NCARTASPALO
            if val == 0:
                val = self.NCARTASPALO
            self.baraja.append(val)

        self.CONTEO = self.Conteo()

        # inicializamos la semilla
        random.seed(time.time())

        # aunque sacaremos las cartas de manera aleatoria, "barajamos" ;-)
        val = random.randint(self.NCARTASTOTALES, 3 * self.NCARTASTOTALES)
        for i in range(0, val):
            pos1 = random.randint(0, self.NCARTASTOTALES - 1)
            pos2 = pos1
            # improbable
            while pos2 == pos1:
                pos2 = random.randint(0, self.NCARTASTOTALES - 1)
            # cambiamos
            tmp = self.baraja[pos1]
            self.baraja[pos1] = self.baraja[pos2]
            self.baraja[pos2] = tmp

        return

    def getResultados(self):
        """
        Devuelve los resultados obtenidos
        """
        self.RESULTADOS.limpiar()
        return self.RESULTADOS

    def getIdBanca(self):
        return self.IDBANCA

    def getJugador(self, idjugador):
        """
        Devuelve un objeto jugador segun el ID
        """
        try:
            return self.JUGADOR[idjugador]
        except:
            raise Exception("Error al acceder al jugador %d" % idjugador)

    def __getCarta__(self):
        """
        Extrae una carta de la baraja
        """

        if not len(self.baraja) > 1:
            raise SinCartas()

        idcarta = random.randint(0, len(self.baraja) - 1)
        carta = self.baraja.pop(idcarta)

        # el as
        if carta == 0:
            carta += 1

        # decrementamos el grupo de la carta
        if carta == 1:
            self.NASES -= 1
        elif carta > 9:
            self.NFIGURAS -= 1

        # decrementamos el grupo de la carta
        if carta in self.CARTAS_ALTAS:
            self.NALTAS -= 1
        elif carta in self.CARTAS_BAJAS:
            self.NBAJAS -= 1
        else:
            self.NNEUTRAS -= 1

        # decrementamos las cartas totales
        self.NCARTASTOTALES -= 1
        # decrementamos las apariciones de dicha carta
        self.CARTAS[carta - 1] -= 1

        self.CONTEO.conteo(carta)

        return carta

    def __mostrarProbabilidades__(self, puntos):
        """
        Muestra las probabilidades de cada carta, de sacar cartas altas,bajas,neutras
        asi como la probabilidad de fallo y la jugada recomendada
        """

        # mostramos la probabilidad de cada carta
        print "[i] Probabilidades:"
        for i in range(1, self.NCARTASPALO + 1):  # empezamos desde el 2
            if i == self.NCARTASPALO:  # el valor self.NCARTASPALO esta fuera del palo y lo tratamos como as
                i = 0
            salida = "\t%d = %.4f%s (Sumaria %d)" % (i + 1, self.__probCarta__(i + 1), '%', puntos + i + 1)
            # se pasaria
            if puntos + i + 1 > Jugador.MAXPUNTOS:
                print bcolors.FAIL + str(salida) + bcolors.ENDC
            else:
                print bcolors.OKGREEN + str(salida) + bcolors.ENDC

        # mostramos la probabilidad de cartas altas/bajas/neutras
        print ""
        print "+ Prob. Alta:   %.4f%s (Sumaria %d)" % (self.__probAlta__(), '%', puntos + self.CARTAS_ALTAS[0])
        print "+ Prob. Baja:   %.4f%s (Max. %d)" % (self.__probBaja__(), '%', puntos + self.CARTAS_BAJAS[-1:][0])
        print "+ Prob. Neutra: %.4f%s (Max. %d)" % (self.__probNeutra__(), '%', puntos + self.CARTAS_ALTAS[0] - 1)
        # mostramos la probabilidad de fallo
        print "\n[i] Probabilidad de fallo: %.4f%s" % (self.__probFallo__(puntos), '%')
        # mostramos la cuenta
        print "\n[i] Conteo:"
        print "\t- HI-LO:    %d" % self.CONTEO.getHILO()
        print "\t- KnockOut: %d" % self.CONTEO.getKO()
        print "\t- Uston SS: %d" % self.CONTEO.getUstonSS()
        # mostramos la jugada recomendada
        print "\n[i] Jugada recomendada: %s" % (bcolors.FAIL + "Pasar" if self.__decidirJugada__(puntos) == 0 else bcolors.OKGREEN + "Pedir carta") + bcolors.ENDC

        return

    def __mostrarTurnos__(self):
        """
        Muestra la cabecera de turnos y devuelve el jugador correspondiente
        """
        os.system('clear')

        if not self.TURNO <= self.NJUGADORES:
            self.TURNO = 0

        # mostramos la cabecera de turnos y puntos
        turno = None
        print bcolors.OKBLUE + ("Ronda %d " % self.RONDA) + bcolors.ENDC,
        print "[ ",
        for i in range(0, self.NJUGADORES + 1):
            jugador = self.getJugador(i)

            salida = "%s (%d) >G: %d P: %d<" % (jugador.getNombre(), jugador.getPuntos(), jugador.getVictorias(), jugador.getDerrotas())
            if self.TURNO == i:
                turno = jugador
                print bcolors.HEADER + str(salida) + bcolors.ENDC,
            else:
                if jugador.getPuntos() > Jugador.MAXPUNTOS:
                    print bcolors.FAIL + str(salida) + bcolors.ENDC,
                elif jugador.getPuntos() == Jugador.MAXPUNTOS:
                    print bcolors.OKGREEN + str(salida) + bcolors.ENDC,
                else:
                    print salida,

            if i < self.NJUGADORES:
                print " | ",
        print " ]\n"

        return turno

    def __decidirJugada__(self, puntos):
        """
        Funcion para decidir la jugada en la estrategia estadistica
        """

        probfallo = int(round(self.__probFallo__(puntos)))
        probalta = int(round(self.__probAlta__()))
        probbaja = int(round(self.__probBaja__()))
#        cuentahilo = self.CONTEO.getHILO()
#        cuentako = self.CONTEO.getKO()
#        cuentaustonss = self.CONTEO.getUstonSS()

        # por defecto no pedimos carta
        ret = 0

        # agregar la logica
        if probfallo <= 65:
            if puntos < 17:
                ret = 1
            elif probalta < probbaja:
                ret = 1

        return ret

    def __turnoInteractivo__(self, jugador):
        """
        Juego de un jugador
        Esta funcion solo se usa en la estrategia interactiva y estadistica
        """
        resp = 's'
        while resp == 's':
            self.__mostrarTurnos__()
            print "[i] Mano actual: ", jugador.getMano()
            print "[i] Puntos:       %d\n" % jugador.getPuntos()
            self.__mostrarProbabilidades__(jugador.getPuntos())
            print "\n[i] Carta? (s/n)[s]:",
            sys.stdout.flush()

            pregunta = 0
            # se le aplica una estrategia
            if self.APLICAR_JUGADORES is not None and jugador.getId() in self.APLICAR_JUGADORES:
                if self.ESTRATEGIA == self.Estrategias.INTERACTIVA:
                    pregunta = 1
            elif self.DEF_ESTRATEGIA == self.Estrategias.INTERACTIVA:
                pregunta = 1

            if pregunta > 0:
                resp = raw_input()
            else:
                resp = self.__decidirJugada__(jugador.getPuntos())
            if resp == '':
                resp = 's'

            if resp == 's':
                carta = self.__getCarta__()
                try:
                    jugador.setCarta(carta)
                except Perdido, e:
                    print "\n", e
                    resp = 'n'

    def __turnoCroupiere__(self, jugador):
        """
        Metodo similar a __turnoJugador__ pero con distinta estrategia
        """
        puntos = jugador.getPuntos()
        while puntos < 17:
            print "[i] Mano:         ", jugador.getMano()
            print "[i] Puntuacion:    %d\n" % puntos
            self.__mostrarProbabilidades__(jugador.getPuntos())
            print ""
            carta = self.__getCarta__()
            try:
                jugador.setCarta(carta)
            except:
                pass
            puntos = jugador.getPuntos()

        print "[i] Mano:       ", jugador.getMano()
        print "[i] Puntuacion:  %d" % puntos

    def jugar(self):
        """
        Metodo para iniciar el juego
        """

        JUGADA = {self.Estrategias.CROUPIERE: self.__turnoCroupiere__,
            self.Estrategias.INTERACTIVA: self.__turnoInteractivo__,
            self.Estrategias.ESTADISTICA: self.__turnoInteractivo__,
            }

        ##############################
        #    QUE EMPIECE EL JUEGO    #
        ##############################
        self.RESULTADOS.agregarRonda()
        while 1:
            turno = self.__mostrarTurnos__()

            # si no tiene cartas hacemos el reparto inicial
            if len(turno.getMano()) < 2:
                # mostramos la probabilidad de sacar blackjack
                if self.NCARTASTOTALES > 1:
                    print "[i] Probabilidad de obtener BlackJack: %.4f%s" % (self.__probBlackJack__(), '%')
                print "\n(Pulse intro para repartir carta)",

                if self.INTERACTIVO:
                    sys.stdout.flush()
                    raw_input()

                # apuesta antes de tener cartas
                if self.CONTEO.getHILO() < 5:
                    turno.setApuesta(self.APUESTA)
                else:
                    turno.setApuesta(self.APUESTA * 2)

                print ""
                for i in range(0, 2):
                    carta = self.__getCarta__()
                    turno.setCarta(carta)
                    if turno.getPuntos() == Jugador.MAXPUNTOS:
                        turno.setBlackJack()
                        if not turno.getId() < 0:
                            print "[i] Ha sacado BlackJack!!"

                print "[i] Mano: ", turno.getMano()
                print "\n(Pulse intro para pasar el turno)",

                if self.INTERACTIVO:
                    sys.stdout.flush()
                    raw_input()
                # repartimos las cartas iniciales al siguiente jugador
                self.TURNO += 1
                continue

            try:
                # el croupiere siempre juega igual
                if turno.getId() < 0:
                    self.__turnoCroupiere__(turno)
                    self.RESULTADOS.agregarJugada(turno.getId(), self.RONDA, turno.getPuntos())
                else:
                    # aplicamos la estrategia de juego por defecto
                    if self.APLICAR_JUGADORES is not None and turno.getId() in self.APLICAR_JUGADORES:
                        JUGADA[self.ESTRATEGIA](turno)
                    else:  # aplicamos la estrategia de juego especificada
                        JUGADA[self.DEF_ESTRATEGIA](turno)

                    self.RESULTADOS.agregarJugada(turno.getId(), self.RONDA, turno.getPuntos())
                    self.TURNO += 1
                    continue

            except SinCartas, e:  # nos hemos quedado sin cartas -> fin del juego
                print e
                break

            # mostramos el resultado de la jugada
            print ""
            banca = self.getJugador(self.IDBANCA)
            pbanca = banca.getPuntos()
            for i in range(0, self.NJUGADORES):
                jugador = self.getJugador(i)
                pjugador = jugador.getPuntos()

                # ya perdio en su turno
                if pjugador > Jugador.MAXPUNTOS:
                    print "%s ya perdio en su turno" % jugador.getNombre()
                    resultado = Resultados.PIERDE
                # la banca pierde con todos
                elif pbanca > Jugador.MAXPUNTOS:
                    print "La banca (%d) pierde contra %s (%d)" % (pbanca, jugador.getNombre(), pjugador)
                    resultado = Resultados.GANA
                # empate
                elif pjugador == pbanca:
                    print "La banca (%d) empata con %s (%d)" % (pbanca, jugador.getNombre(), pjugador)
                    jugador.devolverApuesta()
                    resultado = Resultados.EMPATA
                # el jugador pierde
                elif pjugador < pbanca:
                    print "La banca (%d) gana contra %s (%d)" % (pbanca, jugador.getNombre(), pjugador)
                    resultado = Resultados.PIERDE
                # el jugador gana
                elif pjugador > pbanca:
                    print "La banca (%d) pierde contra %s (%d)" % (pbanca, jugador.getNombre(), pjugador)
                    resultado = Resultados.GANA

                if resultado == Resultados.GANA:
                    jugador.agregarVictoria()
                    banca.agregarDerrota()
                elif resultado == Resultados.PIERDE:
                    jugador.agregarDerrota()
                    banca.agregarVictoria()

                self.RESULTADOS.agregarResultado(jugador.getId(), self.RONDA, resultado)

                jugador.reiniciarMano()

            banca.reiniciarMano()

            print "\n(Pulse intro para pasar a la siguiente ronda)",
            if self.INTERACTIVO or self.DEF_ESTRATEGIA == self.Estrategias.INTERACTIVA or self.ESTRATEGIA == self.Estrategias.INTERACTIVA:
                sys.stdout.flush()
                raw_input()
            self.RONDA += 1
            self.RESULTADOS.agregarRonda()
            self.TURNO = 0


def main():

    # inicializamos el juego
    juego = BlackJack(interactivo=0, jugadores=4, barajas=5, defestrategia=BlackJack.Estrategias.CROUPIERE, estrategia=BlackJack.Estrategias.INTERACTIVA, aplicarjugadores=[0])

    # comenzamos a jugar
    try:
        juego.jugar()
    except KeyboardInterrupt:
        pass
    except SinCartas:
        pass

    print "\n"

    # tenemos los resultados
    datos = juego.getResultados()
    # obtenemos los resultados finales de las jugadas
#    resultados = datos.getResultados()
    # obtenemos los valores de las jugadas
#    jugadas = datos.getJugadas()

    print "+ Dinero de los jugadores:"
    for i in range(0, datos.getJugadores()):
        jugador = juego.getJugador(i)
        print "\t%s: %d EUR" % (jugador.getNombre(), jugador.getDinero())

    print "\n+ Resultados de la mesa:"
    res = datos.getFreqResultados()
    for i in range(0, 3):
        print "\t%s: %d" % (datos.getStrval(i + 1), res[i])

    # obtenemos la moda de los resultados
    print "\n+ Moda de resultados por jugador:"
    for i in range(0, datos.getJugadores()):
        res = datos.getFreqResultados(i)
        print "\tJugador %d: Pierde %d | Gana %d | Empata %d (%s)" % (i, res[0], res[1], res[2], datos.getStrval(datos.getModaResultados(i)))

    print "\n+ Moda de resultados de la mesa: %s" % datos.getStrval(datos.getModaResultados())

    print ""
    sys.exit(0)

if __name__ == "__main__":
    main()
