"""
Cryptography Project - GUI Application
Professional interface for AES, DES, Playfair, and Vigenère ciphers
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
from aes_cipher import AESCipher
from des_cipher import DESCipher
from playfair_cipher import PlayfairCipher
from vigenere_cipher import VigenereCipher


class ToolTip:
    """Create a tooltip for a widget"""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
    
    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(self.tooltip, text=self.text, 
                        background="#2d2d2d", foreground="#ffffff",
                        relief="solid", borderwidth=1,
                        font=("Segoe UI", 9), padx=8, pady=6)
        label.pack()
    
    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None


class CryptographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cryptography Suite - AES, DES, Playfair & Vigenère")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Configure style
        self.setup_style()
        
        # Variables
        self.key_file_path = tk.StringVar()
        self.table_file_path = tk.StringVar()
        self.input_file_path = tk.StringVar()
        self.output_file_path = tk.StringVar()
        self.cipher_type = tk.StringVar(value="AES")
        self.operation_type = tk.StringVar(value="encrypt")
        
        # Build UI
        self.create_widgets()
        
    def setup_style(self):
        """Configure modern dark mode styling"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Dark mode colors
        bg_dark = "#1e1e1e"
        bg_darker = "#252526"
        bg_lighter = "#2d2d30"
        fg_primary = "#e4e4e4"
        fg_secondary = "#b0b0b0"
        accent_blue = "#0078d4"
        accent_green = "#16c60c"
        accent_red = "#e81123"
        border_color = "#3e3e42"
        
        # Configure root
        self.root.configure(bg=bg_dark)
        
        # Frame styles
        style.configure("TFrame", background=bg_dark)
        style.configure("TLabelframe", background=bg_dark, 
                       foreground=fg_primary, bordercolor=border_color,
                       relief="solid")
        style.configure("TLabelframe.Label", background=bg_dark, 
                       foreground=fg_primary, font=("Segoe UI", 10, "bold"))
        
        # Label styles
        style.configure("Title.TLabel", font=("Segoe UI", 26, "bold"), 
                       foreground=accent_blue, background=bg_dark)
        style.configure("Subtitle.TLabel", font=("Segoe UI", 11), 
                       foreground=fg_secondary, background=bg_dark)
        style.configure("Header.TLabel", font=("Segoe UI", 10, "bold"), 
                       foreground=fg_primary, background=bg_dark)
        style.configure("TLabel", font=("Segoe UI", 9), 
                       foreground=fg_primary, background=bg_dark)
        
        # Button styles
        style.configure("TButton", font=("Segoe UI", 10), padding=10,
                       background=bg_lighter, foreground=fg_primary,
                       bordercolor=border_color, borderwidth=1)
        style.map("TButton",
                 background=[("active", bg_darker), ("pressed", bg_darker)],
                 foreground=[("active", fg_primary)])
        
        style.configure("Accent.TButton", font=("Segoe UI", 11, "bold"),
                       background=accent_blue, foreground="#ffffff", padding=12)
        style.map("Accent.TButton",
                 background=[("active", "#005a9e"), ("pressed", "#004578")])
        
        # Entry styles
        style.configure("TEntry", fieldbackground=bg_lighter, 
                       foreground=fg_primary, bordercolor=border_color,
                       insertcolor=fg_primary)
        
        # Radiobutton styles
        style.configure("TRadiobutton", font=("Segoe UI", 10),
                       background=bg_dark, foreground=fg_primary,
                       indicatorbackground=bg_lighter,
                       indicatorforeground=accent_blue)
        style.map("TRadiobutton",
                 background=[("active", bg_dark)],
                 foreground=[("active", accent_blue)])
        
    def create_widgets(self):
        """Create all UI components"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🔐 Cryptography Suite", style="Title.TLabel")
        title_label.grid(row=0, column=0, pady=(0, 5), sticky=tk.W)
        
        subtitle_label = ttk.Label(main_frame, 
                                   text="Professional encryption and decryption tool",
                                   style="Subtitle.TLabel")
        subtitle_label.grid(row=1, column=0, pady=(0, 20), sticky=tk.W)
        
        # Status/Log Area (create first so log() can be called)
        self.create_status_area(main_frame, row=6)
        
        # Cipher Selection
        self.create_cipher_selection(main_frame, row=2)
        
        # Operation Selection
        self.create_operation_selection(main_frame, row=3)
        
        # File Inputs Section
        self.create_file_inputs(main_frame, row=4)
        
        # Action Buttons
        self.create_action_buttons(main_frame, row=5)
        
    def create_cipher_selection(self, parent, row):
        """Create cipher selection section"""
        frame = ttk.LabelFrame(parent, text="Select Cipher Algorithm", padding="15")
        frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)
        frame.columnconfigure(3, weight=1)
        
        ciphers = [
            ("AES (Advanced Encryption Standard)", "AES"),
            ("DES (Data Encryption Standard)", "DES"),
            ("Playfair Cipher", "PLAYFAIR"),
            ("Vigenère Cipher", "VIGENERE")
        ]
        
        for i, (text, value) in enumerate(ciphers):
            rb = ttk.Radiobutton(frame, text=text, variable=self.cipher_type, 
                                value=value, command=self.on_cipher_change)
            rb.grid(row=0, column=i, padx=10, pady=5, sticky=tk.W)
            
    def create_operation_selection(self, parent, row):
        """Create operation selection section"""
        frame = ttk.LabelFrame(parent, text="Select Operation", padding="15")
        frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        ttk.Radiobutton(frame, text="🔒 Encrypt", variable=self.operation_type, 
                       value="encrypt").grid(row=0, column=0, padx=20, pady=5)
        ttk.Radiobutton(frame, text="🔓 Decrypt", variable=self.operation_type, 
                       value="decrypt").grid(row=0, column=1, padx=20, pady=5)
        
    def create_file_inputs(self, parent, row):
        """Create file input section"""
        frame = ttk.LabelFrame(parent, text="File Configuration", padding="15")
        frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        frame.columnconfigure(1, weight=1)
        
        current_row = 0
        
        # Key file
        self.key_label = ttk.Label(frame, text="Key File: ⓘ", style="Header.TLabel")
        self.key_label.grid(row=current_row, column=0, sticky=tk.W, pady=5)
        ToolTip(self.key_label, "Text file containing encryption key.\n" +
                                "AES: 16, 24, or 32 bytes\n" +
                                "DES: Exactly 8 bytes\n" +
                                "Vigenère: Any alphabetic key")
        
        key_entry = ttk.Entry(frame, textvariable=self.key_file_path, state="readonly")
        key_entry.grid(row=current_row, column=1, sticky=(tk.W, tk.E), padx=10, pady=5)
        
        self.key_btn = ttk.Button(frame, text="Browse...", command=self.browse_key_file)
        self.key_btn.grid(row=current_row, column=2, pady=5)
        
        current_row += 1
        
        # Table file (for classical ciphers)
        self.table_label = ttk.Label(frame, text="Table File: ⓘ", style="Header.TLabel")
        self.table_label.grid(row=current_row, column=0, sticky=tk.W, pady=5)
        ToolTip(self.table_label, "Text file containing cipher table.\n" +
                                  "Playfair: 5x5 matrix (25 chars, no J)\n" +
                                  "Vigenère: 26x26 table (676 chars)")
        
        table_entry = ttk.Entry(frame, textvariable=self.table_file_path, state="readonly")
        table_entry.grid(row=current_row, column=1, sticky=(tk.W, tk.E), padx=10, pady=5)
        
        self.table_btn = ttk.Button(frame, text="Browse...", command=self.browse_table_file)
        self.table_btn.grid(row=current_row, column=2, pady=5)
        
        current_row += 1
        
        # Input file
        input_label = ttk.Label(frame, text="Input File: ⓘ", style="Header.TLabel")
        input_label.grid(row=current_row, column=0, sticky=tk.W, pady=5)
        ToolTip(input_label, "File to encrypt or decrypt.\n" +
                            "Modern ciphers (AES/DES): Any file type\n" +
                            "Classical ciphers: ASCII text only")
        
        input_entry = ttk.Entry(frame, textvariable=self.input_file_path, state="readonly")
        input_entry.grid(row=current_row, column=1, sticky=(tk.W, tk.E), padx=10, pady=5)
        
        ttk.Button(frame, text="Browse...", command=self.browse_input_file).grid(
            row=current_row, column=2, pady=5)
        
        current_row += 1
        
        # Output file
        output_label = ttk.Label(frame, text="Output File: ⓘ", style="Header.TLabel")
        output_label.grid(row=current_row, column=0, sticky=tk.W, pady=5)
        ToolTip(output_label, "Where to save the result.\n" +
                             "Extension will match operation type.")
        
        output_entry = ttk.Entry(frame, textvariable=self.output_file_path, state="readonly")
        output_entry.grid(row=current_row, column=1, sticky=(tk.W, tk.E), padx=10, pady=5)
        
        ttk.Button(frame, text="Browse...", command=self.browse_output_file).grid(
            row=current_row, column=2, pady=5)
        
        # Update visibility based on initial cipher selection
        self.on_cipher_change()
        
    def create_action_buttons(self, parent, row):
        """Create action buttons"""
        frame = ttk.Frame(parent)
        frame.grid(row=row, column=0, pady=15)
        
        self.execute_btn = ttk.Button(frame, text="▶ Execute Operation", 
                                      command=self.execute_operation,
                                      style="Accent.TButton")
        self.execute_btn.grid(row=0, column=0, padx=10)
        
        ttk.Button(frame, text="🗑 Clear All", command=self.clear_all).grid(
            row=0, column=1, padx=10)
        
    def create_status_area(self, parent, row):
        """Create status/log area"""
        frame = ttk.LabelFrame(parent, text="Status Log", padding="10")
        frame.grid(row=row, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        parent.rowconfigure(row, weight=1)
        
        self.status_text = scrolledtext.ScrolledText(frame, height=10, width=80,
                                                     font=("Consolas", 9),
                                                     wrap=tk.WORD,
                                                     bg="#1e1e1e",
                                                     fg="#d4d4d4",
                                                     insertbackground="#ffffff",
                                                     selectbackground="#264f78",
                                                     selectforeground="#ffffff",
                                                     relief="flat",
                                                     borderwidth=0)
        self.status_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        
        self.log("✨ Application ready. Select a cipher and configure files.")
        
    def on_cipher_change(self):
        """Handle cipher type change"""
        cipher = self.cipher_type.get()
        
        # Show/hide table file based on cipher type
        if cipher in ["PLAYFAIR", "VIGENERE"]:
            self.table_label.grid()
            self.table_btn.grid()
            
            if cipher == "PLAYFAIR":
                self.key_label.grid_remove()
                self.key_btn.grid_remove()
                self.log("🔑 Playfair selected: Table file required (5x5 matrix)")
            else:
                self.key_label.grid()
                self.key_btn.grid()
                self.log("🔑 Vigenère selected: Table file (26x26) and key file required")
        else:
            self.table_label.grid_remove()
            self.table_btn.grid_remove()
            self.key_label.grid()
            self.key_btn.grid()
            
            if cipher == "AES":
                self.log("🔒 AES selected: Key must be 16, 24, or 32 bytes")
            else:
                self.log("🔒 DES selected: Key must be exactly 8 bytes")
                
    def browse_key_file(self):
        """Browse for key file"""
        filename = filedialog.askopenfilename(
            title="Select Key File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.key_file_path.set(filename)
            self.log(f"📄 Key file selected: {os.path.basename(filename)}")
            
    def browse_table_file(self):
        """Browse for table file"""
        filename = filedialog.askopenfilename(
            title="Select Table File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.table_file_path.set(filename)
            self.log(f"📄 Table file selected: {os.path.basename(filename)}")
            
    def browse_input_file(self):
        """Browse for input file"""
        filename = filedialog.askopenfilename(
            title="Select Input File",
            filetypes=[("All files", "*.*")]
        )
        if filename:
            self.input_file_path.set(filename)
            self.log(f"📝 Input file selected: {os.path.basename(filename)}")
            
    def browse_output_file(self):
        """Browse for output file"""
        filename = filedialog.asksaveasfilename(
            title="Select Output File",
            filetypes=[("All files", "*.*")]
        )
        if filename:
            self.output_file_path.set(filename)
            self.log(f"💾 Output file selected: {os.path.basename(filename)}")
            
    def log(self, message):
        """Add message to status log"""
        self.status_text.insert(tk.END, f"[{self.get_timestamp()}] {message}\n")
        self.status_text.see(tk.END)
        
    def get_timestamp(self):
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")
        
    def clear_all(self):
        """Clear all inputs"""
        self.key_file_path.set("")
        self.table_file_path.set("")
        self.input_file_path.set("")
        self.output_file_path.set("")
        self.log("🧹 All fields cleared")
        
    def execute_operation(self):
        """Execute the selected cryptographic operation"""
        cipher = self.cipher_type.get()
        operation = self.operation_type.get()
        
        # Validate inputs
        if not self.input_file_path.get():
            messagebox.showerror("Error", "Please select an input file")
            return
            
        if not self.output_file_path.get():
            messagebox.showerror("Error", "Please select an output file")
            return
        
        self.log(f"⏳ Starting {operation} operation with {cipher}...")
        
        try:
            if cipher == "AES":
                self.execute_aes()
            elif cipher == "DES":
                self.execute_des()
            elif cipher == "PLAYFAIR":
                self.execute_playfair()
            elif cipher == "VIGENERE":
                self.execute_vigenere()
                
            self.log(f"✅ Operation completed successfully!")
            messagebox.showinfo("Success", 
                              f"File {operation}ed successfully!\n\nOutput: {os.path.basename(self.output_file_path.get())}")
            
        except Exception as e:
            self.log(f"❌ Error: {str(e)}")
            messagebox.showerror("Error", f"Operation failed:\n{str(e)}")
            
    def execute_aes(self):
        """Execute AES encryption/decryption"""
        if not self.key_file_path.get():
            raise ValueError("Please select a key file")
            
        # Read key
        with open(self.key_file_path.get(), 'r', encoding='ascii') as f:
            key = f.read().strip()
        
        key_bytes = key.encode('ascii')
        if len(key_bytes) not in [16, 24, 32]:
            raise ValueError(f"AES key must be 16, 24, or 32 bytes. Current: {len(key_bytes)} bytes")
        
        # Read input file
        with open(self.input_file_path.get(), 'rb') as f:
            data = f.read()
        
        aes = AESCipher(key_bytes)
        
        if self.operation_type.get() == "encrypt":
            result = aes.encrypt_file(data)
            self.log(f"🔒 Encrypted {len(data)} bytes → {len(result)} bytes")
        else:
            result = aes.decrypt_file(data)
            self.log(f"🔓 Decrypted {len(data)} bytes → {len(result)} bytes")
        
        # Write output
        with open(self.output_file_path.get(), 'wb') as f:
            f.write(result)
            
    def execute_des(self):
        """Execute DES encryption/decryption"""
        if not self.key_file_path.get():
            raise ValueError("Please select a key file")
            
        # Read key
        with open(self.key_file_path.get(), 'r', encoding='ascii') as f:
            key = f.read().strip()
        
        key_bytes = key.encode('ascii')
        if len(key_bytes) != 8:
            raise ValueError(f"DES key must be exactly 8 bytes. Current: {len(key_bytes)} bytes")
        
        # Read input file
        with open(self.input_file_path.get(), 'rb') as f:
            data = f.read()
        
        des = DESCipher(key_bytes)
        
        if self.operation_type.get() == "encrypt":
            result = des.encrypt_file(data)
            self.log(f"🔒 Encrypted {len(data)} bytes → {len(result)} bytes")
        else:
            result = des.decrypt_file(data)
            self.log(f"🔓 Decrypted {len(data)} bytes → {len(result)} bytes")
        
        # Write output
        with open(self.output_file_path.get(), 'wb') as f:
            f.write(result)
            
    def execute_playfair(self):
        """Execute Playfair encryption/decryption"""
        if not self.table_file_path.get():
            raise ValueError("Please select a table file")
            
        # Read table
        with open(self.table_file_path.get(), 'r', encoding='ascii') as f:
            table_content = f.read().strip()
        
        # Read input
        with open(self.input_file_path.get(), 'r', encoding='ascii') as f:
            message = f.read()
        
        playfair = PlayfairCipher.from_matrix(table_content)
        
        if self.operation_type.get() == "encrypt":
            result = playfair.encrypt(message)
            self.log(f"🔑 Encrypted {len(message)} characters → {len(result)} characters")
        else:
            result = playfair.decrypt(message)
            self.log(f"🔑 Decrypted {len(message)} characters → {len(result)} characters")
        
        # Write output
        with open(self.output_file_path.get(), 'w', encoding='ascii') as f:
            f.write(result)
            
    def execute_vigenere(self):
        """Execute Vigenère encryption/decryption"""
        if not self.table_file_path.get():
            raise ValueError("Please select a table file")
        if not self.key_file_path.get():
            raise ValueError("Please select a key file")
            
        # Read table
        with open(self.table_file_path.get(), 'r', encoding='ascii') as f:
            table_content = f.read().strip()
        
        # Read key
        with open(self.key_file_path.get(), 'r', encoding='ascii') as f:
            key = f.read().strip()
        
        # Read input
        with open(self.input_file_path.get(), 'r', encoding='ascii') as f:
            message = f.read()
        
        vigenere = VigenereCipher.from_table(key, table_content)
        
        if self.operation_type.get() == "encrypt":
            result = vigenere.encrypt(message)
            self.log(f"🔑 Encrypted {len(message)} characters → {len(result)} characters")
        else:
            result = vigenere.decrypt(message)
            self.log(f"🔑 Decrypted {len(message)} characters → {len(result)} characters")
        
        # Write output
        with open(self.output_file_path.get(), 'w', encoding='ascii') as f:
            f.write(result)


def main():
    root = tk.Tk()
    app = CryptographyApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
