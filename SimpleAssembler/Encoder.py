from Registers import REGISTERS #importing all required files/funtions
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
        rd  = getReg(op[0])
        rs1 = getReg(op[1])
        val = read_imm(op[2])

    else:

        rd  = getReg(op[0])
        rs1 = getReg(op[1])
        val = read_imm(op[2])

    imm = imm_to_bin(val, 12)
    return imm + rs1 + f3 + rd + opcode


def encode_s(op, opcode, f3):#store command
    rs2 = getReg(op[0])
    val, rs1_name = read_immreg(op[1])
    rs1 = getReg(rs1_name)
    imm = imm_to_bin(val, 12)

    imm_upper = imm[0:7]  
    imm_lower = imm[7:12] 
    return (imm_upper+rs2+rs1 +f3 + imm_lower +opcode)


def encode(neumonic, operands, pc, labels):
    itype,opcode, f3, f7 = INSTRUCTIONS[neumonic]
    
    if itype == "R":
        return encode_r(operands, opcode,f3, f7)
    elif itype == "I":
        return encode_i(neumonic, operands, opcode, f3)
    elif itype == "S":
        return encode_s(operands, opcode,f3)

