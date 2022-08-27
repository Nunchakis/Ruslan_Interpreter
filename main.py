import array as arr

INTEGER, PLUS, MINUS, WHITESPACE, EOF = 'INTEGER', 'PLUS', 'MINUS', 'WHITESPACE', 'EOF'


class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({token} , {value})'.format(
            type=self.value,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


class Interpreter(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None

    def error(self):
        raise Exception('Error parsing input')

    def get_next_token(self):
        text = self.text
        if self.pos > len(text) - 1:
            return Token(EOF, None)

        current_char = text[self.pos]

        while current_char.isspace():
            self.pos += 1
            current_char = text[self.pos]

        if current_char.isdigit():
            number = self.takeNumber(text, current_char, 0)
            token = Token(INTEGER, number)
            return token

        if current_char == '+':
            token = Token(PLUS, current_char)
            self.pos += 1
            return token

        if current_char == '-':
            token = Token(MINUS, current_char)
            self.pos += 1
            return token

        self.error()

    def eat(self, token_type):
        if self.current_token.type in token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        self.current_token = self.get_next_token()
        left = self.current_token
        self.eat([INTEGER])

        op = self.current_token
        self.eat([PLUS, MINUS])

        right = self.current_token
        self.eat([INTEGER])

        if op.value == '+':
            result = left.value + right.value
        else:
            result = left.value - right.value
        return result

    def takeNumber(self, text, current_chart, result_number):
        result_number = result_number*10 + int(current_chart)
        self.pos += 1
        if self.pos < len(text) and text[self.pos].isdigit():
            current_chart = text[self.pos]
            result_number = self.takeNumber(text, current_chart, result_number)
        return result_number


def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
