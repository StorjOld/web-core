import os

def to62(i):
    if i < 10:
        return chr(i + ord('0'))
    elif i < 10+26:
        return chr(i-10 + ord('A'))
    else:
        return chr(i-10-26 + ord('a'))


def generate():
    """Generate random alphanumeric token.

    This uses os.urandom as a source of randomness.

    """
    randomness = os.urandom(12)

    # convert byte array to alphanumeric array (base 256 to base 62)

    n   = reduce(lambda x,y: 256*x + y, (ord(c) for c in randomness), 0)
    arr = reduce(lambda x,y: (x[0] + [x[1]%62], x[1]/62), xrange(0, 16), ([], n))[0]

    return "".join(to62(v) for v in arr)

if __name__ == "__main__":
    print generate()

