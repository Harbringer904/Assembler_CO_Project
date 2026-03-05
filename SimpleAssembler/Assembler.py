import sys
from Encoder import encode

def lineToList(line):

    #account for line ='' (empty line)
    if not line:      
        return None, None, []

    #label detection
    label = None
    if ':' in line:
        colon_idx = line.index(':')
        label = line[:colon_idx].strip()
        line = line[colon_idx+1:].strip()

    #empty label edge case
    if not line:
        return label, None, []

    # Split neumonic like add,sub,and,etc from operands like a0,s0,etc
    parts = line.split(None, 1)   # split on first whitespace
    neumonic = parts[0].lower()
    operands = []
    if len(parts) > 1:
        # Split by comma, but account for parentheses of imm(reg)
        operands = [o.strip() for o in parts[1].split(',')]

    return label, neumonic, operands

def assemble(input_path, output_path, readable_path=None):
    with open(input_path, 'r') as f:
            lines = f.readlines()           #collects all instructions in a list of strings
        
    # 1st pass to collect labels and respective addresses (PC values)
    labels = {}
    pc = 0
    instruction_lines = []   # list of (orig_lineno, label, neumonic, operands)

    for lineno, line in enumerate(lines, start=1):
        label, neumonic, operands = lineToList(line)

        if label is not None:
            labels[label] = pc   # label points to CURRENT pc

        if neumonic is not None:
            instruction_lines.append((lineno, neumonic, operands, pc))
            pc += 4

    #2nd pass to actually encode
    binary_lines = []
    for (lineno, neumonic, operands, pc) in instruction_lines:
        binary = encode(neumonic, operands, pc, labels)        #encode is a function we will make in another file called encoder.py that converts the instructions into binary
        binary_lines.append(binary)

    #writing in the binary file
    with open(output_path, 'w') as f:
        for b in binary_lines:
            f.write(b + '\n')

    #insert code for readable path afterwards
    
    print(f"Assembly successful. {len(binary_lines)} instructions written.")
  

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 Assembler.py <input.asm> <output.bin> [readable.txt]")
        sys.exit(1)

    input_path    = sys.argv[1]
    output_path   = sys.argv[2]
    readable_path = sys.argv[3] if len(sys.argv) >3 else None

    assemble(input_path, output_path, readable_path)
