# ============================================================
# HIT137 - GROUP 13 - ASSESSMENT 2
# QUESTION 1 - FILE CIPHER
# ============================================================

# Group Members:
# Aavash Khatiwada - S405266
# Dipak Karki - S407785
# Abiud Kiprop - S399375


# ------------------------------------------------------------
# FUNCTION TO SHIFT A CHARACTER WITHIN A GIVEN RANGE
# ------------------------------------------------------------

def shift_character(char, start_char, end_char, shift):

    start = ord(start_char)
    end = ord(end_char)

    range_size = end - start + 1

    position = ord(char) - start

    new_position = (position + shift) % range_size

    new_char = chr(start + new_position)

    return new_char


# ------------------------------------------------------------
# ENCRYPT FILE
# ------------------------------------------------------------

def encrypt_file(shift1: int, shift2: int,
                 input_path: str, output_path: str) -> None:

    with open(input_path, "r", encoding="utf-8") as file:
        text = file.read()

    encrypted_text = ""

    for char in text:

        # Lowercase letters a-n
        if char >= "a" and char <= "n":

            shift = shift1 * shift2

            encrypted_char = shift_character(
                char, "a", "n", shift
            )

            encrypted_text += encrypted_char


        # Lowercase letters o-z
        elif char >= "o" and char <= "z":

            shift = -(shift1 + shift2)

            encrypted_char = shift_character(
                char, "o", "z", shift
            )

            encrypted_text += encrypted_char


        # Uppercase letters A-M
        elif char >= "A" and char <= "M":

            shift = -shift1

            encrypted_char = shift_character(
                char, "A", "M", shift
            )

            encrypted_text += encrypted_char


        # Uppercase letters N-Z
        elif char >= "N" and char <= "Z":

            shift = shift2 * shift2

            encrypted_char = shift_character(
                char, "N", "Z", shift
            )

            encrypted_text += encrypted_char


        # Digits 0-9
        elif char >= "0" and char <= "9":

            shift = shift1 - shift2

            encrypted_char = shift_character(
                char, "0", "9", shift
            )

            encrypted_text += encrypted_char


        # Spaces, punctuation and other characters
        else:

            encrypted_text += char


    with open(output_path, "w", encoding="utf-8") as file:
        file.write(encrypted_text)

# ------------------------------------------------------------
# DECRYPT FILE
# ------------------------------------------------------------

def decrypt_file(shift1: int, shift2: int,
                 input_path: str, output_path: str) -> None:

    with open(input_path, "r", encoding="utf-8") as file:
        text = file.read()

    decrypted_text = ""

    for char in text:

        # Lowercase letters a-n
        if char >= "a" and char <= "n":

            shift = -(shift1 * shift2)

            decrypted_char = shift_character(
                char, "a", "n", shift
            )

            decrypted_text += decrypted_char


        # Lowercase letters o-z
        elif char >= "o" and char <= "z":

            shift = shift1 + shift2

            decrypted_char = shift_character(
                char, "o", "z", shift
            )

            decrypted_text += decrypted_char


        # Uppercase letters A-M
        elif char >= "A" and char <= "M":

            shift = shift1

            decrypted_char = shift_character(
                char, "A", "M", shift
            )

            decrypted_text += decrypted_char


        # Uppercase letters N-Z
        elif char >= "N" and char <= "Z":

            shift = -(shift2 * shift2)

            decrypted_char = shift_character(
                char, "N", "Z", shift
            )

            decrypted_text += decrypted_char


        # Digits 0-9
        elif char >= "0" and char <= "9":

            shift = -(shift1 - shift2)

            decrypted_char = shift_character(
                char, "0", "9", shift
            )

            decrypted_text += decrypted_char


        # Spaces, punctuation and other characters
        else:

            decrypted_text += char


    with open(output_path, "w", encoding="utf-8") as file:
        file.write(decrypted_text)     


# ------------------------------------------------------------
# VERIFY DECRYPTED FILE
# ------------------------------------------------------------

def verify_files(original_path: str,
                 decrypted_path: str) -> bool:

    with open(original_path, "r", encoding="utf-8") as file:
        original_text = file.read()

    with open(decrypted_path, "r", encoding="utf-8") as file:
        decrypted_text = file.read()

    return original_text == decrypted_text
