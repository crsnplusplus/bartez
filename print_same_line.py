import numpy as np

def print_grid(rows, cols, data):
    assert(rows * cols == len(data))
    print('show')

    for r in range(0, rows):
        for c in range(0, cols):
            pos = r * cols + c
            char = data[pos]
            print(char, end=' '),
        print('')
    print('')

rows, cols = 3, 4
blocks_count, char_count = rows, rows * cols - rows
data = np.array(['_'] * char_count + ['#'] * blocks_count)
np.random.shuffle(data)
print(data)
