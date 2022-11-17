import sys

code = sys.stdin.read()

# print("CODE?")
# print(code, end="")
# print("CODE!")

mcode = code.split("\n")
cont = False
endofline = False
for index, line in enumerate(mcode):
    if not endofline:
        if cont:
            cont=False
            continue
    try:
        stripped_line = line.strip()
        stripped_next_line = mcode[index+1].strip()
        for signal in [":","#^"]:
            if stripped_line.startswith(signal) and len(stripped_line) < 10:
                if not stripped_next_line.startswith(signal) and len(stripped_next_line) < 10 and (not any([stripped_next_line.startswith(x) for x in ["[","]","{","}","(",")",";"]])):
                    # next line will be merged and stripped.
                    cont=True
                    line += " "+ stripped_next_line
                    break
    except:
        # cancel continue? because we don't have next line.
        endofline=True
    print(line) # automatically add spliter?