from typing import Self, Any
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

# digest = hashes.Hash(hashes.SHA256(), default_backend())
# digest.update(b"abc")
# digest.update(b"124")
# hash = digest.finalize()
# print(hash)

class SomeClass:
    num = 8888
    def __init__(self, string):
        self.string = string
    def __repr__(self):
        return str(f"{self.num}{self.string}")

class CBlock: 
    data: Any = None 
    prevHash: bytes | None = None
    prevBlock: Self | None = None

    def __init__(self, data: Any, prevBlock: Self | None):
        self.data = data 
        self.prevBlock = prevBlock
        self.prevHash = prevBlock.computeHash() if prevBlock else None

    def computeHash(self) -> bytes:
        digest = hashes.Hash(hashes.SHA256(), default_backend())
        digest.update(bytes(str(self.data), 'utf8'))
        if self.prevHash: digest.update(self.prevHash)
        return digest.finalize()

if __name__ == "__main__":
    root = CBlock("Root block", None)
    b1 = CBlock("I am block 1", root)
    b2 = CBlock("I am block 2", b1)
    b3 = CBlock(12345, b2)
    b4 = CBlock(SomeClass('fdsa'), b3)
    b5 = CBlock("Top block", b4)

    for b in [b1, b2, b3, b4, b5]:
        if b.prevBlock and b.prevBlock.computeHash() == b.prevHash:
            print('Hash is good')
        else:
            print('Hash is not good')

    b3.data = 9999
    if b4.prevBlock and b4.prevBlock.computeHash() == b4.prevHash:
        print('Tampering not detected')
    else:
        print('Tampering detected')

    b4.data.num = 9090
    if b5.prevBlock and b5.prevBlock.computeHash() == b5.prevHash:
        print('Tampering not detected')
    else:
        print('Tampering detected')
