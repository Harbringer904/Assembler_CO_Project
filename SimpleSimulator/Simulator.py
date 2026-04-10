import sys
from memory import load_instructions,save_output
from instructions import(
run_r_type,run_i_type_alu,run_load_word,run_store_word,
run_jalr,run_branch,run_lui,run_auipc,run_jal,
run_rst,run_rvrs,run_halt,
)

def int_to_bin32(val):
 return f"0b{val:032b}"

def create_simulator():
 regs=[0]*32
 regs[2]=0x0000017C
 return{
  "regs":regs,
  "pc":0,
  "inst_mem":[],
  "memory":[0]*16416,
  "halted":False,
  "trace_lines":[],
 }

def execute_one_instruction(state,out_file):
 pc=state["pc"]
 regs=state["regs"]
 memory=state["memory"]
 inst_mem=state["inst_mem"]
 trace_lines=state["trace_lines"]

 if pc<0 or (pc//4)>=len(inst_mem):
  state["halted"]=True
  return

 if pc%4!=0:
  print(f"Error: Misaligned PC 0x{pc:08x}",file=sys.stderr)
  state["halted"]=True
  return

 try:
  original_pc=pc
  inst_bin=inst_mem[pc//4]

  if not isinstance(inst_bin,str)or len(inst_bin)!=32:
   print(f"Error: Invalid instruction at PC 0x{pc:08x}",file=sys.stderr)
   state["halted"]=True
   return

  if not all(c in '01' for c in inst_bin):
   print(f"Error: Non-binary instruction at PC 0x{pc:08x}",file=sys.stderr)
   state["halted"]=True
   return

  opcode=inst_bin[25:32]
  next_pc=pc+4

  if opcode=="0110011":
   run_r_type(inst_bin,regs)
  elif opcode=="0010011":
   run_i_type_alu(inst_bin,regs)
  elif opcode=="0000011":
   run_load_word(inst_bin,regs,memory,pc,trace_lines,out_file)
  elif opcode=="0100011":
   run_store_word(inst_bin,regs,memory,pc,trace_lines,out_file)
  elif opcode=="1100111":
   new_pc=run_jalr(inst_bin,regs,pc)
   if new_pc is not None:
    next_pc=new_pc
  elif opcode=="1100011":
   new_pc=run_branch(inst_bin,regs,pc)
   if new_pc is not None:
    next_pc=new_pc
  elif opcode=="0110111":
   run_lui(inst_bin,regs)
  elif opcode=="0010111":
   run_auipc(inst_bin,regs,pc)
  elif opcode=="1101111":
   new_pc=run_jal(inst_bin,regs,pc)
   if new_pc is not None:
    next_pc=new_pc
  elif opcode=="0001011":
   run_rst(regs)
  elif opcode=="1111011":
   run_rvrs(inst_bin,regs)
  elif opcode=="0101011":
   result=run_halt()
   if result=="HALT":
    next_pc=pc
    state["halted"]=True
  else:
   print(f"Error: Unknown opcode '{opcode}' at PC 0x{pc:08x}",file=sys.stderr)
   state["halted"]=True
   return

  state["pc"]=next_pc
  trace_str=int_to_bin32(state["pc"])
  for val in regs:
   trace_str=trace_str+" "+int_to_bin32(val)
  trace_lines.append(trace_str)

  if state["pc"]==original_pc:
   state["halted"]=True

 except (ValueError,IndexError,KeyError)as e:
  print(f"Error at PC 0x{pc:08x}: {e}",file=sys.stderr)
  sys.exit(1)
 except Exception as e:
  print(f"Unexpected error at PC 0x{pc:08x}: {type(e).__name__}: {e}",file=sys.stderr)
  sys.exit(1)

def run_simulator(state,out_file):
 iterations=0
 max_iterations=1000000

 while not state["halted"]:
  iterations+=1
  if iterations>max_iterations:
   print(f"Error: Exceeded max iterations ({max_iterations})",file=sys.stderr)
   break
  execute_one_instruction(state,out_file)

def main():
 if len(sys.argv)<3:
  print("Usage: python Simulator.py <input.txt> <output.txt>",file=sys.stderr)
  sys.exit(1)

 in_file=sys.argv[1]
 out_file=sys.argv[2]

 try:
  state=create_simulator()
  state["inst_mem"]=load_instructions(in_file)
  run_simulator(state,out_file)
  save_output(out_file,state["trace_lines"],state["memory"])
 except SystemExit:
  raise
 except Exception as e:
  print(f"Fatal error: {type(e).__name__}: {e}",file=sys.stderr)
  sys.exit(1)

if __name__=="__main__":
 main()
