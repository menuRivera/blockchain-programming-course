from typing import Tuple
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey, RSAPrivateKey
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization

def generate_keys() -> Tuple[RSAPrivateKey, bytes]: 
    private = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
       backend=default_backend()
    )    
    public = private.public_key()
    # serialize public key
    pu_ser = public.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )    
    return private, pu_ser

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

def verify(message:bytes, sig:bytes, pu_ser:bytes) -> bool:
    # deserialize public key
    public = serialization.load_pem_public_key(
        pu_ser,
        backend=default_backend()
    )

    # message = bytes(str(message), 'utf-8')
    try:
        if isinstance(public, RSAPublicKey):
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
        else:
            print("Not RSAPublicKey :(")
            return False
    except InvalidSignature:
        return False
    except:
        print("Error executing public_key.verify")
        return False

if __name__ == "__main__":
    pr, pu_ser = generate_keys()
    message:bytes = b"This is a message"
    sig:bytes = sign(message, pr)

    # this should be correct
    if verify(message, sig, pu_ser):
        print('Correct')
    else:
        print('Incorrect')

    pr2, pu2_ser = generate_keys()

    # This should be incorrect
    if verify(message, sig, pu2_ser):
        print('Incorrect')
    else:
        print('Correct')
    
