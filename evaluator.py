# ============================================================
# HIT137 - GROUP ASSESSMENT 2
# QUESTION 2 - EXPRESSION EVALUATOR
# ============================================================

# Group Members:
# Aavash Khatiwada - S405266
# Dipak Karki - S407785
# Abid Kirpor - S399375


# ------------------------------------------------------------
# TOKENISER
# ------------------------------------------------------------

def tokenize(expression):

    tokens = []

    i = 0

    while i < len(expression):

        char = expression[i]


        # Ignore whitespace
        if char.isspace():

            i += 1


        # Number
        elif char.isdigit():

            number = ""

            while i < len(expression) and expression[i].isdigit():

                number += expression[i]

                i += 1


            # Check for decimal point
            if i < len(expression) and expression[i] == ".":

                number += "."

                i += 1


                # There must be at least one digit
                # after the decimal point
                if i >= len(expression) or not expression[i].isdigit():

                    return None


                while i < len(expression) and expression[i].isdigit():

                    number += expression[i]

                    i += 1


            tokens.append(("NUM", number))


        # Operators
        elif char in "+-*/%^":

            tokens.append(("OP", char))

            i += 1


        # Left parenthesis
        elif char == "(":

            tokens.append(("LPAREN", char))

            i += 1


        # Right parenthesis
        elif char == ")":

            tokens.append(("RPAREN", char))

            i += 1


        # Invalid character
        else:

            return None


    # End token
    tokens.append(("END", ""))

    return tokens


# ------------------------------------------------------------
# TOKEN FORMATTING
# ------------------------------------------------------------

def tokens_to_string(tokens):

    token_text = ""


    for token_type, token_value in tokens:


        if token_type == "END":

            if token_text != "":

                token_text += " "

            token_text += "[END]"


        else:

            if token_text != "":

                token_text += " "


            token_text += (
                "["
                + token_type
                + ":"
                + token_value
                + "]"
            )


    return token_text
