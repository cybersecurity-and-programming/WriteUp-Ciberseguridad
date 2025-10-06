#!/usr/bin/python3
import signal,string,random,sys

def exit_handler(sig, frame):
	print("\n[!] Saliendo de la aplicacion...")
	sys.exit(1)
	
#evento para controlar la salida de la aplicacion con Ctrl+C
signal.signal(signal.SIGINT, exit_handler)

def xor_operation(i, selected):
    return i ^ int(ord(selected[0])) ^ int(ord(selected[1])) ^ int(ord(selected[2])) ^ int(ord(selected[9])) ^ int(ord(selected[13]))
    
# Definimos una función para comprobar si la suma de los elementos es correcta
def check_sum(xored, indices, target_sum):
    return sum(xored[i] for i in indices) == target_sum
    
def get_token():
    token = 0
    letters = string.ascii_letters + string.digits
    secret = [18, 1, 18, 4, 66, 20, 6, 31, 7, 22, 1, 16, 64, 0]
    
    while not token:
        current_selected = random.sample(letters, 14)
                
        # Utilizamos la función map para aplicar la operación XOR a cada elemento de 'secret'
        xored = list(map(lambda i: xor_operation(i, current_selected), secret))
        if check_sum(xored, [0, 1, 2], 308) and check_sum(xored, [7, 8, 9], 325) and check_sum(xored, [11, 12, 13], 265):
            l = list(map(chr, xored[::-1]))
            print("".join(l))
            token = 1
if __name__ == '__main__':
    get_token()
