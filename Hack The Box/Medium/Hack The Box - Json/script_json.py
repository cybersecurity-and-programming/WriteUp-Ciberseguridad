#!/usr/bin/env python3
import argparse
import base64
import hashlib
from Crypto.Cipher import DES3
from Crypto.Util.Padding import unpad

def derive_key(key_str: bytes) -> bytes:
    """
    Deriva una clave válida de 16 o 24 bytes para 3DES a partir de un string.
    Se usa MD5 para generar 16 bytes.
    """
    return hashlib.md5(key_str).digest()

def decrypt(cipher_b64: str, key_str: bytes, encoding: str = "utf-8") -> str:
    """
    Descifra un texto en base64 usando 3DES en modo ECB.
    """
    ciphertext = base64.b64decode(cipher_b64)
    key = derive_key(key_str)
    cipher = DES3.new(key, DES3.MODE_ECB)
    plaintext = unpad(cipher.decrypt(ciphertext), DES3.block_size)
    return plaintext.decode(encoding, errors="ignore")

def main():
    parser = argparse.ArgumentParser(description="Desencriptador 3DES ECB con clave derivada por MD5")
    parser.add_argument("--user", default="4as8gqENn26uTs9srvQLyg==", help="Texto cifrado en base64 del usuario")
    parser.add_argument("--password", default="oQ5iORgUrswNRsJKH9VaCw==", help="Texto cifrado en base64 de la contraseña")
    parser.add_argument("--key", default="_5TL#+GWWFv6pfT3!GXw7D86pkRRTv+$$tk^cL5hdU%", help="Clave base para derivar la key")
    args = parser.parse_args()

    try:
        username = decrypt(args.user, args.key.encode())
        password = decrypt(args.password, args.key.encode())
        print(f"[+] Username: {username}")
        print(f"[+] Password: {password}")
    except Exception as e:
        print(f"[!] Error al descifrar: {e}")

if __name__ == "__main__":
    main()
