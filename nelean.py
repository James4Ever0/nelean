#!/usr/bin/env python3
import sys
import argparse
import tempfile
import shutil


factor = None
it = None
preserve_newlines = False


def tokenize(source, preserve):
    token = []

    class state:
        had_open = False
        comment = False
        string = False
        escape = False

    def flush():
        if token:
            yield "".join(token)
            del token[:]
        state.had_open = False
        state.comment = False
        state.string = False
        state.escape = False

    for line in source.readlines():
        line = line.strip()
        for c in line:
            if state.escape:
                state.escape = False
            elif state.string:
                if c == '"':
                    state.string = False
            elif state.comment:
                pass
            else:
                if c == "\\":
                    state.escape = True
                elif c == '"':
                    state.string = True
                elif c == ";":
                    state.comment = True
                elif c == ")":
                    yield from flush()
                elif c == "(":
                    if state.had_open == True:
                        yield from flush()
                    state.had_open = True
                elif c in (" ", "\t"):
                    yield from flush()
                    continue
            token.append(c)
        yield from flush()
        if preserve:
            yield "\n"


def split_score(*e):
    return sum(x ** (1.0 / factor) for x in e)


class NodeBase:
    def __init__(self):
        self.max_score = (0, self)
        self.size = None
        self.score_size = None


class StringNode(NodeBase):
    def __init__(self, data):
        super().__init__()
        self.data = data

    def done(self, depth):
        self.size = len(self.data)
        self.score_size = self.size


class CommentNode(NodeBase):
    def __init__(self, data):
        super().__init__()
        self.data = data

    def done(self, depth):
        self.size = len(self.data)
        self.score_size = self.size


class Node(NodeBase):
    def __init__(self, data):
        super().__init__()
        self.data = data

    def done(self, depth):
        self.size = len(self.data)
        self.score_size = self.size


class StructureNode(NodeBase):
    def __init__(self, start):
        super().__init__()
        self.start = start
        self.stop = None
        self.children = []
        self.size = None
        self.is_split = False
        self.parent = None

    def done(self, depth):
        for c in self.children:
            c.done(depth + 1)
        self._calc()

    def split(self):
        self.is_split = True
        self.rcalc()

    def _calc(self):
        stoplen = 0
        if self.stop:
            stoplen = len(self.stop)
        if self.is_split:
            self.size = max(
                len(self.start), stoplen, *(len(it) + c.size for c in self.children)
            )
            self.score_size = len(self.start)
            self.max_score = (0, None)
        else:
            self.size = (
                len(self.start) + 1 + sum(c.size for c in self.children) + 1 + stoplen
            )
            self.score_size = self.size
            score = [len(self.start), stoplen]
            for c in self.children:
                score.append(c.score_size)
            self.max_score = (split_score(*score), self)
        for c in self.children:
            if c.max_score[0] > self.max_score[0]:
                self.max_score = c.max_score

    def rcalc(self):
        self._calc()
        if self.parent is not None:
            self.parent.rcalc()


class PairNode(StructureNode):
    def done(self, depth):
        super().done(depth)

    def split(self):
        raise RuntimeError()

    def _calc(self):
        super()._calc()
        self.max_score = (0, None)
        for c in self.children:
            if c.max_score[0] > self.max_score[0]:
                self.max_score = c.max_score


def write(out, at, indent):
    if isinstance(at, StructureNode):
        out.write(at.start)
        if at.is_split:
            indent = indent + 1
            for c in at.children:
                out.write("\n" + it * indent)
                write(out, c, indent)
            indent = indent - 1
            out.write("\n" + it * indent + at.stop)
        else:
            for c in at.children:
                out.write(" ")
                write(out, c, indent)
            if not isinstance(at, PairNode):
                if at.start[-1] == "(":
                    out.write(" ")
                out.write(at.stop)
    else:
        out.write(at.data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--file", help="Format file rather than stdin.",
    )
    parser.add_argument(
        "-i",
        "--inplace",
        help="Modify file in place; requires -f.",
        action="store_true",
    )
    parser.add_argument(
        "-m", "--max-width", help="Maximum line width", type=int, default=500,
    )
    parser.add_argument(
        "-s",
        "--max-score",
        help="Split expressions over this score",
        type=float,
        default=9,
    )
    parser.add_argument(
        "-t", "--indent", help="Indent unit string", default="    ",
    )
    parser.add_argument(
        "--factor",
        help="Scoring bias factor, lower = long expressions, higher = expressions with more children",
        type=float,
        default=3,
    )
    parser.add_argument(
        "-p",
        "--preserve",
        help="Sort of preserve existing newlinesish",
        action="store_true",
    )
    parser.add_argument(
        "--debug-scores",
        help="Show each split with associated score",
        action="store_true",
    )
    args = parser.parse_args()
    global factor, it
    factor = args.factor
    it = args.indent

    if args.file:
        source = open(args.file, "rt")
        if args.inplace:
            dest = tempfile.NamedTemporaryFile(mode="wt", delete=False)
        else:
            dest = sys.stdout
    else:
        source = sys.stdin
        dest = sys.stdout

    must_split = set()

    tree = [StructureNode("")]
    for token in tokenize(source, args.preserve):

        def append(child):
            tree[-1].children.append(child)
            child.parent = tree[-1]
            if isinstance(tree[-1], PairNode):
                tree.pop()

        if token == "\n":
            must_split.add(tree[-1])
        elif token[0] == '"':
            append(StringNode(token))
        elif token[0] == ";":
            must_split.add(tree[-1])
            append(CommentNode(token))
        elif "(" in token:
            token_ = StructureNode(token)
            append(token_)
            tree.append(token_)
        elif ")" in token:
            tree[-1].stop = token
            tree.pop()
        elif token[0] == "#" and ":" in token:
            token_ = PairNode(token)
            append(token_)
            tree.append(token_)
        else:
            append(Node(token))

    roots = tree[0].children
    for root in roots:
        root.parent = None
        root.done(0)

    for c in must_split:
        if isinstance(root, PairNode):
            continue
        c.split()

    for root in roots:
        while root.size > args.max_width or root.max_score[0] > args.max_score:
            if args.debug_scores:
                print("Splitting expression with score: {}".format(root.max_score[0]))
                sys.stdout.write(it)
                write(sys.stdout, root.max_score[1], 1)
                print("\n\n")
            root.max_score[1].split()

    for root in roots:
        write(dest, root, 0)
        dest.write("\n")
        if not args.preserve:
            dest.write("\n")

    dest.flush()

    if args.file and args.inplace:
        shutil.move(dest.name, args.file)
