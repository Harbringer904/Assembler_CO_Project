import sys
import os
from FINAL_PROJECT.SimpleSimulator.memory import read_mem, write_mem, is_valid_addr

def unsigned32(val):
    return val & 0xFFFFFFFF

def signed32(val):
    if val & 0x80000000:
        return val - 0x100000000
    return val

def sign_extend(val, bits):
    sign_bit = 1 << (bits - 1)
    return (val & (sign_bit - 1)) - (val & sign_bit)

def safe_write_trace(trace_lines, out_file):
    if not out_file:
        return
    try:
        os.makedirs(os.path.dirname(out_file) or '.', exist_ok=True)
        with open(out_file, 'w') as f:
            for line in trace_lines:
                f.write(line + "\n")
    except (OSError, IOError):
        pass

def run_r_type(inst_bin, regs):
    if len(inst_bin) != 32:
        raise ValueError("Invalid instruction")
    rd = int(inst_bin[20:25], 2)
    rs1 = int(inst_bin[12:17], 2)
    rs2 = int(inst_bin[7:12], 2)
    funct3 = inst_bin[17:20]
    funct7 = inst_bin[0:7]
    
    if not all(c in '01' for c in inst_bin):
        raise ValueError("Invalid instruction bits")
    if rd < 0 or rd > 31 or rs1 < 0 or rs1 > 31 or rs2 < 0 or rs2 > 31:
        raise ValueError("Invalid register")
    
    val1 = signed32(regs[rs1])
    val2 = signed32(regs[rs2])
    result = 0
    
    if funct3=="000" and funct7=="0000000":
        result = val1+ val2

    elif funct3 =="000" and funct7 == "0100000":
        result = val1 -val2

    elif funct3 =="001" and funct7== "0000000":
        result = signed32(unsigned32(val1)<<(val2 & 0x1F))

    elif funct3 =="010" and funct7=="0000000":
        if val1 < val2:
            result=1
        else:
            result=0
    elif funct3=="011" and funct7 =="0000000":
        if unsigned32(val1) < unsigned32(val2):
            result=1
        else:
            result=0

    elif funct3 =="100" and funct7 =="0000000":
        result = val1^ val2

    elif funct3 == "101" and funct7 == "0000000":
        result = unsigned32(val1) >> (val2 & 0x1F)

    elif funct3 =="110" and funct7 =="0000000":
        result = val1 | val2

    elif funct3 =="111" and funct7 =="0000000":
        result = val1 & val2

    elif funct3 =="000" and funct7 =="0000001":
        result = val1 *val2
    else:
        raise ValueError(f"Unsupported R-type funct3/funct7: {funct3}/{funct7}")
    
    if rd !=0:
        regs[rd] = unsigned32(result)

def run_i_type_alu(inst_bin, regs):
    if len(inst_bin) != 32:
        raise ValueError("Invalid instruction")
    rd = int(inst_bin[20:25], 2)
    rs1 = int(inst_bin[12:17], 2)
    funct3 = inst_bin[17:20]
    imm = sign_extend(int(inst_bin[0:12], 2), 12)
    
    if not all(c in '01' for c in inst_bin):
        raise ValueError("Invalid instruction bits")
    if rd < 0 or rd > 31 or rs1 < 0 or rs1 > 31:
        raise ValueError("Invalid register")
    
    val1 = signed32(regs[rs1])
    result = 0
    if funct3 == "000":
        result = val1 + imm
    elif funct3 == "011":
        result = 1 if unsigned32(val1) < unsigned32(signed32(imm)) else 0
    else:
        raise ValueError(f"Unsupported I-type funct3: {funct3}")
    
    if rd != 0:
        regs[rd] = unsigned32(result)

def run_load_word(inst_bin, regs, memory, pc, trace_lines, out_file):
    if len(inst_bin) != 32:
        raise ValueError("Invalid instruction")
    rd = int(inst_bin[20:25], 2)
    rs1 = int(inst_bin[12:17], 2)
    funct3 = inst_bin[17:20]
    imm = sign_extend(int(inst_bin[0:12], 2), 12)
    
    if not all(c in '01' for c in inst_bin):
        raise ValueError("Invalid instruction bits")
    if rd < 0 or rd >31 or rs1< 0 or rs1> 31:
        raise ValueError("Invalid register")
    
    if funct3 !="010":
        print(f"Error: Unknown funct3 '{funct3}' for load at PC 0x{pc:08x}", file=sys.stderr)
        sys.exit(1)
    
    address =signed32(regs[rs1]) + imm
    if not is_valid_addr(address):
        safe_write_trace(trace_lines, out_file)
        print(f"Error: Invalid memory access at 0x{address:08x}", file=sys.stderr)
        sys.exit(1)
    
    try:
        value =read_mem(memory, address)
        if rd != 0:
            regs[rd] = value
    except (ValueError, IndexError) as e:
        safe_write_trace(trace_lines, out_file)
        print(f"Error: Memory read failed: {e}", file=sys.stderr)
        sys.exit(1)

def run_store_word(inst_bin, regs, memory, pc, trace_lines, out_file):
    if len(inst_bin) != 32:
        raise ValueError("Invalid instruction")
    funct3 =inst_bin[17:20]
    rs1 =int(inst_bin[12:17], 2)
    rs2 =int(inst_bin[7:12], 2)
    imm_str =inst_bin[0:7] + inst_bin[20:25]
    imm =sign_extend(int(imm_str, 2), 12)

    if not all(c in '01' for c in inst_bin):
        raise ValueError("Invalid instruction bits")

    if funct3 != "010":
        print(f"Error: Unknown funct3 '{funct3}' for store opcode at PC 0x{pc:08x}", file=sys.stderr)
        sys.exit(1)
    
    if rs1 <0 or rs1> 31 or rs2< 0 or rs2> 31:
        raise ValueError("Invalid register")
    
    address = signed32(regs[rs1]) + imm
    if not is_valid_addr(address):
        safe_write_trace(trace_lines, out_file)
        print(f"Error: Invalid memory access at 0x{address:08x}", file=sys.stderr)
        sys.exit(1)
    
    try:
        write_mem(memory, address, regs[rs2])
    except (ValueError, IndexError) as e:
        safe_write_trace(trace_lines, out_file)
        print(f"Error: Memory write failed: {e}", file=sys.stderr)
        sys.exit(1)
