# The Vigenère cipher
# Code by Md. Al-Amin

import string
import sys 

# 95 characters in total
PRINTABLE_CHARS = string.ascii_letters + string.digits + string.punctuation + ' '
CHAR_COUNT = len(PRINTABLE_CHARS)

def sanitize_key(key):
    return "".join(filter(str.isalpha, key))

def extended_vigenere_cipher(text, key, mode='encrypt'):
    """
    Encrypts or decrypts ALL 95 printable characters using a Vigenère-style shift.
    """
    result = ""
    sanitized_key = sanitize_key(key)
    if not sanitized_key:
        raise ValueError("The key must contain at least one letter.")
        
    key_index = 0
    key_length = len(sanitized_key)
    # Determine shift direction: +1 for encrypt, -1 for decrypt
    shift_multiplier = -1 if mode == 'decrypt' else 1

    for char in text:
        try:
            # 1. Get the position of the current character
            char_pos = PRINTABLE_CHARS.index(char)
        except ValueError:
            # If the character is not in our alphabet (e.g., a newline), keep it as is
            result += char
            continue

        # 2. Get the key character and its shift value
        key_char = sanitized_key[key_index % key_length]
        
        # Determine the shift value (A/a=0, B/b=1, etc.)
        shift_base = ord('A') if key_char.isupper() else ord('a')
            
        key_shift_value = (ord(key_char) - shift_base) * shift_multiplier

        # 3. Apply the shift modulo the size of our custom alphabet (95)
        # The CHAR_COUNT ensures the result wraps correctly for decryption too
        new_pos = (char_pos + key_shift_value) % CHAR_COUNT
        
        # 4. Get the new character
        result += PRINTABLE_CHARS[new_pos]
        key_index += 1

    return result

def get_valid_key():
    """Prompts the user for a key and validates that it contains at least two different letters."""
    while True:
        user_key = input("Enter the secret key (must contain at least two different letters, case-sensitive): ").strip()
        
        # 1. Check if it contains any letters first
        letters_only_key = sanitize_key(user_key)
        
        if not letters_only_key:
            print("\n ! Invalid key. The key must contain at least one letter.")
            continue
            
        # 2. Check for at least two DIFFERENT letters (case-sensitive)
        unique_letters = set(letters_only_key)
        
        if len(unique_letters) >= 2:
            return user_key
        else:
            print("\n ! Invalid key. The key must contain at least two *different* letters (e.g., 'ab' or 'aBc', but not 'aaa').")

def get_multiline_input(prompt):
    """Handles multi-line text input until the user presses Enter twice."""
    print(prompt)
    print(" (Press Enter twice to finish input):")
    
    lines = []
    # Loop to capture input line by line
    while True:
        try:
            line = input()
        except EOFError:
            # Handle Ctrl+D (EOF) if used
            break
            
        if line == "":
            break # Exit loop on double enter (empty line)
            
        lines.append(line)
        
    # Join lines with a single space to preserve separation without newlines
    return " ".join(lines).strip()

# ----------------------------------------------------------------------

def main():
        # ASCII Art/Banner Text for "Cipher Shell"
    print("=" * 60)
    print(r"   _____ _       _                   _____ _          _ _ ")
    print(r"  / ____(_)     | |                 / ____| |        | | |")
    print(r" | |     _ _ __ | |__   ___ _ __   | (___ | |__   ___| | |")
    print(r" | |    | | '_ \| '_ \ / _ \ '__|   \___ \| '_ \ / _ \ | |")
    print(r" | |____| | |_) | | | |  __/ |      ____) | | | |  __/ | |")
    print(r"  \_____|_| .__/|_| |_|\___|_|     |_____/|_| |_|\___|_|_|")
    print(r"          | |                                                     ")
    print(r"          |_|                                                     ")
    print("=" * 60)
    print("     --- Cipher Shell - Extended Cipher Tool ---")
    print("            --- Code by Md. Al-Amin ---")
    print("=" * 60)
    print("Commands: (E)ncrypt, (D)ecrypt, or (exit)")

    while True:
        # Prompt for command (E, D, or exit)
        command = input("\n[Cipher-Shell] > ").strip().lower()

        if command == 'exit':
            print("--Terminating application. Goodbye!")
            sys.exit(0) 
        
        elif command in ['e', 'd']:
            mode = 'encrypt' if command == 'e' else 'decrypt'
        else:
            print("! Invalid command. Please enter 'E', 'D', or 'exit'.")
            continue
            
        # --- Start of the Encryption/Decryption Logic ---
        print(f"\n--- Mode Selected: {mode.upper()} ---")

        # 1. Get the Key FIRST
        user_key = get_valid_key()
        sanitized_key_used = sanitize_key(user_key)
        print(f"Key will be sanitized to: '{sanitized_key_used}' (CASE IS IMPORTANT!)")
        
        # 2. Get the input text/ciphertext (using fixed bug-free handler)
        prompt = ("Please paste the text or paragraph you wish to encrypt below:") if mode == 'encrypt' else (
                 "Please paste the ciphertext or paragraph you wish to decrypt below:")
                 
        user_text = get_multiline_input(prompt)
        
        if not user_text:
            print("\nOperation cancelled: No text was provided.")
            continue 

        # 3. Perform the operation
        try:
            processed_text = extended_vigenere_cipher(user_text, user_key, mode)
        except ValueError as e:
            print(f"\nError: {e}")
            continue 
        
        # 4. Display the result
        print("\n" + "="*60)
        print(f"       {mode.upper()}ION SUCCESSFUL")
        print("="*60)
        
        # Display results clearly
        if mode == 'encrypt':
            print(f"Original Text (Snippet):   {user_text[:50]}{'...' if len(user_text) > 50 else ''}")
            print(f"Key Used (Case-Sensitive): {sanitized_key_used}")
            print("-" * 60)
            print(f"Ciphertext (Encrypted):\n{processed_text}")
        else:
            print(f"Ciphertext (Snippet):      {user_text[:50]}{'...' if len(user_text) > 50 else ''}")
            print(f"Key Used (Case-Sensitive): {sanitized_key_used}")
            print("-" * 60)
            print(f"Plaintext (Decrypted):\n{processed_text}")
            
        print("="*60)
        # --- End of Logic ---

if __name__ == "__main__":
    main()
