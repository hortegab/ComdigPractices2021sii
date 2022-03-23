import numpy as np
from gnuradio import gr

class inversedB(gr.sync_block):  

    def __init__(self, ): 
        gr.sync_block.__init__(
            self,
            name='e_inversedB_ff',
            in_sig=[np.float32],
            out_sig=[np.float32]
        )

    def work(self, input_items, output_items):
        x=input_items[0]
        y=output_items[0]
        y[:]=np.power(10,x)
        return len(y)
