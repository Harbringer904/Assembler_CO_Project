# RV32I Assembler

A custom assembler for a subset of the RISC-V 32-bit integer (RV32I) instruction set, built as part of a Computer Organization course project.

The assembler reads `.asm` assembly files and converts them into `.bin` binary output files (32-bit binary strings, one per line). If errors are found in the input, the assembler reports them with line numbers instead of generating output.

---

## Team Members

| Roll No. |       Name       |                                   Role                                    |
|----------|------------------|---------------------------------------------------------------------------|
|  2025277 |   Krunal Patel   |       Instruction metadata, Main Assembler Logic, error handling          |
|  2025264 | Kinshuk Tripathi |      Instruction metadata, Utility functions logic, error handling        |
|  2025292 |  Lakshika Tayal  |    Register Table, Encoder - B, U, J type instructions, error handling    |
|  2025187 |    Dhruv Nath    |        Encoder — R, I, S, Bonus type instructions, error handling         |

---

## Project Structure

```
assembler/
├── assembler.py       # Main entry point — argument parsing, two-pass logic, error reporting
├── encoder.py         # Instruction encoding — converts instructions to 32-bit binary
├── instructions.py    # Instruction metadata table — type, opcode, funct3, funct7
├── registers.py       # Register name to 5-bit binary mapping (ABI names + x0-x31)
├── utils.py           # Helper functions — immediate parsing, binary conversion, memory operand parsing
└── README.md          # This file
```

---

## Supported Instructions

### R-Type
`add`, `sub`, `sll`, `srl`, `slt`, `sltu`, `xor`, `or`, `and`

### I-Type
`addi`, `sltiu`, `lw`, `jalr`

### S-Type
`sw`

### B-Type
`beq`, `bne`, `blt`, `bge`, `bltu`, `bgeu`

### U-Type
`lui`, `auipc`

### J-Type
`jal`

### Bonus Instructions
`mul`, `rst`, `halt`, `rvrs`

---

## Requirements

- Python 3.x
- No external libraries required

---

## How to Run

```bash
python assembler.py <input_file.asm> <output_file.bin> <readable_file.txt>
```

**Example:**
```bash
python assembler.py program.asm program.bin program.txt
```

## Input Format

The input is a plain text `.asm` file. Each line can be one of:

- An empty line — ignored
- A label — must start with a letter or underscore, followed by a colon: `loop:` or `_loop:`
- An instruction — opcode followed by operands separated by commas

**Register names** can be written as ABI names (`zero`, `ra`, `sp`, `t0`, `a0`, etc.) or as `x0`–`x31`.

**Immediate values** can be written as decimal (`42`, `-8`), hexadecimal (`0xFF`), or binary (`0b1010`).

**Memory operands** use the format `imm(reg)`, for example `20(sp)` or `-4(s0)`.

**Labels** in branch/jump instructions are resolved automatically by the assembler.

### Example Input

```asm
addi t0,zero,5
addi t1,zero,3
loop: add t2,t0,t1
      addi t0,t0,-1
      bne t0,zero,loop
beq zero,zero,0
```

---

## Output Format

If the program is valid, a `.bin` file is generated where each line is a 32-character string of `0`s and `1`s representing one encoded instruction.

**Example output line:**
```
00000000001100000000001010010011
```

If there are errors, they are printed to the terminal with line numbers and no `.bin` file is created.

---

## Error Handling

The assembler detects and reports the following errors:

- Unknown instruction name (typo in mnemonic)
- Unknown register name
- Immediate value out of range for the instruction's bit field
- Invalid immediate format (non-numeric)
- Invalid or duplicate label names
- Wrong number of operands for an instruction
- Malformed memory operand (missing parentheses)
- Missing virtual halt instruction (`beq zero,zero,0`)
- Virtual halt not being the last instruction

---

## Virtual Halt

All programs **must** end with the virtual halt instruction:

```asm
beq zero,zero,0
```

This signals the simulator to stop execution. The assembler will report an error if this instruction is missing or is not the last instruction in the file.

---

## ISA Reference

This assembler implements a subset of the [RV32I RISC-V specification](https://msyksphinz-self.github.io/riscv-isadoc/html/rvi.html).

An online RISC-V simulator for reference: https://www.cs.cornell.edu/courses/cs3410/2019sp/riscv/interpreter/

---

## Acknowledgments

This project utilized AI assistance for very specific and minute tasks such as writing this README documentation file and other auxiliary development tasks. The core assembler logic, instruction encoding, error handling, and all fundamental functionality were developed by the team members listed above.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
