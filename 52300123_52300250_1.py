def Infix2Postfix(Infix):
    # Độ ưu tiên của toán tử
    precedence = {'<=>': 1, '=>': 2, '&': 3, '|': 3, '~': 4}
    # Khởi tạo output và stack
    output = []
    stack = []
    
    i = 0
    while i < len(Infix):
        char = Infix[i]
        
        if char.isalpha():
            # Nếu là biến (A-Z), thêm vào output
            output.append(char)
            i += 1
        elif char == '(':
            # Đẩy dấu ngoặc mở vào stack
            stack.append(char)
            i += 1
        elif char == ')':
            # Lấy ra cho đến khi gặp '('
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()  # Xóa '('
            i += 1
        elif char in '~&|':
            # Xử lý toán tử đơn (~) hoặc nhị phân (&,|)
            while (stack and stack[-1] != '(' and 
                   precedence.get(stack[-1], 0) >= precedence.get(char, 0)):
                output.append(stack.pop())
            stack.append(char)
            i += 1
        elif char == '=' and i + 1 < len(Infix) and Infix[i + 1] == '>':
            # Xử lý toán tử '=>'
            op = '=>'
            while (stack and stack[-1] != '(' and 
                   precedence.get(stack[-1], 0) >= precedence.get(op, 0)):
                output.append(stack.pop())
            stack.append(op)
            i += 2
        elif char == '<' and i + 2 < len(Infix) and Infix[i + 1] == '=' and Infix[i + 2] == '>':
            # Xử lý toán tử '<=>'
            op = '<=>'
            while (stack and stack[-1] != '(' and 
                   precedence.get(stack[-1], 0) >= precedence.get(op, 0)):
                output.append(stack.pop())
            stack.append(op)
            i += 3
        else:
            i += 1  # Bỏ qua ký tự không hợp lệ
    
    # Lấy hết toán tử còn lại trong stack
    while stack:
        output.append(stack.pop())
    
    return ''.join(output)

def Postfix2Truthtable(Postfix):
    # Tìm các biến trong biểu thức hậu tố
    variables = sorted(set([c for c in Postfix if c.isalpha()]))
    if not variables:
        return "Không tìm thấy biến"
    
    # Sinh tất cả tổ hợp giá trị chân lý
    n = len(variables)
    combinations = [[(i >> j) & 1 for j in range(n-1, -1, -1)] for i in range(2**n)]
    
    # Khởi tạo bảng chân lý
    truth_table = []
    for combo in combinations:
        # Gán giá trị chân lý cho biến
        env = dict(zip(variables, combo))
        stack = []
        
        # Đánh giá biểu thức hậu tố
        for char in Postfix:
            if char.isalpha():
                # Đẩy giá trị chân lý của biến
                stack.append(env[char])
            elif char == '~':
                # Phủ định
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
                # Ngụ ý (A => B tương đương ~A | B)
                b, a = stack.pop(), stack.pop()
                stack.append((1 - a) | b)
            elif char == '<=>':
                # Tương đương (A <=> B tương đương (A & B) | (~A & ~B))
                b, a = stack.pop(), stack.pop()
                stack.append((a & b) | ((1 - a) & (1 - b)))
        
        # Thêm kết quả vào bảng chân lý
        row = combo + [stack.pop()]
        truth_table.append(row)
    
    # Định dạng output
    header = variables + ['Kết quả']
    result = '\n'.join(['\t'.join(map(str, row)) for row in [header] + truth_table])
    return result

test_cases = [
    "P|(Q&R)",          # Test case 1
    "~P|(Q&R)",         # Test case 2
    "P|(R&Q)",          # Test case 3
    "(P=>Q)&(Q=>R)",    # Test case 4
    "(P<=>Q)=>~P"       # Test case 5
]

for i, infix in enumerate(test_cases, 1):
    print(f"Test case {i}: {infix}")
    postfix = Infix2Postfix(infix)
    print(f"Biểu thức hậu tố: {postfix}")
    print("Bảng chân lý:")
    print(Postfix2Truthtable(postfix))
    print()