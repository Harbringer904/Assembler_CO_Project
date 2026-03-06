from Registers import REGISTERS 
from Instructions import INSTRUCTIONS
from Utils import imm_to_bin, read_imm, read_immreg

def getReg(name):
    name =name.strip()
    if name not in REGISTERS:
        raise ValueError(f"Unidentified register: '{name}'")
    return REGISTERS[name]

def encode_r(op, opcode, f3, f7):#register type commands
    rd  = getReg(op[0])
    rs1 = getReg(op[1])
    rs2 = getReg(op[2])
    return f7 + rs2 + rs1 + f3 + rd + opcode

def encode_i(neumonic, op, opcode, f3):#immediate commands
    if neumonic == "lw": #loadwith
        rd = getReg(op[0])
        val, rs1_name = read_immreg(op[1])
        rs1 = getReg(rs1_name)

    elif neumonic == "jalr":#jumplink
        rd = getReg(op[0])
        rs1 = getReg(op[1])
        val = read_imm(op[2])

    else:
        rd = getReg(op[0])
        rs1 = getReg(op[1])
        val = read_imm(op[2])

    imm = imm_to_bin(val, 12)
    return imm + rs1 + f3 + rd + opcode

def encode_s(op, opcode, f3):#store command
    rs2 = getReg(op[0])
    val, rs1_name = read_immreg(op[1])
    rs1 = getReg(rs1_name)
    imm = imm_to_bin(val, 12)

    imm_u = imm[0:7]  
    imm_l = imm[7:12] 
    return (imm_u+rs2+rs1 +f3 + imm_l +opcode)

def encode_b(opers, opc, func3, pc, labels):# branch inst
    rs1 = getReg(opers[0])# def r1
    rs2 = getReg(opers[1])

    label_or_imm = opers[2].strip()
    if label_or_imm in labels:#  implimenting offset 
        offsett = labels[label_or_imm] - pc
    else:
        offsett = read_imm(label_or_imm)

    imm = imm_to_bin(offsett, 13)

    b12=imm[0]
    b11=imm[1]
    b10_5=imm[2:8]
    b4_1=imm[8:12]
    return b12 + b10_5 + rs2 + rs1 + func3 + b4_1 + b11 + opc

def encode_u(opers, opc):
    rd = getReg(opers[0])
    imm_no = read_imm(opers[1])
    imm = imm_to_bin(imm_no, 20, unsigned=True)
    return imm + rd + opc

def encode_j(opers, opc, pc, labels):
    rd = getReg(opers[0])

    label_or_imm = opers[1].strip()
    if label_or_imm in labels:
        offsett = labels[label_or_imm] - pc
    else:
        offsett = read_imm(label_or_imm)

    imm = imm_to_bin(offsett, 21)

    b20    = imm[0]
    b19_12 = imm[1:9]
    b11    = imm[9]
    b10_1  = imm[10:20]
    return b20 + b10_1 + b11 + b19_12 + rd + opc

#rgst == 01011
def encode_rst():
    # reset command, custom opc 0001011
    return "00000000000000000000000000001011"

# stop executing code
def encode_halt():
    # stops execution, custom opc 0101011
    return "00000000000000000000000000101011"

# rd and rs1 into bin
def encode_rvrs(opers):
    # Format: 0000000 00000 rs1 000 rd 1111011, custom opc 1111011
    rd  = getReg(opers[0])
    rs1 = getReg(opers[1])

    return "0000000" + "00000" + rs1 + "000" + rd + "1111011"

def encode(neumonic, operands, pc, labels):
     if mnemonic not in INSTRUCTIONS:
        raise ValueError(f"Unidentified instruction: '{mnemonic}'")
    itype,opcode, f3, f7 = INSTRUCTIONS[neumonic]
    
    if itype == "R":
        return encode_r(operands, opcode,f3, f7)
    elif itype == "I":
        return encode_i(neumonic, operands, opcode, f3)
    elif itype == "S":
        return encode_s(operands, opcode,f3)
    elif itype == "B":
        return encode_b(operands, opcode, f3, pc, labels)
    elif itype == "U":
        return encode_u(operands, opcode)
    elif itype == "J":
        return encode_j(operands, opcode, pc, labels)
    elif itype == "RST":
        return encode_rst()
    elif itype == "HALT":
        return encode_halt()
    elif itype == "RVRS":
        return encode_rvrs(operands)
        
    raise ValueError(f"Unhandled instruction type for '{mnemonic}'")
