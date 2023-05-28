# The next two lines are for adding the parent directory in the pythonpath
from site import addsitedir
addsitedir('..')

import signatures.signatures as signatures

class Tx:
    inputs = []
    outputs = []
    sigs = []
    reqd = []

    def __init__(self) -> None:
        self.inputs = []
        self.outputs = []
        self.sigs = []
        self.reqd = []

    def add_input(self, from_address, amount):
        self.inputs.append((from_address, amount))

    def add_output(self, to_address, amount):
        self.outputs.append((to_address, amount))

    def add_reqd(self, address):
        self.reqd.append(address)

    def sign(self, private):
        message = self.__gather()
        self.sigs.append(signatures.sign(message, private)) 

    def is_valid(self):
        data = self.__gather()
        for addr, amount in self.inputs:
            found = False
            for s in self.sigs:
                if signatures.verify(data, s, addr):
                    found = True
            if not found:
                return False
        return True

    def __gather(self):
        data = []
        data.append(self.inputs)
        data.append(self.outputs)
        data.append(self.reqd)
        return bytes(str(data), 'utf-8')

if __name__ == "__main__":
    pr1, pu1 = signatures.generate_keys()
    pr2, pu2 = signatures.generate_keys()
    pr3, pu3 = signatures.generate_keys()
    pr4, pu4 = signatures.generate_keys()

    Tx1 = Tx()
    Tx1.add_input(pu1, 1)
    Tx1.add_output(pu2, 1)
    Tx1.sign(pr1)
    Tx2 = Tx()
    Tx2.add_input(pu1, 2)
    Tx2.add_output(pu2, 1)
    Tx2.add_output(pu3, 1)
    Tx2.sign(pr1)

    Tx3 = Tx()
    Tx3.add_input(pu3, 1.2)
    Tx3.add_output(pu1, 1.1)
    Tx3.add_reqd(pu4)
    Tx3.sign(pr3)
    Tx3.sign(pr4)

    for t in [Tx1, Tx2, Tx3]:
        if t.is_valid():
            print('Valid transaction')
        else:
            print('Invalid transaction')

    # Wrong transaction
    Tx4 = Tx()
    Tx4.add_input(pu1, 1)
    Tx4.add_output(pu2, 1)
    Tx4.sign(pr2)

    # Two input addres signed by one
    Tx5 = Tx()
    Tx5.add_input(pu3, 1)
    Tx5.add_input(pu4, 1)
    Tx5.add_output(pu1, 2)
    Tx5.sign(pr3)

    for t in [Tx4, Tx5]:
        if t.is_valid():
            print('Wrong!')
        else:
            print('Right!')
