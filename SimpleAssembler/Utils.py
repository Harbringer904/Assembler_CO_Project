def imm_to_bin(value, bits, unsigned=False): # Convert an integer immediate to a binary string of given bit width, checking range.
    if unsigned== True:
        if(value < 0 or value >= (1 << bits)): #as 2**bits is max value we can get to
            raise ValueError(f"Immediate {value} out of range for {bits}-bit field")
        return format(value, f'0{bits}b') # e.g. format(5, '08b') → '00000101'
    else:
        min_value = -(1 << (bits - 1))
        max_value = (1 << (bits - 1)) - 1
        if value < min_value or value > max_value:
            raise ValueError(f"Immediate {value} out of range for {bits}-bit field")
        if value < 0:
            value = value + (1 << bits) # Convert to two's complement(converting negtive to its 2's complement equavlent) e.g. -1 with 8 bits → 255 (0b11111111)
        return format(value, f'0{bits}b')

def read_imm(a):            #identify decimal,hex(0x),or binary(0b) immediate string to int(decimal).
    a = a.strip()
    if a.startswith("0x") or a.startswith("0X"):
        return int(a, 16) # e.g. int("0x10", 16) → 16 ......... Base 16 to decimal
    elif a.startswith("0b") or a.startswith("0B"):
        return int(a, 2) # e.g. int("0b1010", 2) → 10......... Base 2 to decimal
    else:
        return int(a) # e.g. int("42") → 42 ................ Base 10 to decimal


def read_immreg(token): #Parse 'imm(reg)' format → (imm_int, reg_name)"""   
    token = token.strip()
    imm_part = token[:token.index('(')]
    reg_part = token[token.index('(')+1 : token.index(')')]
    imm = read_imm(imm_part)
    reg = reg_part

    return imm, reg
