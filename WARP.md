# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Commands

- Install deps: `pip install -r requirements.txt`
- Run GUI (recommended): `python gui.py`
- Run CLI: `python main.py`
- Build: No build step (pure Python)
- Lint: Not configured in this repo
- Tests: No test suite detected

## Important usage notes (from README)

- AES/DES operate on binary files; Playfair/Vigenère operate on ASCII text files.
- Key/table files are required:
  - AES: key file must be 16, 24, or 32 bytes
  - DES: key file must be exactly 8 bytes
  - Playfair: provide a 5x5 matrix (25 letters, J merged into I)
  - Vigenère: provide a 26x26 table (676 letters) and a key file
- The README references example inputs in `examples/` (keys, tables, sample plaintext).

## High-level architecture

- Entry points
  - `gui.py` — Tkinter desktop app wrapping all ciphers with a polished UI (theme toggle, file pickers, status log). Orchestrates file I/O and dispatches to cipher classes.
  - `main.py` — Simple CLI menu that prompts for files and operations, then invokes cipher classes.
- Cipher implementations
  - `aes_cipher.py` — AES-CBC using PyCryptodome. For files, writes IV||ciphertext (IV is first 16 bytes). Text helpers use base64 iv:ciphertext format.
  - `des_cipher.py` — DES-CBC using PyCryptodome. For files, writes IV||ciphertext (IV is first 8 bytes). Text helpers use base64 iv:ciphertext format.
  - `playfair_cipher.py` — Classical Playfair with 5x5 matrix (J→I). Can construct from a provided 25-letter table; text sanitization and digraph handling included.
  - `vigenere_cipher.py` — Classical Vigenère. Supports custom 26×26 table from file; otherwise can generate a standard table.
- Data flow & I/O conventions
  - GUI/CLI read key/table files and input file, route to chosen cipher and operation, then write result to output file.
  - Modern ciphers use binary I/O with padding; classical ciphers use ASCII I/O and preserve non-letters where applicable.
  - Errors are surfaced to console (CLI) or status/log + message box (GUI).

## Developing here

- Add new ciphers by following the pattern of a small class exposing encrypt/decrypt and (optionally) file helpers; wire into `gui.py` (radio option + execute_* method) and `main.py` (menu + runner).
- If you introduce linting/tests, prefer adding configuration files (e.g., Ruff/Flake8, pytest) and update this section with exact commands (e.g., `pytest -k <name>` for a single test).
