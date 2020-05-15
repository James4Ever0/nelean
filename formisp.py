#!/usr/bin/env python
import sys
import argparse
import tempfile
import shutil


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f',
        '--file',
        help='Format file rather than stdin.',
    )
    parser.add_argument(
        '-i',
        '--inplace',
        help='Modify file in place; requires -f.',
        action='store_true',
    )
    args = parser.parse_args()

    if args.file:
        source = open(args.file, 'rt')
        if args.inplace:
            dest = tempfile.NamedTemporaryFile(mode='wt', delete=False)
        else:
            dest = sys.stdout
    else:
        source = sys.stdin
        dest = sys.stdout

    indent = [(0, 0)]
    blanks = 0
    state = 'code'
    for line in source.readlines():
        if state != 'code':
            dest.write(line + '\n')
        else:
            # Normalize space at end of line
            line = line.strip()

            # Remove blank lines
            if line == '':
                blanks += 1
                if blanks > 1:
                    continue
                dest.write('\n')
                continue
            else:
                blanks = 0

            # Write line
            use_indent = indent[-1][1]
            if line[0] == ')':
                use_indent = use_indent - 1
            dest.write('    ' * use_indent + line + '\n')

        # Calculate indentation change
        prev = None
        delta = 0
        for cur in line:
            if state == 'code':
                if cur == '(':
                    delta += 1
                elif cur == ')':
                    delta -= 1
                elif cur == '"':
                    state = 'string'
                elif cur == ';':
                    break
                elif cur == '#!':
                    state = 'comment'
            elif state == 'string':
                if cur == '"' and prev != '\\':
                    state = 'code'
            elif state == 'comment':
                if cur == '!' and prev == '#':
                    state = 'code'
            else:
                raise RuntimeError()
            prev = cur
        if delta == 0:
            pass
        else:
            new_count = indent[-1][0] + delta
            if delta > 0:
                indent.append((new_count, indent[-1][1] + 1))
            elif delta < 0:
                while indent[-1][0] > 0 and indent[-1][0] > new_count:
                    indent.pop()
    dest.flush()

    if args.file and args.inplace:
        shutil.move(dest.name, args.file)