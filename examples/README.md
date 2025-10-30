# Examples

This folder contains ready-to-use files for the GUI and CLI.

Modern ciphers (binary I/O):
- AES keys: `examples/aes/key_128.txt`, `key_192.txt`, `key_256.txt`
- DES key: `examples/des/key_08.txt`
- Sample input: `examples/sample.bin`

Classical ciphers (ASCII I/O):
- Playfair table: `examples/playfair/table_secure.txt` (5x5, J merged into I)
- Vigenère keys: `examples/vigenere/key_long.txt`, `key_phrase.txt`
- Vigenère table: `examples/vigenere_table.txt`
- Plaintexts: `examples/classical/plaintext_with_spaces.txt`, `plaintext_with_punct.txt`, `examples/plaintext.txt`

Usage:
- AES/DES: choose a key file and `examples/sample.bin` as input; pick any output path.
- Playfair: choose the Playfair table and a classical plaintext; pick an output path.
- Vigenère: choose `vigenere_table.txt`, a Vigenère key file, and a classical plaintext; pick an output path.
