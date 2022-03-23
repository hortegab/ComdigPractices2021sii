import numpy
import numpy as np
import random
import math
from gnuradio import gr

class e_canal_BER(gr.sync_block):
    """
Es un canal AWGN (Additive White Gaussian Noise, en banda base), Recibe la envolvente compleja de una senal con modulacion digital. 
El bloque tiene dos salidas: out0, out1. En out0 entrega la misma senal recibida pero con ruido blanco gausiano aditivo con 
diferentes valores de potencia que corresponden a diferentes valores Es/No; en out1 entrega un valor de Es/No aplicado a cada muestra de out0. 
Este bloque se diferencia de otros bloques tradicionales de canal AWGN en lo siguiente: 
- Tiene internamente una funcion que mide la potencia promedio de la senal entrante Ps, de modo que puede calcular Es=Ps/Rs; 
- Al ir variando la potencia del ruido Pn se logra variar la relacion Es/No para que tome N posibles valores entre EsN0min y EsN0max. 
- Con eso ha completado el primer ensayo para que otro sea el bloque que calcule la Curva de BER. 
- Pero alli no para, sino que sigue realizando tantos ensayos como lo permita el tiempo de simulacion, para que el bloque que calcula la Curva de BER la pueda ir perfeccionando cada vez mas.

Datos de configuracion del bloque:
N: Es el numero de puntos discretos que va a tener la curva de BER. Tambien corresponde al numero de valores que tomará la relacion Es/No
EsN0min: El minimo valor a tener en cuenta para Es/No
EsN0max: El maximo valor a tener en cuenta para Es/No
Rs: es la rata de simbolos.
B: Es una caracteristica de la senal entrante, corresponde a la frecuencia de muestreo de la señal entrante y puede ser mayor o igual a Rs. 
Es: es la energia de un simbolo

Senales de entrada:
In0: Envolvente compleja de señal con modulacion digital.

Senales de salida: 
out0: es la salida del canal, es decir, la misma señal entrante pero a la cual se le ha sumado un ruido para satisfacer una determinado valor para la relación Es/No
out1: Es el valor Es/No aplicado a la salida actual.

Algunas variables internas son:
No: es la Densidad espectral del potencia del ruido blanco.
SNR-Db: es la relacion senal a ruido en dB

NOTA IMPORTANTE: 
* Nos preguntamos si este bloque no deberia llamarse e_canal_BER, pues no maneja bits, ni relacion alguna con ellos, solo simbolos. El nombre mas apropiado seria e_canal_EsN0
* Este bloque no conoce el numero de bits por simbolo, por lo tanto no puede determinar la relacion Eb/No y lo que calcula es la BER con respecto a Es/No.
* La Envolvente compleja puede tener varias muestras por simbolo (Sps), por ejemplo cuando ha pasado por un bloque de Wave Forming, por ello SampRate puede ser mayor o igual a Rs. SampRate=Rs*Sps. El problema es que en este caso, la salida out0 tendra tambien Sps valores por simbolo, lo cual debe ser tenido en cuenta por los bloques que usen esta senal.
* Es es calculado como: Es = Ps x Ts, donde Ps es la potencia promedio de la senal entrante (se mide internamente) y Ts es la duracion de cada simbolo o Ts = 1 / Rs. Entendemos que eso implica imaginar que los simbolos tienen forma rectangular, lo cual puede ser valido cuando la senal entrante trae modulacion digital basada en puntos de constelacion como es el caso de: BPSK, QPSK, MPSK, MQAM. En otras palabras, es una idealizacion pensada en una herramienta de analisis de Curvas de BER para comparar diferentes tipos de modulacion en condiciones similares.

PARA CORREGIR: este bloque no debria llamarse e_canal_BER sino canal_BER_cc
"""
    def __init__(self, N=8, EsN0min=0, EsN0max=16,B=100,Rs=1):  # only default arguments here
        gr.sync_block.__init__(
        self,
        name='e_EsNo_Channel',
        in_sig=[np.complex64],
        out_sig=[np.complex64, np.int32])

        # Npoints: Numero de puntos de la curva de SER
        # Ntrials: es un vector que contiene el numero de ensayos a aplicar
        # a cada punto de la curva SER. Pero los ensayos no están dados en
        # número de muestras sino en número de tramas de L muestras
        # itrial: es el ensayo actual
        # self.ipoint: el punto actual de la curva
        # Calc_v: velocidad de calculo. Entre mas pequeno la curva de BER se vera cambiando de manera mas dinamica
        # pero tendremos mayor desgaste de tiempo para obtener la curva final.
        Calc_v=1.5
        self.Npoints = N
        self.B=B
        self.Rs=Rs
        self.EsN0dB=np.linspace(EsN0min,EsN0max,N)
        self.Ntrials=np.round(np.power(Calc_v,np.arange(N)))
        #self.Ntrials=np.arange(N)*10
#        self.Ntrials=[2]*N
        self.ipoint=0
        self.itrial=0
     
    def work(self, input_items, output_items):

        # calculo de la varianza (potencia promedio normalizada) de la senal entrante
        L=len(input_items[0])
        Pin=np.mean(np.absolute(input_items[0])**2)

        ###############################################################  
        ##  Aqui es donde esta el mehoyo y se puede optimizar mejor  ##
        ##  Algo que se podria hacer es que le de mas atencion a los ## 
        ##  valores altos de Es/No que es donde es mas dificil de ob-##
        ##  tener la BER. Al parecer la forma facil de hacerlo es    ##
        ##  hacer que el vector EsN0dB vaya cambiando, ya que es     ##
        ##  estatico y es el que define que valores de EsN0dB usar   ##
        ## Nota: a veces se nos da por creer que debemos entregar un 
        ## vector o stream que lleva N muestras consecutivas, pero   ##
        ## no es así, sino que cada muestra que sale lleva una espe- ##
        ## de etiqueta que dice cual es su puesto dentro de los N    ##
        ## valores discretos de la curva de BER, esa etiqueta es la  ##
        ## sale por la salida out1, porque a cada muestra en out0,   ##
        ## le corresponde una en out1.                               ##
        ## Quizá necesitamos incluir un retardador para que si los   ##
        ## bits han sufrido un retardo con respecto a la señal en el ##
        ## canal esto sea tenido en cuenta.
        ## Supongo que ya tenemos un valor fijo para L=N nos liberaremos
        ## de los for e if de abajo                                  ##
        ###############################################################

        ##################################################################
        ## En realidad lo unico que hay que hacer agregar ruido a la    ##
        ## senal entrante para que salga por output_items[0] y poder    ##
        ## indicar, por output_items[0], el punto de la curva que le    ##
        ## corresponde                                                  ##
        ##################################################################
        output_items[0][:] = input_items[0]+vec_noise_c(L,self.EsN0dB[self.ipoint], Pin,self.Rs,self.B)
        output_items[1][:] = [self.ipoint]*L # porque ipoint no ha cambiado en la trama L 
#        print("ipoint= ",self.ipoint)
#        print("output1= ", output_items[1])

        ##############################################################
        ## seccion donde se programa el salto a un nivel mayor de   ##
        ## ruido a inyectar a la señal                              ##
        ##############################################################
        # ya sabemos que los if no son deseables, pero tengase en cuenta
        # que no lo estamos usando para cada muestra, sino para cada
        # trama de L muestras. Podemos cambiarlo por while una vez pase
        # todas las pruebas
        if self.itrial < self.Ntrials[self.ipoint]-1: 
            self.itrial += 1
        else:
            # reseteamos el contador de ensayos interno. No nos importa
            # porque nuestro bloque no calcula promedios, solo suma ruido
            # y senala a que punto de la curva corresponde. Ahora pasamos
            # al siguiente punto de la curva
            self.itrial=0
            if self.ipoint < self.Npoints-1:
                self.ipoint += 1
            else:
                self.ipoint=0
        return len(output_items[0])

#############################################################################
## calculo de una muestra de ruido
## Rb: Rata de simbolos
## B: Es el ancho de banda pasobanda que va a ocupar el ruido blanco, que no
##    no es otra cosa que 2 veces el ancho de banda que tiene la envolvente
##    compleja del ruido blanco que estamos generando. Estamos considerando que
##    B es igual a la frecuencia de muestreo de la senal
## N: es el numero de elementos en el vector
## P_s: es la varianza (potencia promedio) de la senal entrante. 
## SNR_dB: es la relacion senal a ruido en dB del ruido respecto a P_signal
#############################################################################

def vec_noise_c(N, EsN0_dB,P_s,Rs,B):

    EsN0=pow(10.,EsN0_dB/10.) 
    SNR=EsN0*Rs/B
    P_n = P_s/SNR  # la potencia del ruido
    Vrms = math.sqrt(P_n)
#    print("Vrms= ",Vrms)
    # random.normal() pide la desviacion standard que es el mismo Valor RMS
    # Vrms es el Valor RMS de la Envolvente compleja del ruido, pero la vamos
    # a generar como un ruido real mas un ruido imaginario. Pero esas dos
    # senales tienen un valor RMS un tanto diferente: Vrms_q=Vrms/math.sqrt(2.) 
    Vrms_q= [Vrms/math.sqrt(2.)]*N # Notese que Vrms_q es un vector
    # print("Vrms_q= ",Vrms_q)
    n=np.random.normal(0.,Vrms_q)+np.random.normal(0.,Vrms_q)*1.j
    return n



