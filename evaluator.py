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

# ============================================================
# RECURSIVE DESCENT PARSER
# ============================================================


# ------------------------------------------------------------
# EXPRESSION LEVEL
# Handles + and -
# ------------------------------------------------------------

def parse_expression(tokens, position):

    left, position = parse_term(tokens, position)

    while (
        tokens[position][0] == "OP"
        and tokens[position][1] in "+-"
    ):

        operator = tokens[position][1]

        position += 1

        right, position = parse_term(tokens, position)

        left = (
            "binary",
            operator,
            left,
            right
        )

    return left, position


# ------------------------------------------------------------
# TERM LEVEL
# Handles *, /, %, and implicit multiplication
# ------------------------------------------------------------

def parse_term(tokens, position):

    left, position = parse_unary(tokens, position)

    while True:

        # Normal multiplication, division, or modulus
        if (
            tokens[position][0] == "OP"
            and tokens[position][1] in "*/%"
        ):

            operator = tokens[position][1]

            position += 1

            right, position = parse_unary(
                tokens,
                position
            )

            left = (
                "binary",
                operator,
                left,
                right
            )


        # Implicit multiplication
        # Example: 2(3 + 4)
        elif tokens[position][0] == "LPAREN":

            right, position = parse_unary(
                tokens,
                position
            )

            left = (
                "binary",
                "*",
                left,
                right
            )


        # Implicit multiplication
        # Example: (2 + 3)4
        elif (
            tokens[position][0] == "NUM"
            and position > 0
            and tokens[position - 1][0] == "RPAREN"
        ):

            right, position = parse_unary(
                tokens,
                position
            )

            left = (
                "binary",
                "*",
                left,
                right
            )


        else:

            break

    return left, position


# ------------------------------------------------------------
# UNARY LEVEL
# Handles unary -
# ------------------------------------------------------------

def parse_unary(tokens, position):

    # Unary negative
    if (
        tokens[position][0] == "OP"
        and tokens[position][1] == "-"
    ):

        position += 1

        operand, position = parse_unary(
            tokens,
            position
        )

        return (
            "neg",
            operand
        ), position


    # Unary + is not supported
    elif (
        tokens[position][0] == "OP"
        and tokens[position][1] == "+"
    ):

        raise ValueError


    return parse_power(tokens, position)


# ------------------------------------------------------------
# POWER LEVEL
# Handles ^
# ------------------------------------------------------------

def parse_power(tokens, position):

    left, position = parse_primary(
        tokens,
        position
    )

    # Exponentiation is right associative
    if (
        tokens[position][0] == "OP"
        and tokens[position][1] == "^"
    ):

        position += 1

        right, position = parse_unary(
            tokens,
            position
        )

        left = (
            "binary",
            "^",
            left,
            right
        )

    return left, position


# ------------------------------------------------------------
# PRIMARY LEVEL
# Handles numbers and parentheses
# ------------------------------------------------------------

def parse_primary(tokens, position):

    token_type = tokens[position][0]
    token_value = tokens[position][1]


    # Number
    if token_type == "NUM":

        position += 1

        return (
            "number",
            token_value
        ), position


    # Parenthesised expression
    elif token_type == "LPAREN":

        position += 1

        node, position = parse_expression(
            tokens,
            position
        )

        # Must have closing parenthesis
        if tokens[position][0] != "RPAREN":

            raise ValueError

        position += 1

        return node, position


    else:

        raise ValueError


# ------------------------------------------------------------
# PARSE COMPLETE TOKEN LIST
# ------------------------------------------------------------

def parse_tokens(tokens):

    tree, position = parse_expression(
        tokens,
        0
    )

    # A valid expression must end at END
    if tokens[position][0] != "END":

        raise ValueError

    return tree


# ============================================================
# TREE FORMATTING
# ============================================================

def format_number(number_text):

    number = float(number_text)

    if number.is_integer():
        return str(int(number))

    return str(number)


def tree_to_string(tree):

    node_type = tree[0]

    if node_type == "number":

        return format_number(tree[1])


    elif node_type == "neg":

        operand = tree_to_string(tree[1])

        return "(neg " + operand + ")"


    elif node_type == "binary":

        operator = tree[1]

        left = tree_to_string(tree[2])
        right = tree_to_string(tree[3])

        return (
            "("
            + operator
            + " "
            + left
            + " "
            + right
            + ")"
        )


# ============================================================
# EXPRESSION EVALUATION
# ============================================================

def evaluate_tree(tree):

    node_type = tree[0]


    # Number
    if node_type == "number":

        return float(tree[1])


    # Unary negative
    elif node_type == "neg":

        value = evaluate_tree(tree[1])

        return -value


    # Binary operation
    elif node_type == "binary":

        operator = tree[1]

        left = evaluate_tree(tree[2])
        right = evaluate_tree(tree[3])


        if operator == "+":

            return left + right


        elif operator == "-":

            return left - right


        elif operator == "*":

            return left * right


        elif operator == "/":

            if right == 0:
                raise ZeroDivisionError

            return left / right


        elif operator == "%":

            if right == 0:
                raise ZeroDivisionError

            return left % right


        elif operator == "^":

            value = left ** right

            if isinstance(value, complex):
                raise ValueError

            return value


    raise ValueError


# ============================================================
# EVALUATE ONE EXPRESSION
# ============================================================

def evaluate_expression(expression):

    tokens = tokenize(expression)


    # Tokenisation error
    if tokens is None:

        return {
            "input": expression,
            "tree": "ERROR",
            "tokens": "ERROR",
            "result": "ERROR"
        }


    token_text = tokens_to_string(tokens)


    # Parsing
    try:

        tree = parse_tokens(tokens)

        tree_text = tree_to_string(tree)


    except (ValueError, IndexError):

        return {
            "input": expression,
            "tree": "ERROR",
            "tokens": token_text,
            "result": "ERROR"
        }


    # Evaluation
    try:

        result = evaluate_tree(tree)

        result = float(result)


        if (
            result != result
            or result == float("inf")
            or result == float("-inf")
        ):

            raise ValueError


    except (
        ValueError,
        ZeroDivisionError,
        OverflowError
    ):

        result = "ERROR"


    return {
        "input": expression,
        "tree": tree_text,
        "tokens": token_text,
        "result": result
    }
