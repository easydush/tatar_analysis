TATAR_SYMBOLS = 'әӘөӨүҮңҢҗҖһҺ'


def is_tatar_text(text):
    return any(symbol in text for symbol in TATAR_SYMBOLS)
