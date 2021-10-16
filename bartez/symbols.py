from collections import namedtuple

# SquareValue.block = ? = 'A' - 2
# SquareValue.char = @ = 'A' - 1
SquareValuesTuple = namedtuple('SquareValue', ['block', 'char'])
SquareValues = SquareValuesTuple(chr(ord('A') - 2), chr(ord('A') - 1) )

# chr(ord(Symbols.FIRST)) == ?
# chr(ord(Symbols.LAST)) == Z
# this way symbol_to_base0 is trivial because it's obtained
# with an offset
SymbolsTuple = namedtuple('Symbols', ['FIRST', 'LAST', 'extra_symbols_count'])
Symbols = SymbolsTuple(SquareValues.block, 'Z', 2)


def get_alphabet_base0():
    return list(map(chr, range(ord(Symbols.FIRST), ord(Symbols.LAST))))


def get_symbols_count():
    return len(get_alphabet_base0())


def symbol_to_base0(symbol):
    return ord(symbol) - ord(Symbols.FIRST)


def base0_to_symbol(base0):
    alphabet_base0 = get_alphabet_base0()
    return alphabet_base0[base0]


def symbols_to_base0(symbols):
    return list(map(symbol_to_base0, symbols))


def base0_to_symbols(base0):
    return list(map(base0_to_symbol, base0))
