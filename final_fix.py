import re
import sys

data = sys.stdin.read()
# mcode = code.split('\n')
dataDict = {}
comments=r";.*"
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
print(data)