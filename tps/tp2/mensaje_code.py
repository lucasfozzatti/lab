from converter import a_bits
import os

def mess(mensaj):
    mens = open(mensaj, "rb").read().decode()
    mensa = a_bits(mens, '2')
    mens = ''.join([str(elem) for elem in mensa])
    sis = os.path.getsize(mensaj)
    return mens, sis