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
        total_in = 0
        total_out = 0
        data = self.__gather()

        # inputs validations
        for addr, amount in self.inputs:
            found = False
            for sig in self.sigs:
                if signatures.verify(data, sig, addr):
                    found = True
            if not found:
                return False
            if amount < 0:
                return False
            total_in += amount

        # output validations
        for _, amount in self.outputs:
            if amount < 0:
                return False
            total_out += amount

        # required addresses validations
        for addr in self.reqd: 
            found = False
            for sig in self.sigs:
                if signatures.verify(data, sig, addr):
                    found = True
            if not found:
                return False

        if total_in < total_out: 
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

    # These tx must be wrong
    # Wrong sig
    Tx4 = Tx()
    Tx4.add_input(pu1, 1)
    Tx4.add_output(pu2, 1)
    Tx4.sign(pr2)

    # Escrow tx not signed by arbiter
    Tx5 = Tx()
    Tx5.add_input(pu3, 1.2)
    Tx5.add_output(pu1, 1.1)
    Tx5.add_reqd(pu4)
    Tx5.sign(pr3)

    # two inputs addres, signed by one
    Tx6 = Tx()
    Tx6.add_input(pu3, 1)
    Tx6.add_input(pu4, 0.1)
    Tx6.add_output(pu1, 1.1)
    Tx6.sign(pr3)

    # outputs exceed inputs
    Tx7 = Tx()
    Tx7.add_input(pu4, 1.2)
    Tx7.add_output(pu1, 1)
    Tx7.add_output(pu2, 2)
    Tx7.sign(pr4)

    # negative values
    Tx8 = Tx()
    Tx8.add_input(pu2, -1)
    Tx8.add_output(pu1, -1)
    Tx8.sign(pr2)

    for t in [Tx4, Tx5, Tx6, Tx7, Tx8]:
        if t.is_valid():
            print('Wrong!')
        else:
            print('Right!')

