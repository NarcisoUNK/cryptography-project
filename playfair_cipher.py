"""
Playfair Cipher Implementation
Classical digraph substitution cipher using a 5x5 matrix
"""


class PlayfairCipher:
    def __init__(self, key=None, matrix=None):
        """Initialize Playfair cipher with a key or matrix"""
        if matrix is not None:
            self.matrix = matrix
            self.key = ""
        else:
            self.key = key.upper().replace('J', 'I')
            self.matrix = self._create_matrix()
    
    def _create_matrix(self):
        """Create 5x5 Playfair matrix from key"""
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # No J
        key_string = ""
        
        # Add unique characters from key
        for char in self.key:
            if char.isalpha() and char not in key_string:
                key_string += char
        
        # Add remaining alphabet
        for char in alphabet:
            if char not in key_string:
                key_string += char
        
        # Create 5x5 matrix
        matrix = []
        for i in range(5):
            matrix.append(list(key_string[i*5:(i+1)*5]))
        
        return matrix
    
    def _find_position(self, char):
        """Find position of character in matrix"""
        for i, row in enumerate(self.matrix):
            for j, c in enumerate(row):
                if c == char:
                    return i, j
        return None
    
    def _prepare_text(self, text):
        """Prepare text for encryption (remove spaces, handle duplicates)"""
        text = text.upper().replace('J', 'I').replace(' ', '')
        prepared = ""
        
        i = 0
        while i < len(text):
            if not text[i].isalpha():
                i += 1
                continue
            
            prepared += text[i]
            
            if i + 1 < len(text):
                if text[i] == text[i + 1]:
                    prepared += 'X'
                else:
                    prepared += text[i + 1]
                    i += 1
            else:
                prepared += 'X'
            
            i += 1
        
        return prepared
    
    def encrypt(self, plaintext):
        """Encrypt plaintext using Playfair cipher"""
        plaintext = self._prepare_text(plaintext)
        ciphertext = ""
        
        for i in range(0, len(plaintext), 2):
            row1, col1 = self._find_position(plaintext[i])
            row2, col2 = self._find_position(plaintext[i + 1])
            
            if row1 == row2:  # Same row
                ciphertext += self.matrix[row1][(col1 + 1) % 5]
                ciphertext += self.matrix[row2][(col2 + 1) % 5]
            elif col1 == col2:  # Same column
                ciphertext += self.matrix[(row1 + 1) % 5][col1]
                ciphertext += self.matrix[(row2 + 1) % 5][col2]
            else:  # Rectangle
                ciphertext += self.matrix[row1][col2]
                ciphertext += self.matrix[row2][col1]
        
        return ciphertext
    
    def decrypt(self, ciphertext):
        """Decrypt ciphertext using Playfair cipher"""
        plaintext = ""
        
        for i in range(0, len(ciphertext), 2):
            row1, col1 = self._find_position(ciphertext[i])
            row2, col2 = self._find_position(ciphertext[i + 1])
            
            if row1 == row2:  # Same row
                plaintext += self.matrix[row1][(col1 - 1) % 5]
                plaintext += self.matrix[row2][(col2 - 1) % 5]
            elif col1 == col2:  # Same column
                plaintext += self.matrix[(row1 - 1) % 5][col1]
                plaintext += self.matrix[(row2 - 1) % 5][col2]
            else:  # Rectangle
                plaintext += self.matrix[row1][col2]
                plaintext += self.matrix[row2][col1]
        
        return plaintext
    
    @classmethod
    def from_matrix(cls, table_content):
        """Create PlayfairCipher from a table file content"""
        # Parse the table - expecting 25 characters (5x5 matrix)
        # Can be formatted as lines or continuous text
        chars = ''.join(c.upper() for c in table_content if c.isalpha())
        
        if len(chars) != 25:
            raise ValueError(f"Table must contain exactly 25 alphabetic characters, got {len(chars)}")
        
        # Create 5x5 matrix
        matrix = []
        for i in range(5):
            matrix.append(list(chars[i*5:(i+1)*5]))
        
        return cls(matrix=matrix)
