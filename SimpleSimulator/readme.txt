# RV32I Simulator

A custom simulator for a subset of the RISC-V 32-bit integer (RV32I) instruction set, built as part of a Computer Organization course project.

The simulator reads a `.txt`/`.bin` file containing 32-bit binary instructions (one per line), executes them sequentially, and writes execution trace plus data memory dump to an output file.

---

## Team Members

| Roll No. |       Name       |                                   Role                                    |
|----------|------------------|---------------------------------------------------------------------------|
|  2025277 |   Krunal Patel   |       Simulator control flow, integration, error handling                 |
|  2025264 | Kinshuk Tripathi |      Memory model, utility logic, error handling                          |
|  2025292 |  Lakshika Tayal  |      Branch/jump and state update handling, error handling                |
|  2025187 |    Dhruv Nath    |      Instruction execution helpers, trace formatting, error handling      |

---

## Project Structure

```
SimpleSimulator/
├── Simulator.py      # Main entry point — fetch/decode/execute loop, trace generation
├── instructions.py   # Instruction handlers — R, I, S, B, U, J, and bonus ops
├── memory.py         # Instruction loading, memory read/write, output dump helpers
└── readme.txt        # This file
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
python Simulator.py <input_file.txt> <output_file.txt>
```

**Example:**
```bash
python Simulator.py input.txt output.txt
```

---

## Input Format

The input is a plain text file where each non-empty line must be a 32-character binary instruction string.

**Example input line:**
```
00000000001100000000001010010011
```

You can generate this file using your assembler output.

---

## Output Format

The output file contains:

1. **Execution Trace**
	- One line per executed instruction
	- Each line stores current PC and all register values in 32-bit binary format

2. **Data Memory Dump**
	- 32 words starting at address `0x00010000`
	- Format: `0xADDR:0b<32-bit-value>`

**Example memory dump line:**
```
0x00010000:0b00000000000000000000000000000000
```

---

## Simulator Behavior

- Registers are initialized to `0`, with stack pointer (`x2`) initialized to `0x0000017C`
- Program counter starts at `0`
- Each instruction is fetched using `pc // 4`
- Normal instruction flow increments PC by 4
- Branch/jump instructions update PC as per instruction semantics
- Halt instruction stops execution

---

## Error Handling

The simulator detects and reports the following important errors:

- Input file not found or unreadable
- Empty or malformed binary instruction lines
- Non-binary instruction content
- Invalid/misaligned PC
- Unknown opcode
- Unsupported funct combinations for instruction handlers
- Invalid register indices
- Invalid/unaligned memory access
- Memory out-of-bounds read/write
- Output file write failures
- Excessive iterations (infinite loop protection)

On critical runtime errors, the simulator prints an error message and exits.

---

## Notes

- Keep assembler and simulator instruction support aligned.
- Ensure the input file contains only machine-code instruction lines expected by this simulator.
- For clean end-of-program behavior, include the expected halt flow in your program.

---

## License

This project is licensed under the MIT License. See `LICENSE` for details.
