def Infix2Postfix(Infix):
    precedence = {'<=>': 1, '=>': 2, '&': 3, '|': 3, '~': 4}
    output = []
    stack = []

    i = 0
    while i < len(Infix):
        char = Infix[i]
        
        if char.isalpha():
            output.append(char)
            i += 1
        elif char == '(':
            stack.append(char)
            i += 1
        elif char == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()
            i += 1
        elif char in '~&|':
            while (stack and stack[-1] != '(' and 
                   precedence.get(stack[-1], 0) >= precedence.get(char, 0)):
                output.append(stack.pop())
            stack.append(char)
            i += 1
        elif char == '=' and i + 1 < len(Infix) and Infix[i + 1] == '>':
            op = '=>'
            while (stack and stack[-1] != '(' and 
                   precedence.get(stack[-1], 0) >= precedence.get(op, 0)):
                output.append(stack.pop())
            stack.append(op)
            i += 2
        elif char == '<' and i + 2 < len(Infix) and Infix[i + 1] == '=' and Infix[i + 2] == '>':
            op = '<=>'
            while (stack and stack[-1] != '(' and 
                   precedence.get(stack[-1], 0) >= precedence.get(op, 0)):
                output.append(stack.pop())
            stack.append(op)
            i += 3
        else:
            i += 1
    
    # Lấy hết toán tử còn lại trong stack
    while stack:
        output.append(stack.pop())
    
    return ''.join(output)

def Postfix2Truthtable(Postfix):
    # Tìm các biến trong biểu thức hậu tố
    variables = sorted(set([c for c in Postfix if c.isalpha()]))
    if not variables:
        return "Không tìm thấy biến"
    
    n = len(variables)
    combinations = [[(i >> j) & 1 for j in range(n-1, -1, -1)] for i in range(2**n)]
    
    # Khởi tạo bảng chân lý
    truth_table = []
    for combo in combinations:
        env = dict(zip(variables, combo))
        stack = []
        
        for char in Postfix:
            if char.isalpha():
                stack.append(env[char])
            elif char == '~':
                a = stack.pop()
                stack.append(1 - a)
            elif char == '&':
                # AND
                b, a = stack.pop(), stack.pop()
                stack.append(a & b)
            elif char == '|':
                # OR
                b, a = stack.pop(), stack.pop()
                stack.append(a | b)
            elif char == '=>':
                b, a = stack.pop(), stack.pop()
                stack.append((1 - a) | b)
            elif char == '<=>':
                b, a = stack.pop(), stack.pop()
                stack.append((a & b) | ((1 - a) & (1 - b)))
        
        row = combo + [stack.pop()]
        truth_table.append(row)
    
    header = variables + ['Kết quả']
    result = '\n'.join(['\t'.join(map(str, row)) for row in [header] + truth_table])
    return result

test_cases = [
    "P|(Q&R)",
    "~P|(Q&R)",
    "P|(R&Q)",
    "(P=>Q)&(Q=>R)",
    "(P<=>Q)=>~P"
]

for i, infix in enumerate(test_cases, 1):
    print(f"Test case {i}: {infix}")
    postfix = Infix2Postfix(infix)
    print(f"Biểu thức hậu tố: {postfix}")
    print("Bảng chân lý:")
    print(Postfix2Truthtable(postfix))
    print()