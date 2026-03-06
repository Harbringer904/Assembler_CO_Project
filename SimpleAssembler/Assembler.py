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

#function to determine if a label is valid or not
def is_label(label):      
    if len(label) == 0:
        return False
    
    # First character must be a letter or underscore
    first_char = label[0]
    if first_char.isalpha()!= True and first_char != '_':
        return False
    
    # Rest of the characters must be letters, digits, or underscores
    for char in label[1:]:
        if char.isalnum()!= True and char != '_':
            return False
    
    return True

def is_halt_valid(instruction):
    #checks if given instruction is valid virtual halt (beq zero, zero, 0) or not
    if instruction[1] != 'beq':
        return False
    if instruction[2][0] != 'zero' or instruction[2][1] != 'zero' or instruction[2][2] != '0':
        return False
    return True

def assemble(input_path, output_path, readable_path=None):
    with open(input_path, 'r') as f:
        lines = f.readlines()           #collects all instructions in a list of strings

    errors = []                     #collects all errors to print at the end
        
    # 1st pass to collect labels and respective addresses (PC values)
    labels = {}
    pc = 0
    instruction_lines = []   # list of (orig_lineno, label, neumonic, operands)

    for lineno, line in enumerate(lines, start=1):
        label, neumonic, operands = lineToList(line)

        if label is not None:
            if not is_label(label):
                errors.append(f"Line {lineno}: Invalid label name '{label}'")
            elif label in labels:
                errors.append(f"Line {lineno}: Duplicate label '{label}'")
            else:
                labels[label] = pc   # label points to CURRENT pc

        if neumonic is not None:
            instruction_lines.append((lineno, neumonic, operands, pc))
            pc += 4

    #error handling for no instructions and invalid virtual halt
    if not instruction_lines:
        errors.append("Error: No instructions found.")         
        for e in errors:
            print(e)
        sys.exit(1)                     #exiting with error code 1 after printing all the errors
    
    if not is_halt_valid(instruction_lines[-1]):
        errors.append("Error: Last instruction must be 'beq zero, zero, 0' to serve as virtual halt.")
        for e in errors:
            print(e)
        sys.exit(1)

    #2nd pass to actually encode
    binary_lines = []
    for (lineno, neumonic, operands, pc) in instruction_lines:
        binary = encode(neumonic, operands, pc, labels)        #encode is a function we will make in another file called encoder.py that converts the instructions into binary
        binary_lines.append(binary)

    #writing in the binary file
    with open(output_path, 'w') as f:
        for b in binary_lines:
            f.write(b + '\n')

    #writing in the human readable file if the path is given with line number, address, binary, and original instruction
    if readable_path:
        with open(readable_path, 'w') as f:
            f.write("Line |  Address   |             Binary               | Original Instruction\n")
            f.write("---- | ---------- | -------------------------------- | --------------------\n")
            for i, (line, binary, (orig_lineno, neumonic, operands, pc)) in enumerate(zip(lines, binary_lines, instruction_lines), start=1):
                f.write(f"  {i}  | 0x{pc:08X} | {binary} | {line}")
    
    print(f"Assembly successful. {len(binary_lines)} instructions written.")
  

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 Assembler.py <input.asm> <output.bin> [readable.txt]")
        sys.exit(1)

    input_path    = sys.argv[1]
    output_path   = sys.argv[2]
    readable_path = sys.argv[3] if len(sys.argv) >3 else None

    assemble(input_path, output_path, readable_path)
