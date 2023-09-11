import tempfile
import sys
import os

dest_mapping = {
  "null": "000",
  "M": "001",
  "D": "010",
  "MD":"011",
  "A": "100",
  "AM":"101",
  "AD": "110",
  "AMD": "111"
}

jump_map = {
  "null": "000",
  "JGT": "001",
  "JEQ": "010",
  "JGE": "011",
  "JLT": "100",
  "JNE": "101",
  "JLE": "110",
  "JMP": "111"
}

comp_map ={
  "0": "0101010",
  "1": "0111111",
  "-1": "0111010",
  "D": "0001100",
  "A": "0110000",
  "!D": "0001100",
  "!A": "0110001",
  "-D": "0001111",
  "-A": "0110011",
  "D+1": "0011111",
  "A+1": "0110111",
  "D-1": "0001110",
  "A-1": "0110010",
  "D+A": "0000010",
  "D-A": "0010011",
  "A-D": "0000111",
  "D&A": "0000000",
  "D|A": "0010101",
  "M": "1110000",
  "!M": "1110001",
  "M+1": "1110111",
  "M-1": "1110010",
  "D+M": "1000010",
  "D-M": "1010011",
  "M-D": "1000111",
  "D&M": "1000000",
  "D|M": "1010101",
}

symbol_table ={
  "R0": 0,
  "R1": 1,
  "R2": 2,
  "R3": 3,
  "R4": 4,
  "R5": 5,
  "R6": 6,
  "R7": 7,
  "R8": 8,
  "R9": 9,
  "R10": 10,
  "R11": 11,
  "R12": 12,
  "R13": 13,
  "R14": 14,
  "R15": 15,
  "SCREEN": 16384,
  "KBD": 24576,
  "SP": 0,
  "LCL": 1,
  "ARG":2,
  "THIS":3,
  "THAT":4
}

variable_counter = 16

def clean_line(line):
    cleaned_line = line.strip()

    if '//' in cleaned_line:
        cleaned_line = cleaned_line.split('//')[0].strip()

    return cleaned_line

def split_instruction(instruction):
    dest = None
    comp = None
    jump = None

    parts = instruction.split('=')

    if len(parts) == 2:
        dest, rest = parts
        if ";" in rest:
            comp, jump = rest.split(';')
        else:
            comp = rest
    else:
        rest = parts[0]
        if ";" in rest:
            comp, jump = rest.split(';')
        else:
            comp = rest

    # Set default values if 'dest' and 'jump' are not provided
    if dest is None:
        dest = "null"
    if jump is None:
        jump = "null"

    return dest, comp, jump


def parse_to_a_inst(string):
  n = int(string)
  return bin(n)[2:].zfill(16)

def parse_to_c_inst(string):

  dest, comp, jump = split_instruction(string.strip())

  return f"111{comp_map[comp]}{dest_mapping[dest]}{jump_map[jump]}"

def add_or_not_symbol_to_table(string):
    global variable_counter
    if string.isdigit():
        return parse_to_a_inst(string)
    elif string in symbol_table:
        return parse_to_a_inst(symbol_table[string])
    else:
        symbol_table[string] = variable_counter
        variable_counter += 1
        return parse_to_a_inst(symbol_table[string])





def main():
  if len(sys.argv) != 2:
    print("Usage: python assembler.py <input_file.asm>")
    sys.exit(1)


  input_file = sys.argv[1]
  output_file = os.path.splitext(input_file)[0] + ".hack"

  with open(input_file, "r") as program_file, open(output_file, "w") as binary_file:
    with tempfile.NamedTemporaryFile(delete=False, mode='w') as aux_file:
      line_number = 0
      for line in program_file:
        if line.strip():
          if not line.startswith("//"):
            cleaned_line = clean_line(line)
            if cleaned_line:
                if cleaned_line.startswith("("):
                  symbol_table[cleaned_line.replace("(", "").replace(")", "")] = line_number
                else:
                  aux_file.write(cleaned_line + '\n')
                  line_number += 1

    with open(aux_file.name, "r") as aux_file:
      for line in aux_file:
        if line.startswith("@"):
          binary_instruction = add_or_not_symbol_to_table(line.strip().replace("@", ""))
          binary_file.write(binary_instruction + '\n')
        else:
          c_instruction = parse_to_c_inst(line)
          binary_file.write(c_instruction + '\n')

if __name__ == "__main__":
    main()