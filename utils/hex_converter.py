def convert(base, number):
    hex_number = hex(int(f'{base}', base=16) + number)[2:]
    return hex_number