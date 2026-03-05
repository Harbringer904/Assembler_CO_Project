from Registers import REGISTERS 
from Instructions import INSTRUCTIONS
from Utils import imm_to_bin, read_imm, read_immreg

def getReg(name):
    name =name.strip()
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
    rs1 = getReg(opers[0])
    rs2 = getReg(opers[1])

    label_or_imm = opers[2].strip()
    if label_or_imm in labels:#  implimenting offset in branching
        offsett = labels[label_or_imm] - pc
    else:
        offsett = read_imm(label_or_imm)

    imm = imm_to_bin(offsett, 13)# converint into 13 bit bin

    b12=imm[0]
    b11=imm[1]
    b10_5=imm[2:8]
    b4_1=imm[8:12]
    return b12 + b10_5 + rs2 + rs1 + func3 + b4_1 + b11 + opc


def encode_u(opers, opc):# Upper imm inst
    rd = getReg(opers[0])
    imm_no = read_imm(opers[1])
    imm = imm_to_bin(imm_no, 20, unsigned=True)# converting into 20 bit bin
    return imm + rd + opc


def encode_j(opers, opc, pc, labels):# jump inst
    rd = getReg(opers[0])

    label_or_imm = opers[1].strip()
    if label_or_imm in labels:
        offsett = labels[label_or_imm] - pc# offset by label adress
    else:
        offsett = read_imm(label_or_imm)# numeric offset

    imm = imm_to_bin(offsett, 21)# converting into 21 bit bin

    b20    = imm[0]
    b19_12 = imm[1:9]
    b11    = imm[9]
    b10_1  = imm[10:20]
    return b20 + b10_1 + b11 + b19_12 + rd + opc


def encode(neumonic, operands, pc, labels):
    itype,opcode, f3, f7 = INSTRUCTIONS[neumonic]
    
    if itype == "R":
        return encode_r(operands, opcode,f3, f7)
    elif itype == "I":
        return encode_i(neumonic, operands, opcode, f3)
    elif itype == "S":
        return encode_s(operands, opcode,f3)
    if itype == "B":
        return encode_b(operands, opcode, f3, pc, labels)
    elif itype == "U":
        return encode_u(operands, opcode)
    elif itype == "J":
        return encode_j(operands, opcode, pc, labels)
