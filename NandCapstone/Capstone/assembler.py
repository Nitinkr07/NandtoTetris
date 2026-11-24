import sys
import os

PREDEFINED_SYMBOLS = {
    "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
    "R0": 0, "R1": 1, "R2": 2, "R3": 3, "R4": 4, "R5": 5, "R6": 6, "R7": 7,
    "R8": 8, "R9": 9, "R10": 10, "R11": 11, "R12": 12, "R13": 13, "R14": 14, "R15": 15,
    "SCREEN": 16384, "KBD": 24576
}

COMP_TABLE = {
    "0": "0101010", "1": "0111111", "-1": "0111010",
    "D": "0001100", "A": "0110000", "!D": "0001101", "!A": "0110001",
    "-D": "0001111", "-A": "0110011", "D+1": "0011111", "A+1": "0110111",
    "D-1": "0001110", "A-1": "0110010", "D+A": "0000010", "D-A": "0010011",
    "A-D": "0000111", "D&A": "0000000", "D|A": "0010101",
    "M": "1110000", "!M": "1110001", "-M": "1110011", "M+1": "1110111",
    "M-1": "1110010", "D+M": "1000010", "D-M": "1010011", "M-D": "1000111",
    "D&M": "1000000", "D|M": "1010101"
}

DEST_TABLE = {
    "": "000", "M": "001", "D": "010", "MD": "011",
    "A": "100", "AM": "101", "AD": "110", "AMD": "111"
}

JUMP_TABLE = {
    "": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
    "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"
}

def clean_line(line):
    # Remove inline comments and all whitespace
    line = line.split("//")[0].strip()
    return "".join(line.split())

def assemble(input_path):
    with open(input_path, "r", encoding="utf-8") as f:
        raw_lines = f.readlines()

    symbol_table = dict(PREDEFINED_SYMBOLS)
    defined_labels = set()
    cleaned_instructions = []

    # First Pass: Record labels and warn on duplicates (K=41 -> 41 mod 3 = 2)
    rom_address = 0
    for line_num, raw in enumerate(raw_lines, start=1):
        line = clean_line(raw)
        if not line:
            continue
        if line.startswith("(") and line.endswith(")"):
            label = line[1:-1]
            if label in defined_labels:
                print(f"Warning (Line {line_num}): Duplicate label '({label})' defined.")
            else:
                defined_labels.add(label)
                symbol_table[label] = rom_address
        else:
            cleaned_instructions.append(line)
            rom_address += 1

    # Second Pass: Translate instructions into 16-bit binary
    next_ram_address = 16
    machine_code = []

    for line in cleaned_instructions:
        if line.startswith("@"):
            symbol = line[1:]
            if symbol.isdigit():
                address = int(symbol)
            else:
                if symbol not in symbol_table:
                    symbol_table[symbol] = next_ram_address
                    next_ram_address += 1
                address = symbol_table[symbol]
            machine_code.append(f"0{address:015b}")
        else:
            # C-instruction: dest=comp;jump
            dest, comp_jump = ("", line)
            if "=" in line:
                dest, comp_jump = line.split("=", 1)
            comp, jump = (comp_jump, "")
            if ";" in comp_jump:
                comp, jump = comp_jump.split(";", 1)

            c_bits = COMP_TABLE[comp]
            d_bits = DEST_TABLE[dest]
            j_bits = JUMP_TABLE[jump]
            machine_code.append(f"111{c_bits}{d_bits}{j_bits}")

    output_path = os.path.splitext(input_path)[0] + ".hack"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(machine_code) + "\n")
    print(f"Successfully assembled {input_path} -> {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python assembler.py <file.asm>")
        sys.exit(1)
    assemble(sys.argv[1])