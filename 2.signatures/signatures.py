from typing import Tuple
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey, RSAPrivateKey
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature


def generate_keys() -> Tuple[RSAPrivateKey, RSAPublicKey]: 
    _pr = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
                backend=default_backend()
            )
    _pu = _pr.public_key()
    return _pr, _pu

def sign(message:bytes, private:RSAPrivateKey) -> bytes:
    _sig = private.sign(
                data=message,
                padding=padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH
                    ),
                algorithm=hashes.SHA256()
            )
    return _sig

def verify(message:bytes, sig:bytes, public:RSAPublicKey) -> bool:
    try:
        public.verify(
                   signature=sig,
                   data=message,
                   padding=padding.PSS(
                           mgf=padding.MGF1(hashes.SHA256()),
                           salt_length=padding.PSS.MAX_LENGTH
                       ),
                   algorithm=hashes.SHA256()
                )
        return True
    except InvalidSignature:
        print('Invalid signature')
        return False
    except:
        print('Generic error')
        return False

if __name__ == "__main__":
    pr, pu = generate_keys()
    message:bytes = b'This is a message'
    sig:bytes = sign(message, pr)

    # this will be correct
    print('test 1')
    if verify(message, sig, pu):
        print('Correct')
    else:
        print('Incorrect')
    print('\n')

    pr2, pu2 = generate_keys()

    print('test 2')
    # This will be incorrect
    if verify(message, sig, pu2):
        print('Correct')
    else:
        print('Incorrect')
    
