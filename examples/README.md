# Examples

This folder contains ready-to-use files for the GUI and CLI.

Modern ciphers (binary I/O):
- AES keys: `examples/aes/key_128.txt`, `key_192.txt`, `key_256.txt`
- DES key: `examples/des/key_08.txt`
- Sample input: `examples/test_file.txt`

Classical ciphers (ASCII I/O):
- Playfair table: `examples/playfair/table_secure.txt` (5x5, J merged into I)
- Vigenère keys: `examples/vigenere/key_long.txt`, `key_phrase.txt`
- Vigenère table: `examples/vigenere_table.txt`
- Plaintexts: `examples/classical/plaintext_with_spaces.txt`, `examples/plaintext.txt`, `examples/classical/plaintext_with_punct.txt`

Usage:
- AES/DES: choose a key file and `examples/test_file.txt` as input; pick any output path.
- Playfair: choose the Playfair table and a classical plaintext; pick an output path.
- Vigenère: choose `vigenere_table.txt`, a Vigenère key file, and a classical plaintext; pick an output path.

---

Automated quick tests:

Run a script that exercises all ciphers using the example files and writes outputs to `examples/output/`:

- PowerShell (Windows):
  python examples/test_ciphers.py

- Bash (macOS/Linux):
  python3 examples/test_ciphers.py

The script will:
- AES/DES: encrypt and decrypt `examples/test_file.txt`
- Playfair/Vigenère: encrypt and decrypt `examples/plaintext.txt`
- Save results to `examples/output/`
