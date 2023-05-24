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

