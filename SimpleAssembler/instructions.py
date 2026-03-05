# Format: name → (type, opcode, funct3, funct7)
# funct3/funct7 = None if not applicable

INSTRUCTIONS = {
    # R-type
    "add":  ("R", "0110011", "000", "0000000"),
    "sub":  ("R", "0110011", "000", "0100000"),
    "sll":  ("R", "0110011", "001", "0000000"),
    "slt":  ("R", "0110011", "010", "0000000"),
    "sltu": ("R", "0110011", "011", "0000000"),
    "xor":  ("R", "0110011", "100", "0000000"),
    "srl":  ("R", "0110011", "101", "0000000"),
    "or":   ("R", "0110011", "110", "0000000"),
    "and":  ("R", "0110011", "111", "0000000"),
    "mul":  ("R", "0110011", "000", "0000001"),

    # I-type
    "addi": ("I", "0010011", "000", None),
    "sltiu":("I", "0010011", "011", None),
    "lw":   ("I", "0000011", "010", None),
    "jalr": ("I", "1100111", "000", None),

    # S-type
    "sw":   ("S", "0100011", "010", None),

    # B-type
    "beq":  ("B", "1100011", "000", None),
    "bne":  ("B", "1100011", "001", None),
    "blt":  ("B", "1100011", "100", None),
    "bge":  ("B", "1100011", "101", None),
    "bltu": ("B", "1100011", "110", None),
    "bgeu": ("B", "1100011", "111", None),

    # U-type
    "lui":  ("U", "0110111", None, None),
    "auipc":("U", "0010111", None, None),

    # J-type
    "jal":  ("J", "1101111", None, None),

    #Bonus Type
    "rst":  ("RST", None, None, None),
    "halt": ("HALT", None, None, None),
    "rvrs": ("RVRS", None, None, None),
}
