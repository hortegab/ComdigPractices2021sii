import numpy as np
import random
import math
import numpy
from gnuradio import gr

class e_BERtool(gr.sync_block):

    """
Calcula la curva de SER (Symbol Error Ratio) o la Curva BER (Bit Error Ratio). Para lograrlo, por las 3 entradas in0, in1, in2 espera hasta que hallan llegado N muestras, con lo cual puede obtener una primera version de la curva de BER (o de SER) de N muestras. Esa curva de BER (o de SER) se va perfeccionando en el tiempo, ya que lo anterior se repite una y otra vez, tanto como lo permita el tiempo que dure corriendo el flujograma, con lo cual va recalculando la curva de BER (o de SER) para que sea cada vez mas perfecta. 

Senales de entrada:
in0: El numero del punto de la BER que esta siendo atendido en el momento, el cual corresponde a un determinado valor de Es/No. Pero en realidad este bloque desconoce Es/No y solo le interesa conocer cual es el numero del punto a atender  
in1: es la señal de bits (o de simbolos emitidos), osea, aquellos que están antes del canal
in2: Es la señal de los bits recibidos (o de simbolos), después de pasar por un canal 

Senal de salida
Puede ser vista como una senal que cada N muestras representa la actualizacion de la curva de BER. La idea es convertirla en un vector de N muestras y graficarla mediante algo asi como un "QT GUI vector Sink" 

NOTA IMPORTANTE:
* El bloque e_canal_BER es el que se ha estado usando para generar la senal que entra por in0. Las limitaciones que eso genera son las siguientes:
   ** El canal e_canal_BER esta pensado para llevar envolvente compleja, es decir simbolos. Por lo tanto, lo que realmente se está obteniendo en una Curva de SER. Convertir eso a Curva de BER puede que no sea tan facil, necesitaria no contar con que en in1 e in2 esten las senales de bits en vez de simbolos, sino que habria que ajustar la senal destinada a la entrada in0 para que hacer que por cada bit haya un valor de Es/No o de Eb/No
   ** El bloque e_canal_BER lo que entrega es la relacion Es/No.
   ** Convertir Es/No a Eb/No es posible pero como parte de un flujograma donde se conozca el numero de bits por simbolo (Bps), teniendo en cuenta que, en términos lineales, Eb=Es/Bps
   ** La manera en que esta hecho el bloque e_canal_BER hace que si el numero de muestras por simbolo es mayor a 1 (Sps>1), la senal Es/No sale con Sps valores por simbolo. En ese caso se requeriria aplicar algun tipo de mejora ya que nuestro bloque supone que solo hay una muestra Es/No (o Es/No) por cada muestra de senal en in1 e in2.
* las senales in1 y in2 pueden ser bits o simbolos. En el segundo caso es el que hemos usado mas, ya que las senales in1 e in2 son de tipo M-PAM. Por eso, lo que hemos estado calculando es Curva de SER. Se puede pasar facilmente a Curvas de BER, si a los bits se les aplica de-M-PAM.

PARA CORREGIR: Este bloque no deberia llamarme e_BERtool, sino BERtool_if
 
"""

    ############################################################################################
    ##  Constructor del bloque                                                                ##
    ############################################################################################

    def __init__(self, N=16):  
        gr.sync_block.__init__(
        self,
        name='v_BERtool',
        in_sig=[np.int32, np.int8, np.int8],
        out_sig=[(np.float32,N)])

        # N es el numero de puntos de la curva de SER a calcular
        # self.errores = np.zeros(self.N)
        # count: cuenta el numero de muestras que ya han sido procesadas para cada punto de la BER
        # SER: es la memoria de la ultima curva calculada

        # self.count=0. # DUDA: PARECE QUE HAY ERROR. DEBERIA HABER UN CONTADOR POR CADA k
        # self.count=np.zeros(self.N)

        self.N=N 
        self.errores = np.float64(np.ones(self.N))
        self.count=np.uint64(np.ones(self.N))
        #self.SER=np.ones(self.N)
        self.SER=[1e-12]*N
        #self.ipointi=0 

    ############################################################################################
    ##  Lo de arriba es solo el constructor del bloque). Aqui comienza el verdadero cdigo     ##
    ############################################################################################

    def work(self, input_items, output_items):
        in0=input_items[1] 
        in1=input_items[2] 
        
        # L: es el tamano del vector de entrada. 
        # i: es el punto actual de los datos entrantes
        # ipoint: es el punto actual de la SER
        # count: vector de contadores para cada punto de la curva		
        L=len(in0)

        # Se recalcula la curva SER. 
        for i in range(0,L):
            ipoint=input_items[0][i] 
            self.errores[ipoint] += int(in0[i]!=in1[i])
            self.SER[ipoint]=self.errores[ipoint]/self.count[ipoint]
            self.count[ipoint] = self.count[ipoint]+1

        # La salida es simplemente la curva de SER
        output_items[0][:]=self.SER
        return len(output_items[0])

