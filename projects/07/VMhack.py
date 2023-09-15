import os
import sys

unique_count = 0

static_memory_start = 16
temp_memory_start = 5

## MEMORY MANAGEMENT

def push_constant_to_asm(value):
  return (f"@{value}\n" +
          "D=A\n" +
          "@SP\n" +
          "A=M\n" +
          "M=D\n" +
          "@SP\n" +
          "M=M+1\n" )

def push_to_asm_no_pointer(segment_prefix, position):
  return (
        f"@{position}\n" +
        "D=A\n" +
        f"@{segment_prefix}\n" +
        "A=A+D\n" +
        "D=M\n" +
        "@SP\n" +
        "A=M\n" +
        "M=D\n" +
        "@SP\n" +
        "M=M+1\n")

def push_to_asm(segment_prefix, pointer):
  return (
        f"@{pointer}\n" +
        "D=A\n" +
        f"@{segment_prefix}\n" +
        "A=M+D\n" +
        "D=M\n" +
        "@SP\n" +
        "A=M\n" +
        "M=D\n" +
        "@SP\n" +
        "M=M+1\n")


def pop_to_asm_no_pointer(segment_prefix, position):
  return (
        f"@{position}\n" +
        "D=A\n" +
        f"@{segment_prefix}\n" +
        "D=A+D\n" +
        "@R13\n" +
        "M=D\n" +
        "@SP\n" +
        "AM=M-1\n" +
        "D=M\n" +
        "@R13\n" +
        "A=M\n" +
        "M=D\n" )



def pop_to_asm(segment_prefix, pointer):
  return (
        f"@{pointer}\n" +
        "D=A\n" +
        f"@{segment_prefix}\n" +
        "D=M+D\n" +
        "@R13\n" +
        "M=D\n" +
        "@SP\n" +
        "AM=M-1\n" +
        "D=M\n" +
        "@R13\n" +
        "A=M\n" +
        "M=D\n" )




def pop_pointer_to_asm(segment_prefix):
  return (
      "@SP\n" +
      "MD=M-1\n" +
      "A=D\n"+
      "D=M\n"+
      f"@{segment_prefix}\n" +
      "M=D\n" )


def push_pointer_to_asm(segment_prefix):
  return (
      f"@{segment_prefix}\n" +
      "D=M\n" +
      "@SP\n" +
      "A=M\n" +
      "M=D\n" +
      "@SP\n" +
      "M=M+1\n")



def push_to_stack(segment, value):
  match segment:
    case 'constant':
      return push_constant_to_asm(value)
    case 'local':
     return push_to_asm("LCL", value)
    case 'argument':
      return push_to_asm("ARG", value)
    case 'this':
      return push_to_asm("THIS", value)
    case 'that':
      return push_to_asm("THAT", value)
    case 'static':
      return push_to_asm_no_pointer(static_memory_start, value)
    case 'temp':
      return push_to_asm_no_pointer(temp_memory_start, value)
    case 'pointer':
      if value == "0":
        return push_pointer_to_asm("THIS")
      else:
        return push_pointer_to_asm("THAT")

def pop_from_stack(segment, pointer):
  match segment:
    case 'local':
     return pop_to_asm("LCL", pointer)
    case 'argument':
      return pop_to_asm("ARG", pointer)
    case 'this':
      return pop_to_asm("THIS", pointer)
    case 'that':
      return pop_to_asm("THAT", pointer)
    case 'static':
      return pop_to_asm_no_pointer(static_memory_start, pointer)
    case 'temp':
      return pop_to_asm_no_pointer(temp_memory_start, pointer)
    case 'pointer':
      if pointer == '0':
        return pop_pointer_to_asm("THIS")
      else:
        return pop_pointer_to_asm("THAT")



# arithmetic management
# X = M Y = D
def get_x_and_y_to_asm():
  return (
          "@SP\n" +
          "A=M-1\n" +
          "D=M\n" +
          "@SP\n" +
          "M=M-1\n" +
          "A=M-1\n" )
def arithmetic_parser(command):

  match command:
    case 'add':
      return get_x_and_y_to_asm() + "M=M+D\n"
    case 'sub':
      return get_x_and_y_to_asm() + "M=M-D\n"
    case 'neg':
      return (
              "@SP\n" +
              "A=M-1\n" +
              "D=M\n" +
              "M=-D\n")
    case 'and':
      return get_x_and_y_to_asm() + "M=D&M\n"
    case 'or':
      return get_x_and_y_to_asm() + "M=D|M\n"
    case 'not':
      return  (
              "@SP\n" +
              "A=M-1\n" +
              "D=M\n" +
              "M=!M\n")
    case 'eq':
      return (
              get_x_and_y_to_asm() +
              "D=M-D\n" +
              f"@EQ.true{unique_count}\n" +
              "D;JEQ\n" +
              "@SP\n" +
              "A=M-1\n" +
              "M=0\n" +
              f"@EQ.finish{unique_count}\n" +
              "0;JMP\n" +
              f"(EQ.true{unique_count})\n" +
              "@SP\n" +
              "A=M-1\n" +
              "M=-1\n" +
              f"(EQ.finish{unique_count})\n")
    case 'gt':
      return (
              get_x_and_y_to_asm() +
              "D=M-D\n" +
              f"@GT.true{unique_count}\n" +
              "D;JGT\n" +
              "@SP\n" +
              "A=M-1\n" +
              "M=0\n" +
              f"@GT.finish{unique_count}\n" +
              "0;JMP\n" +
              f"(GT.true{unique_count})\n" +
              "@SP\n" +
              "A=M-1\n" +
              "M=-1\n" +
              f"(GT.finish{unique_count})\n")
    case 'lt':
      return (
            get_x_and_y_to_asm() +
            "D=M-D\n" +
            f"@LT.true{unique_count}\n" +
            "D;JLT\n" +
            "@SP\n" +
            "A=M-1\n" +
            "M=0\n" +
            f"@LT.finish{unique_count}\n" +
            "0;JMP\n" +
            f"(LT.true{unique_count})\n" +
            "@SP\n" +
            "A=M-1\n" +
            "M=-1\n" +
            f"(LT.finish{unique_count})\n")


def split_command(command):
  parts = command.strip().split()
  if len(parts) == 3:
        action, segment, value = parts
        if action == "push":
          return push_to_stack(segment, value)
        else:
          return pop_from_stack(segment,value)

  elif len(parts) == 1:
    return arithmetic_parser(parts[0])
  else:
    raise ValueError("Invalid command format: " + command)




def main():
  global unique_count
  if len(sys.argv) != 2:
    print("Usage: python assembler.py <input_file.vm>")
    sys.exit(1)


  input_file = sys.argv[1]
  output_file = os.path.splitext(input_file)[0] + ".asm"

  with open(input_file, "r") as vm_file, open(output_file, "w") as assembler_file:

    for line in vm_file:
      if line.strip():
        if not line.startswith("//"):
          unique_count += 1
          assembler_instructions = split_command(line.strip())
          assembler_file.write(assembler_instructions)



if __name__ == "__main__":
    main()