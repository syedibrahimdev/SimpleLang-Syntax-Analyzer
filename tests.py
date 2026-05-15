from tokenizer import tokenize
from parser import Parser

# === Test Case ===
code = """
int x;
bool flag;
x = 10;
flag = true;

if (x > 5) {
    x = x - 1;
}

for (int i; i < 3; i = i + 1) {
    x = x + i;
}
"""

try:
    tokens = tokenize(code)
    parser = Parser(tokens)
    parser.parse()
    print("✅ Parsing successful: Code is valid.")
except SyntaxError as e:
    print("❌ Syntax Error:", e)
except RuntimeError as e:
    print("❌ Tokenization Error:", e)
