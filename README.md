# Cryptography Project

Implementation of classical and modern encryption algorithms in Python.

## Algorithms Implemented

- **AES (Advanced Encryption Standard)** - Modern symmetric encryption
- **DES (Data Encryption Standard)** - Legacy symmetric encryption
- **Playfair Cipher** - Classical digraph substitution cipher
- **Vigenère Cipher** - Classical polyalphabetic cipher

## Requirements

```
pycryptodome
```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

### File-Based Operations

All ciphers now operate on files:

#### Classical Ciphers (Vigenère & Playfair)
- Read from ASCII text files
- Write to ASCII text files
- Require table files and key files

#### Modern Ciphers (AES & DES)
- Read from binary files
- Write to binary files
- Require key files with specific lengths:
  - **AES**: 16, 24, or 32 bytes (128, 192, or 256 bits)
  - **DES**: 8 bytes (64 bits)

### Example Files

Example files are provided in the `examples/` directory:
- `aes_key.txt` - 16-byte AES key
- `des_key.txt` - 8-byte DES key
- `playfair_table.txt` - 5x5 Playfair matrix
- `vigenere_table.txt` - 26x26 Vigenère table
- `vigenere_key.txt` - Vigenère key
- `plaintext.txt` - Sample plaintext
- `test_file.txt` - Sample file for encryption

## Team

Collaborative project for cryptography implementation and analysis.

## License

MIT License
