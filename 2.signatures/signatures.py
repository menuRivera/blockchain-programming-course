def generate_keys():
    private='privkeyblabla'
    public='publkeyblabla'
    return private, public

def sign(message, private):
    sig='xllgllf'
    return sig

def verify(message, sig, public):
    return False

if __name__ == "__main__":
    pr, pu = generate_keys()
    message = 'This is a message'
    sig = sign(message, pr)
    correct = verify(message, sig, pu)

    if correct:
        print('Correct')
    else:
        print('Incorrect')
