import sys

def assemble(input_path, output_path, readable_path=None):
  with open(input_path, 'r') as f:
        lines = f.readlines()           #collects all instructions in a list of strings

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 Assembler.py <input.asm> <output.bin> [readable.txt]")
        sys.exit(1)

    input_path    = sys.argv[1]
    output_path   = sys.argv[2]
    readable_path = sys.argv[3] if len(sys.argv) >3 else None

    assemble(input_path, output_path, readable_path)
