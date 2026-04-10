import os
import sys

MEM_SIZE= 32
DATA_MEM_START= 0x00010000

def int_to_bin32(val):
    return f"0b{val:032b}"

def load_instructions(filename):
    if not os.path.exists(filename):
        print(f"Error: File not found: {filename}", file=sys.stderr)
        sys.exit(1)
    
    instructions=[]
    try:
        with open(filename, 'r') as f:
            for i, line in enumerate(f, 1):
                line =line.strip()
                if not line or line.startswith('#'):
                    continue
                if len(line)!=32 or not all(c in '01' for c in line):
                    print(f"Error: Invalid instruction at line {i}: {line}", file=sys.stderr)
                    sys.exit(1)
                instructions.append(line)
        if not instructions:
            print("Error: No instructions found", file=sys.stderr)
            sys.exit(1)
        return instructions
    except IOError as e:
        print(f"Error: Cannot read file: {e}", file=sys.stderr)
        sys.exit(1)

def read_mem(mem, addr):
    if not isinstance(mem, list):
        raise TypeError("Memory must be a list")
    if not isinstance(addr, int):
        raise TypeError("Address must be an integer")
    if addr%4 !=0 or addr<0:
        raise ValueError(f"Invalid address: 0x{addr:08x}")
    idx = addr//4
    if idx >= len(mem):
        raise IndexError(f"Address out of bounds: 0x{addr:08x}")
    return mem[idx]

def write_mem(mem, addr, value):
    if not isinstance(mem, list):
        raise TypeError("Memory must be a list")
    if not isinstance(addr, int):
        raise TypeError("Address must be an integer")
    if not isinstance(value, int):
        raise TypeError("Memory value must be an integer")
    if addr%4 != 0 or addr<0:
        raise ValueError(f"Invalid address: 0x{addr:08x}")
    idx =addr//4
    if idx>=len(mem):
        raise IndexError(f"Address out of bounds: 0x{addr:08x}")
    mem[idx] =value & 0xFFFFFFFF

def is_valid_addr(addr):
    if addr % 4!=0:
        return False
    return (0x0<=addr<=0xFF) or (0x100<=addr<=0x17F) or (0x10000<=addr<=0x1007F)

def save_output(filename, trace_lines, mem):
    try:
        if not isinstance(trace_lines, list):
            raise TypeError("trace_lines must be a list")
        if not isinstance(mem, list):
            raise TypeError("mem must be a list")
        os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)
        with open(filename, 'w') as f:
            for line in trace_lines:
                f.write(line + "\n")
            for i in range(MEM_SIZE):
                mem_addr =DATA_MEM_START + i*4
                mem_val =mem[mem_addr//4]
                f.write(f"0x{mem_addr:08X}:{int_to_bin32(mem_val)}\n")
    except IOError as e:
        print(f"Error: Cannot write output: {e}", file=sys.stderr)
        sys.exit(1)
