# todo: import signatures

class Tx:
    inputs = None
    outputs = None
    sigs = None
    reqd = None

    def __init__(self) -> None:
        self.inputs = []
        self.outputs = []
        self.sigs = []
        self.reqd = []

    def add_input(self, from_address, amount):
        pass

    def add_output(self, to_address, amount):
        pass

    def add_reqd(self, address):
        pass

    def sign(self, private):
        pass

    def is_valid(self):
        return False

if __name__ == "__main__":
    pr1, pu1 = signatures.generate_keys()
    pr2, pu2 = signatures.generate_keys()
    pr3, pu3 = signatures.generate_keys()
    pr4, pu4 = signatures.generate_keys()

    Tx1 = Tx()
    Tx1.add_input(pu1, 1)
    Tx1.add_output(pu2, 1)
    Tx1.sign(pr1)

    if Tx1.is_valid():
        print('Success')
    else:
        print('Error')
