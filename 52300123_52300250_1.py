import itertools

precedence = {
    '~': 4,
    '&': 3,
    '|': 2,
    '>': 1,
    '=': 0
}

def Infix2Postfix(infix):
    stack = []
    output = ''
    for char in infix:
        if char.isalpha():
            output += char
        elif char == '(':
            stack.append(char)
        elif char == ')':
            while stack and stack[-1] != '(':
                output += stack.pop()
            stack.pop()
        else:
            while stack and stack[-1] != '(' and precedence[char] <= precedence.get(stack[-1], 0):
                output += stack.pop()
            stack.append(char)
    while stack:
        output += stack.pop()
    return output

def eval_postfix(expr, values):
    stack = []
    for token in expr:
        if token.isalpha():
            stack.append(values[token])
        elif token == '~':
            a = stack.pop()
            stack.append(not a)
        else:
            b = stack.pop()
            a = stack.pop()
            if token == '&':
                stack.append(a and b)
            elif token == '|':
                stack.append(a or b)
            elif token == '>':
                stack.append((not a) or b)
            elif token == '=':
                stack.append(a == b)
    return stack.pop()

def Postfix2Truthtable(postfix):
    variables = sorted(set(filter(str.isalpha, postfix)))
    print(" | ".join(variables) + " | Result")
    print("-" * (4 * len(variables) + 10))
    for combo in itertools.product([False, True], repeat=len(variables)):
        values = dict(zip(variables, combo))
        result = eval_postfix(postfix, values)
        row = " | ".join(str(int(values[v])) for v in variables)
        print(f"{row} |   {int(result)}")

if __name__ == "__main__":
    testcases = [
        "R|(P&Q)",
        "~P|(Q&R)>R",
        "P|(R&Q)",
        "(P>Q)&(Q>R)",
        "(P|~Q)>~P=(P|(~Q))>~P"
    ]
    for i, infix in enumerate(testcases, 1):
        print(f"\nTestcase {i}: {infix}")
        postfix = Infix2Postfix(infix)
        print("Postfix:", postfix)
        Postfix2Truthtable(postfix)
