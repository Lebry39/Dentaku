ops = ["+", "-", "*", "/", ")", "(", "^"]
ops_p = {"+": 1, "-": 1, "*": 2, "/": 2, ")": 0, "(": 3, "^": 3}

def syntax_analysis(src):
    tokens = []
    cnt = 0
    is_first = True

    # cntはlen(src)-1まで
    while len(src)-1 >= cnt:
        s = src[cnt]
        cnt += 1

        # 空白を飛ばす
        if s == " ":
            continue

        if s in ops and not (is_first and s == "-"):
            # 演算子(初めの"-"は含まない)
            tokens.append(s)
        else:
            # 数字だった
            num = s

            # 次の演算子まで読む
            while len(src)-1 >= cnt:
                s = src[cnt]  # 数字

                # 空白を飛ばす
                if s == " " or s in ops:
                    break
                else:
                    cnt += 1
                    num += s

            tokens.append(num)

        if s == "(":
            is_first = True
        else:
            is_first = False

    assert tokens[-1] == ")" or not tokens[-1] in ops  # Last No Ops

    return tokens

def parser(src):
    parserd = []
    stack = []
    pris = []
    bias = 0

    def pop(op, stack, pris):
        op_p = ops_p[op] + bias
        out = [s for s, p in zip(reversed(stack), reversed(pris)) if p >= op_p]
        stack = [s for s, p in zip(stack, pris) if p < op_p]
        pris = [p for p in pris if p < op_p]
        return out, stack, pris

    for token in src:
        if token in ops:
            res, stack, pris = pop(token, stack, pris)
            parserd += [r for r in res if not r in ["(", ")"]]

            if token == "(":
                bias += 3
            elif token == ")":
                bias -= 3
            stack.append(token)
            pris.append(ops_p[token] + bias)
        else:
            parserd.append(token)

    parserd += [s for s in reversed(stack) if not s in ["(", ")"]]

    assert bias == 0  # () Okashi

    return parserd

def to_num(str):
    # 返還済み
    if isinstance(str, int) or isinstance(str, float):
        return str

    is_negative = False
    if str[0] == "-":
        is_negative = True
        str = str[1:]

    frac = 0
    if "." in str:
        frac = str.split(".")[1]
        str = str.split(".")[0]
        frac = [(ord(c) - ord("0"))/(10**(i+1)) for i, c in enumerate(frac)]
        frac = sum(frac)

    nums = [(ord(c) - ord("0"))*(10**i) for i, c in enumerate(reversed(str))]

    res = sum(nums) + frac
    if is_negative:
        res *= -1
    return res

def stack_machine(src):
    stack = []
    for token in src:
        # 演算子
        if token in ops:
            if token == "+":
                stack[-2] = to_num(stack[-2]) + to_num(stack[-1])
            if token == "-":
                stack[-2] = to_num(stack[-2]) - to_num(stack[-1])
            if token == "*":
                stack[-2] = to_num(stack[-2]) * to_num(stack[-1])
            if token == "/":
                stack[-2] = to_num(stack[-2]) / to_num(stack[-1])
            if token == "^":
                stack[-2] = to_num(stack[-2]) ** to_num(stack[-1])
            stack[-2] = stack[-2]
            del stack[-1]
        else:
            stack.append(token)

        # print(token, stack)

    return stack

def test():
    formulas = ["3^5 /(-3* (-4+ 1))", "(12*6-(-1-1-5*(6/(5-3)*6)+2)+5)-3"]
    ans = [27, 164]

    for x, y in zip(formulas, ans):
        res = syntax_analysis(x)
        res = parser(res)
        res = stack_machine(res)
        print(x, "=", res[0], "(%s)" % y)
        assert res[0] == y
    print("ok")

def main():
    # src = "3^2 /(-2* (4+ 6))"

    src = input(">>")
    # print("Source :", src)
    try:
        res = syntax_analysis(src)
        # print("Syntax :", res)

        res = parser(res)
        # print("Parser :", res)

        res = stack_machine(res)
        print("=",res[0])
        # print("Answer :", res)
    except:
        print("Error...")

if __name__ == '__main__':
    while True:
        main()
