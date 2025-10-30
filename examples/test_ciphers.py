#!/usr/bin/env python3
"""
Run example encrypt/decrypt operations for AES, DES, Playfair, and Vigenère.
Outputs are written to examples/output/.
"""
import os
import sys
from pathlib import Path

# Ensure project root is on sys.path so we can import cipher modules when running this file
THIS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = THIS_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from aes_cipher import AESCipher
from des_cipher import DESCipher
from playfair_cipher import PlayfairCipher
from vigenere_cipher import VigenereCipher


def read_text(path: Path) -> str:
    return path.read_text(encoding="ascii").strip()


def read_bytes(path: Path) -> bytes:
    return path.read_bytes()


def write_text(path: Path, data: str) -> None:
    path.write_text(data, encoding="ascii")


def write_bytes(path: Path, data: bytes) -> None:
    path.write_bytes(data)


def main() -> int:
    out_dir = THIS_DIR / "output"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Example inputs
    plaintext_txt = THIS_DIR / "plaintext.txt"
    test_file = THIS_DIR / "test_file.txt"

    # Keys and tables
    aes_key_file = THIS_DIR / "aes_key.txt"
    des_key_file = THIS_DIR / "des_key.txt"
    vigenere_key_file = THIS_DIR / "vigenere_key.txt"
    vigenere_table_file = THIS_DIR / "vigenere_table.txt"
    playfair_table_file = THIS_DIR / "playfair_table.txt"

    print("=== Running example operations ===")

    # AES
    try:
        key_bytes = read_text(aes_key_file).encode("ascii")
        data = read_bytes(test_file)
        aes = AESCipher(key_bytes)
        aes_enc = aes.encrypt_file(data)
        aes_dec = aes.decrypt_file(aes_enc)
        write_bytes(out_dir / "aes_encrypted.bin", aes_enc)
        write_bytes(out_dir / "aes_decrypted.txt", aes_dec)
        print(f"AES OK: round-trip match = {aes_dec == data}")
    except Exception as e:
        print(f"AES FAILED: {e}")

    # DES
    try:
        key_bytes = read_text(des_key_file).encode("ascii")
        data = read_bytes(test_file)
        des = DESCipher(key_bytes)
        des_enc = des.encrypt_file(data)
        des_dec = des.decrypt_file(des_enc)
        write_bytes(out_dir / "des_encrypted.bin", des_enc)
        write_bytes(out_dir / "des_decrypted.txt", des_dec)
        print(f"DES OK: round-trip match = {des_dec == data}")
    except Exception as e:
        print(f"DES FAILED: {e}")

    # Playfair
    try:
        table_content = read_text(playfair_table_file)
        message = plaintext_txt.read_text(encoding="ascii")
        playfair = PlayfairCipher.from_matrix(table_content)
        pf_enc = playfair.encrypt(message)
        pf_dec = playfair.decrypt(pf_enc)
        write_text(out_dir / "playfair_encrypted.txt", pf_enc)
        write_text(out_dir / "playfair_decrypted.txt", pf_dec)
        # Note: Playfair removes spaces and may insert filler 'X', so original != decrypted
        print("Playfair OK: produced encrypted and decrypted outputs (round-trip not exact by design)")
    except Exception as e:
        print(f"Playfair FAILED: {e}")

    # Vigenère
    try:
        table_content = vigenere_table_file.read_text(encoding="ascii")
        key = read_text(vigenere_key_file)
        message = plaintext_txt.read_text(encoding="ascii")
        vigenere = VigenereCipher.from_table(key, table_content)
        vig_enc = vigenere.encrypt(message)
        vig_dec = vigenere.decrypt(vig_enc)
        write_text(out_dir / "vigenere_encrypted.txt", vig_enc)
        write_text(out_dir / "vigenere_decrypted.txt", vig_dec)
        print(f"Vigenère OK: round-trip match = {vig_dec == message.upper()}")
    except Exception as e:
        print(f"Vigenère FAILED: {e}")

    print(f"Outputs written to: {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
