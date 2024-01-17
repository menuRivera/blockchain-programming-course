# The next two lines are for adding the parent directory in the pythonpath
from site import addsitedir
addsitedir('..')

import pickle
# from blockchain.blockchain import CBlock
from blockchain import CBlock
import signatures
from signatures import sign, verify
from transactions import Tx

class TxBlock(CBlock): 
    def __init__(self, prevBlock):
        super(TxBlock, self).__init__([], prevBlock)

    def add_tx(self, tx_in): 
        self.data.append(tx_in)

    def is_valid(self):
        if not super(TxBlock, self).is_valid():
            return False
        for tx in self.data:
            if not tx.is_valid():
                return False

            return True

if __name__ == "__main__":
    pr1, pu1_ser = signatures.generate_keys()
    pr2, pu2_ser = signatures.generate_keys()
    pr3, pu3_ser = signatures.generate_keys()

    Tx1 = Tx()
    Tx1.add_input(pu1_ser, 1)
    Tx1.add_output(pu2_ser, 1)
    Tx1.sign(pr1)

    # is correct
    # print(Tx1.is_valid())

    savefile = open("tx.dat", "wb")
    pickle.dump(Tx1, savefile)
    savefile.close()

    loadfile = open("tx.dat", "rb")
    loaded_tx = pickle.load(loadfile)

    # is correct
    # print(loaded_tx.is_valid())
    loadfile.close()

    root = TxBlock(None) 
    root.add_tx(Tx1)
    
    Tx2 = Tx()
    Tx2.add_input(pu2_ser, 1.1)
    Tx2.add_output(pu3_ser, 1)
    Tx2.sign(pr2)

    root.add_tx(Tx2)

    B1 = TxBlock(root)

    Tx3 = Tx()
    Tx3.add_input(pu3_ser, 1.1)
    Tx3.add_output(pu1_ser, 1)
    Tx3.sign(pr3)

    B1.add_tx(Tx3)

    Tx4 = Tx()
    Tx4.add_input(pu1_ser, 1)
    Tx4.add_output(pu2_ser, 1)
    Tx4.add_reqd(pu3_ser)
    Tx4.sign(pr1)
    Tx4.sign(pr3)

    B1.add_tx(Tx4)

    # B1.is_valid()
    # root.is_valid()

    savefile = open('block.dat', 'wb')
    pickle.dump(B1, savefile)
    savefile.close()

    loadfile = open('block.dat', 'rb')
    load_B1 = pickle.load(loadfile)

    load_B1.is_valid()
    for b in [root, B1, load_B1, load_B1.prevBlock]:
        if b.is_valid():
            print("Success!: good block")
        else:
            print("Error!: Bad block")

    B2 = TxBlock(B1)
    Tx5 = Tx()
    Tx5.add_input(pu3_ser, 1)
    Tx5.add_output(pu1_ser, 100)
    Tx5.sign(pr3)
    B2.add_tx(Tx5)

    load_B1.prevBlock.add_tx(Tx4)

    for b in [B2, load_B1]:
        if b.is_valid():
            print("Error: Bad block valid somehow")
        else:
            print("Success: bad block detected")
