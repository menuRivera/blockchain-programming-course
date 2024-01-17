# The next two lines are for adding the parent directory in the pythonpath
from site import addsitedir
addsitedir('..')

import pickle
from blockchain.blockchain import CBlock
import signatures.signatures as signatures
from signatures.signatures import sign, verify
from transactions.transactions import Tx

class TxBlock(CBlock): 
    def __init__(self, prevBlock):
        pass
    def add_tx(self, tx_in): 
        pass
    def is_valid(self):
        return False

if __name__ == "__main__":
    pr1, pu1_ser = signatures.generate_keys()
    pr2, pu2_ser = signatures.generate_keys()
    pr3, pu3_ser = signatures.generate_keys()

    Tx1 = Tx()
    Tx1.add_input(pu1_ser, 1)
    Tx1.add_output(pu2_ser, 1)
    Tx1.sign(pr1)

    print(Tx1.is_valid())


    savefile = open("tx.dat", "wb")
    pickle.dump(Tx1, savefile)
    savefile.close()

    loadfile = open("tx.dat", "rb")
    loaded_tx = pickle.load(loadfile)

    print(loaded_tx.is_valid())
    loadfile.close()
