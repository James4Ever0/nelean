#!/usr/bin/env python3
import sys
import argparse
import tempfile
# import shutil
import re

def useful_patterns(data):
    dataDict = {}
# with open("test2.hy","r") as f:
    # data=f.read()
    sexps=[ r"(#\[\[(?:\n|.)+\]\])",
            r'(f"(?:\\\"|[^"])*")', # shall you verify the code legitimacy first.
            r'(r"(?:\\\"|[^"])*")',
            r'(b"(?:\\\"|[^"])*")',
            r'("(?:\\\"|[^"])*")',
        ]
    sexp_start=r"[^#](\([ ]+[^ ^\)])"
    nsexp_starts=[r"[{][^ ^}]",r"[\[][^ ^\]]",r"#*(\([ ]+[^ ^\)])"]
    # comments=r";.*" # this is dumb. really.
    comments = r"(?<!\\\\);(;{1,3})?"
    # what do you want to do about comments? just ignore?
    for exp, flag in[(comments, "comment")]+[(x, "string") for x in sexps]+[(sexp_start,"fix_s")]+[(nsexp_start,"fix_ns") for nsexp_start in nsexp_starts]:
        exp0=re.compile(exp)
        vals=exp0.findall(data)
        for val in vals:
            if type(val) == str: # or it will be tuple.
                val = [val]
            elif type(val) == tuple:
                val = list(val)
            for subval in val:
                if type(subval) == str:
                    try:
                    # now begin to replace shit.
                        if flag == "string":
                            while True:
                                import uuid
                                mhash = str(uuid.uuid4()).split("-")[0]
                                string_id = f"string_{mhash}"
                                if string_id not in dataDict.keys():
                                    # place this value in dataDict.
                                    dataDict[string_id]=subval
                                    break
                            if "\n" in subval or len(subval) > 10:
                                string_id += "\n"
                            data = data.replace(subval, " "+string_id+" ")
                        elif flag == "fix_s":
                            fixed_subval = subval.replace(" ","")
                            data = data.replace(subval, fixed_subval)
                        elif flag == "fix_ns":
                            fixed_subval = subval[0]+" "+subval[1:]
                            data = data.replace(subval, fixed_subval)
                        elif flag =="comment":
                            while True:
                                import uuid
                                mhash = str(uuid.uuid4()).split("-")[0]
                                comment_id = f"comment_{mhash}"
                                if comment_id not in dataDict.keys():
                                    # place this value in dataDict.
                                    dataDict[comment_id]=subval
                                    break
                            # replace it with id.
                            data = data.replace(subval, f";{comment_id}")
                    except:
                        pass
        # print("___")
        # print("expression:")
        # print(exp)
        # print("value found:")
        # print(val)
    # print("DATADICT:", dataDict)
    # print("____CODE____")
    # recover comments here.
    # no need to recover comments here.
    # for key in dataDict.keys():
    #     if key.startswith("comment_"):
    #         data = data.replace(key, dataDict[key])
    # print(data)
    return data, dataDict

def reparse_fix_code(code):
    # print("CODE?")
    # print(code, end="")
    # print("CODE!")
    lines = []

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
                    if not stripped_next_line.startswith(signal) and len(stripped_next_line) < 10 and (not any([stripped_next_line.startswith(x) for x in (["[","]","{","}","(",")",";"] if signal == ":" else [";"])])):
                        # next line will be merged and stripped.
                        cont=True
                        line += " "+ stripped_next_line
                        break
        except:
            # cancel continue? because we don't have next line.
            endofline=True
        # print(line) # automatically add spliter?
        lines.append(line)
    return "\n".join(lines)

##########################
def final_fix(data):
    # mcode = code.split('\n')
    dataDict = {}
    # comments=r";.*"
    comments = r"(?<!\\\\);(;{1,3})?"
    # so it contains space.
    # nsexp_starts=[r"[{][ ^}]",r"[\[][ ^\]]",r"#*(\([ ]+[ ^\)])"]
    nsexp_starts = [r"(\([ ]+[^ ^\)])",r"({[ ]+[^ ^}])", r"(\[[ ]+[^ ^\]])"]

    for exp, flag in[(comments, "comment")]+[(nsexp_start,"fix_ns") for nsexp_start in nsexp_starts]:
        exp0=re.compile(exp)
        vals=exp0.findall(data)
        for val in vals:
            if type(val) == str: # or it will be tuple.
                val = [val]
            elif type(val) == tuple:
                val = list(val)
            for subval in val:
                if type(subval) == str:
                    try:
                    # now begin to replace shit.
                        # if flag == "string":
                        #     while True:
                        #         import uuid
                        #         mhash = str(uuid.uuid4()).split("-")[0]
                        #         string_id = f"string_{mhash}"
                        #         if string_id not in dataDict.keys():
                        #             # place this value in dataDict.
                        #             dataDict[string_id]=subval
                        #             break
                        #     if "\n" in subval or len(subval) > 10:
                        #         string_id += "\n"
                        #     data = data.replace(subval, " "+string_id+" ")
                        # elif flag == "fix_s":
                        #     fixed_subval = subval.replace(" ","")
                        #     data = data.replace(subval, fixed_subval)
                        if flag == "fix_ns":
                        # elif flag == "fix_ns":
                            fixed_subval = subval.replace(" ","")
                            # fixed_subval = subval[0]+" "+subval[1:]
                            data = data.replace(subval, fixed_subval)
                        elif flag =="comment":
                            while True:
                                import uuid
                                mhash = str(uuid.uuid4()).split("-")[0]
                                comment_id = f"comment_{mhash}"
                                if comment_id not in dataDict.keys():
                                    # place this value in dataDict.
                                    dataDict[comment_id]=subval
                                    break
                            # replace it with id.
                            data = data.replace(subval, comment_id)
                    except:
                        pass
        # print("___")
        # print("expression:")
        # print(exp)
        # print("value found:")
        # print(val)
    # print("DATADICT:", dataDict)
    # print("____CODE____")
    # recover comments here.
    for key in dataDict.keys():
        if key.startswith("comment_"):
            data = data.replace(key, dataDict[key])
    # print(data)
    return data, dataDict

##########################

factor = None
it = None
preserve_newlines = False
# man what the fuck is this?

def tokenize(source, preserve):
    token = []

    class state:
        had_open = False
        comment = False
        string = False
        # pending = False
        escape = False

    def flush():
        if token:
            yield "".join(token)
            del token[:]
        state.had_open = False
        state.comment = False
        state.string = False
        state.escape = False
        # state.pending = False

    for line in source.readlines():
        line = line.strip()
        for index, c in enumerate(line):
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
                # elif c == "#":
                #     state.pending = True
                elif c == '"':
                    state.string = True
                elif c == ";":
                    state.comment = True
                elif c == ")" or c == "]" or c == "}":
                    yield from flush()
                elif c == "#":
                    if not state.string:
                        try:
                            if line[index+1] in ['(',"[","{"]:
                                token.append(c) # really working?
                                continue
                        except:
                            pass
                elif c == "(" or c == "[" or c == "{":
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

# what is indentation?
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
                out.write(" ") # no need for this space? let's see.
                write(out, c, indent)
            if not isinstance(at, PairNode):
                if at.start[-1] in  ["(" ,"{", "["]:
                    # out.write(" ")
                    # do you want this space in empty brackets?
                    # maybe you want it.
                    ...
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
    dest = tempfile.NamedTemporaryFile(mode="wt")
    with dest:
    # dest = tempfile.NamedTemporaryFile(mode="wt", delete=False)
        if args.file:
            source = open(args.file, "rt")
            if args.inplace: # change the dest.
                pass
                # dest = tempfile.NamedTemporaryFile(mode="wt", delete=False)
            else:
                pass
                # dest = sys.stdout
        else:
            # pass
            source = sys.stdin
            # dest = sys.stdout
        # preprocess the source somehow. please.
        pre_1 = source.read()
        # code from useful_patterns

        pre_1, dataDict_1= useful_patterns(pre_1)
        import io
        source = io.StringIO(pre_1)


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
            elif any(t in token for t in ["{", "[", "("]):
                token_ = StructureNode(token)
                append(token_)
                tree.append(token_)
            elif any(t in token for t in ["}", "]", ")"]):
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
        # dest.name
        # operation not supported? wtf?
        # with tempfile.NamedTemporaryFile("w+") as dest2:
        with open(dest.name,'r') as f:
            data = f.read()
        lines = data.split('\n') # you might want not to run this against CRLF
        new_lines = []
        for index, line in enumerate(lines):
            try:
                index_before = lines[index-1].strip()
                index_after = lines[index+1].strip()
                stripped_line = line.strip()
                checkfunc = lambda l : l == "" or l.startswith(";") or (not (l.startswith("(def") or l.startswith("(if") or l.startswith("(when")))
                sig0 = checkfunc(index_before)
                sig1 = checkfunc(index_after)
                sig2 = stripped_line == ""
                sig3 = not (index_before.startswith(";") and (not index_after.startswith(";")))
                sig4 = not ((not index_before.startswith(";")) and index_after.startswith(";"))
                sig5 = not (index_before.count(")") == len(index_before))
                # print("STRIPPED_LINE:", [stripped_line])
                if sig0 and sig1 and sig2 and sig3 and sig4 and sig5:
                    continue
            except:
                # import traceback
                # traceback.print_exc()
                pass
            new_lines.append(line)
        new_data = "\n".join(new_lines)
        # do think about it twice.
        new_data = reparse_fix_code(new_data)
        new_data, dataDict_2 = final_fix(new_data)
        # use dataDict_1 to recover my strings.
        for key in dataDict_1.keys():
            if key.startswith("comment_"):
                new_data = new_data.replace(f";{key}", dataDict_1[key])
            elif key.startswith("string_"):
                new_data = new_data.replace(key, dataDict_1[key])

        if args.file and args.inplace:
            # shutil.move(dest.name, args.file)
            with open(args.file,'w+') as f:
                f.write(new_data)
        else:
            # print(";; FROM STDOUT")
            # not from stdout?
            print(new_data, end="")
            # print(";; FROM STDOUT")
