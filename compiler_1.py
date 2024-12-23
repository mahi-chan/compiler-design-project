import re


def remove_comments(file_path):
    with open(file_path, 'r') as file:
        code = file.read()

    single_line_comments = re.findall(r'//.*', code)
    multi_line_comments = re.findall(r'/\*.*?\*/', code, flags=re.DOTALL)

    comments = single_line_comments + multi_line_comments

    code_without_comments = re.sub(r'//.*', '', code)
    code_without_comments = re.sub(r'/\*.*?\*/', '', code_without_comments, flags=re.DOTALL)

    return code, code_without_comments, comments


def extract_variables(code):
    var_pattern = re.compile(r'\b(int|float|double|char)\s+([a-zA-Z_]\w*(?:\s*,\s*[a-zA-Z_]\w*)*)\s*;')
    matches = var_pattern.findall(code)

    variables = []
    for match in matches:
        var_type = match[0]
        var_names = match[1].split(',')
        for name in var_names:
            variables.append((name.strip(), var_type))

    return variables


def extract_numbers(code):
    number_pattern = re.compile(r'\b\d+(\.\d+)?\b')
    numbers = [match.group() for match in number_pattern.finditer(code)]
    return numbers


def extract_symbols(code):
    symbols = "!@#$%^&*()_+-=<>;{}[],"
    found_symbols = re.findall(f"[{re.escape(symbols)}]", code)
    symbol_count = {}

    for symbol in found_symbols:
        if symbol in symbol_count:
            symbol_count[symbol] += 1
        else:
            symbol_count[symbol] = 1

    return symbol_count


def extract_keywords(code):
    keywords = [
        'asm', 'auto', 'break', 'case', 'catch', 'char', 'class', 'const', 'continue', 'default', 'delete', 'do',
        'double', 'else', 'enum', 'extern', 'float', 'for', 'goto', 'if', 'inline', 'int', 'long', 'register', 'return',
        'short', 'signed', 'sizeof', 'static', 'struct', 'switch', 'typedef', 'union', 'unsigned', 'void', 'volatile',
        'while'
    ]

    found_keywords = [kw for kw in keywords if re.search(r'\b' + kw + r'\b', code)]

    return found_keywords


def save_to_files(code_without_comments, comments, keywords, symbols, variables, numbers):

    with open("code.txt", 'w') as file:
        file.write(code_without_comments + "\n")

    with open("comments.txt", 'w') as file:
        for comment in comments:
            file.write(comment + "\n")

    with open("keywords.txt", 'w') as file:
        for keyword in keywords:
            file.write(keyword + "\n")

    with open("symbols.txt", 'w') as file:
        for symbol, count in symbols.items():
            file.write(f"{symbol}: {count}\n")

    with open("variables.txt", 'w') as file:
        for var_name, var_type in variables:
            file.write(f"Variable Name: {var_name}, Type: {var_type}\n")

    with open("numbers.txt", 'w') as file:
        for number in numbers:
            file.write(f"{number}\n")

    print("Files have been saved successfully.")

    print("\nKeywords:")
    for keyword in keywords:
        print(keyword)
    print("\nSymbols:")
    for symbol, count in symbols.items():
        print(f"{symbol}: {count}")
    print("\nVariables:")
    for var_name, var_type in variables:
        print(f"Variable Name: {var_name}, Type: {var_type}")
    print("\nNumbers:")
    for number in numbers:
        print(number)

def find_tokens(code):

    keywords = [
        "asm", "auto", "bool", "break", "case", "catch", "char", "class", "const",
        "const_cast", "continue", "default", "delete", "do", "double", "dynamic_cast",
        "else", "enum", "explicit", "export", "extern", "false", "float", "for",
        "friend", "goto", "if", "inline", "int", "long", "mutable", "namespace",
        "new", "operator", "private", "protected", "public", "register", "reinterpret_cast",
        "return", "short", "signed", "sizeof", "static", "static_cast", "struct",
        "switch", "template", "this", "throw", "true", "try", "typedef", "typeid",
        "typename", "union", "unsigned", "using", "virtual", "void", "volatile",
        "wchar_t", "while", "include"
    ]

    special_characters = ['{', '}', '(', ')', '[', ']', ',', ';']
    arithmatic_operators = ['+', '-', '*', '/', '%', '++', '--']
    re_operators = ['==', '!=', '<', '>', '<=', '>=']
    assign_operators = ['=', '+=', '-=', '*=', '/=', '%=']
    log_operators = ['&&', '||', '!']
    bit_operators = ['&', '|', '^', '~', '<<', '>>']

    special_symbols_attribute = {
        '{': "Opening Curly Braces",
        '}': "Closing Curly Braces",
        '(': "Opening Parenthesis",
        ')': "Closing Parenthesis",
        '[': "Opening Square Bracket",
        ']': "Closing Square Bracket",
        ',': "Comma",
        ';': "Semicolon"
    }

    arithmatic_operators_attribute = {
        '+': "Addition",
        '-': "Subtraction",
        '*': "Multiplication",
        '/': "Division",
        '%': "Modulo",
        '++': "Increment",
        '--': "Decrement"
    }

    re_operators_attribute = {
        '==': "Equal to",
        '!=': "Not equal to",
        '<': "Less than",
        '>': "Greater than",
        '<=': "Less than or equal to",
        '>=': "Greater than or equal to"
    }

    assign_operators_attribute = {
        '=': "Simple assignment",
        '+=': "Add AND assignment",
        '-=': "Subtract AND assignment",
        '*=': "Multiply AND assignment",
        '/=': "Divide AND assignment",
        '%=': "Modulo AND assignment"
    }

    log_operators_attribute = {
        '&&': "Logical AND",
        '||': "Logical OR",
        '!': "Logical NOT"
    }

    bit_operators_attribute = {
        '&': "Bitwise AND",
        '|': "Bitwise OR",
        '^': "Bitwise exclusive OR",
        '~': "Bitwise complement",
        '<<': "Shift left",
        '>>': "Shift right"
    }

    tokens = []
    token_pattern = re.compile(r'\b\w+\b|[{}]|\S+')
    for match in token_pattern.finditer(code):
        token = match.group()
        if token.lower() in keywords:
            tokens.append((token, "Keyword", '--'))
        elif token in special_characters:
            tokens.append((token, "Special Symbol", special_symbols_attribute[token]))
        elif token in arithmatic_operators:
            tokens.append((token, "Arithmetic Operator", arithmatic_operators_attribute[token]))
        elif token in re_operators:
            tokens.append((token, "Relational Operator", re_operators_attribute[token]))
        elif token in assign_operators:
            tokens.append((token, "Assignment Operator", assign_operators_attribute[token]))
        elif token in log_operators:
            tokens.append((token, "Logical Operator", log_operators_attribute[token]))
        elif token in bit_operators:
            tokens.append((token, "Bitwise Operator", bit_operators_attribute[token]))
        elif re.match(r'^[0-9]+$', token):
            tokens.append((token, "Number", "Constant"))
        else:
            tokens.append((token, "Identifier", "Pointer to Symbol Table Entry"))

    return tokens


def symbol_table(variables):
    symbol_table = []
    pointer_counter = 0

    for var_name, var_type in variables:
        symbol_table.append((var_name, "id", var_type, pointer_counter))
        pointer_counter += 1

    return symbol_table


def print_tokens():

    with open("code.txt", 'r') as file:
        code_lines = file.read()
    code = code_lines

    tokens = find_tokens(code)

    print("=" * 80)
    print("|\tLexeme".ljust(20) + "|\tToken Name".ljust(25) + "|\tAttribute".ljust(30) + "|")
    print("=" * 80)

    for lexeme, token_name, attribute in tokens:
        print(f"|\t{lexeme.ljust(15)}|\t{token_name.ljust(20)}|\t{attribute.ljust(30)}|")
        print("-" * 80)


def print_symbol(symbol_table):
    print("=" * 80)
    print("|\tSymbol".ljust(20) + "|\tToken".ljust(25) + "|\tData Type".ljust(30) + "|\tPointer to Symbol Table Entry".ljust(40) + "|")
    print("=" * 80)

    for symbol, token, data_type, pointer in symbol_table:
        print(f"|\t{symbol.ljust(15)}|\t{token.ljust(20)}|\t{data_type.ljust(30)}|\t\t{str(pointer).ljust(40)}|")
        print("-" * 80)


if __name__ == "__main__":
    file_path = 'example.txt'
    original_code, code_without_comments, comments = remove_comments(file_path)
    keywords = extract_keywords(original_code)
    symbols = extract_symbols(original_code)
    variables = extract_variables(original_code)
    numbers = extract_numbers(original_code)

    save_to_files(code_without_comments, comments, keywords, symbols, variables, numbers)

    print_tokens()

    symbol_table = symbol_table(variables)
    print_symbol(symbol_table)