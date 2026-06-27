<div align="center">

# 🔤 SimpleLang Syntax Analyzer

**A hand-built recursive descent parser and tokenizer for a custom programming language — validates source code against a formal EBNF grammar.**

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Compiler Theory](https://img.shields.io/badge/Compiler-Theory-success?style=for-the-badge)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

[📂 Source Code](https://github.com/syedibrahimdev/SimpleLang-Syntax-Analyzer) · [🐛 Report Bug](https://github.com/syedibrahimdev/SimpleLang-Syntax-Analyzer/issues)

</div>

---

## 🧐 What Is This?

Every compiler starts the same way: turning raw text into tokens, then validating that those tokens form a grammatically correct program. This project implements both stages from scratch in Python — a **tokenizer (lexer)** using regex-based pattern matching, and a **recursive descent parser** that walks the token stream and enforces SimpleLang's grammar rules.

No parser-generator libraries (no PLY, no ANTLR) — every rule is hand-written, which is exactly what makes this a strong demonstration of actually understanding compiler theory rather than just using a tool.

---

## 📐 SimpleLang Grammar (EBNF)

```ebnf
program        := { statement }

statement      := variable_decl
                | assignment
                | if_statement
                | for_loop

variable_decl  := TYPE ID [ "=" expression ] ";"
assignment     := ID "=" expression ";"

if_statement   := "if" "(" expression ")" "{" { statement } "}"

for_loop       := "for" "(" variable_decl expression ";"
                   ID "=" expression ")" "{" { statement } "}"

expression     := simple_expression [ COMPARE simple_expression ]
simple_expression := term { OP term }
term           := NUMBER | ID | "(" expression ")"

TYPE           := "int" | "bool" | "string"
COMPARE        := "==" | "!=" | "<=" | ">=" | "<" | ">"
OP             := "+" | "-" | "*" | "/" | "&&" | "||"
```

> **Design note:** the `for` loop's update clause (`i = i + 1`) is parsed without a trailing semicolon before the closing `)` — this required custom handling in `for_loop()` since reusing the standard `assignment()` rule would have demanded an extra `;` that doesn't belong in a C-style for-loop header.

---

## 🏗️ How It Works — Two Stages

### Stage 1: Tokenizer (`tokenizer.py`)

Converts raw source code into a stream of `Token(type, value, line)` objects using a single combined regex with named groups. Each token type is matched in priority order — critically, `COMPARE` (`==`, `<=`, etc.) is checked **before** `ASSIGN` (`=`) and `OP`, so multi-character operators aren't accidentally split.

Input:  x = 10;

Tokens: [Token(ID, 'x', 1), Token(ASSIGN, '=', 1), Token(NUMBER, '10', 1), Token(END, ';', 1)]

Whitespace is silently skipped, newlines increment the line counter (for accurate error reporting), and any unrecognized character raises an immediate `RuntimeError`.

### Stage 2: Parser (`parser.py`)

A **recursive descent parser** — each grammar rule becomes a method (`statement()`, `expression()`, `term()`, etc.) that consumes tokens via `eat(token_type)`. If the next token doesn't match what the grammar expects, it raises a `SyntaxError` with the exact line number and the token that was found instead.
statement()

→ variable_declaration() | assignment() | if_statement() | for_loop()

→ expression()

→ simple_expression()

→ term()

---

## 💻 Sample Input / Output

### ✅ Valid Program

**Input:**
```c
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
```

**Output:**
✅ Parsing successful: Code is valid.

---

### ❌ Invalid Program — Missing Semicolon

**Input:**
```c
int y
y = 3;
```

**Output:**
❌ Syntax Error: Expected END at line 2, found ID (y)

---

### ❌ Invalid Program — Malformed Expression

**Input:**
```c
int x;
x = (1 + ) 2;
```

**Output:**
❌ Syntax Error: Invalid term at line 2

---

### ❌ Invalid Program — Unclosed Block

**Input:**
```c
int x;
if (x > 0) {
    x = x + 1;
```

**Output:**
❌ Syntax Error: Expected RBRACE at line 4, found EOF

---

## 📁 Project Structure
SimpleLang-Syntax-Analyzer/

│

├── main.py            # CLI entry point — run built-in demo or pass a file

├── tokenizer.py        # Lexer: source code → token stream

├── parser.py           # Recursive descent parser: validates grammar

├── sample_code.txt     # Example programs (valid + invalid cases)

└── README.md

---

## 🚀 Getting Started

```bash
# 1. Clone the repo
git clone https://github.com/syedibrahimdev/SimpleLang-Syntax-Analyzer.git
cd SimpleLang-Syntax-Analyzer

# 2. No dependencies needed — pure Python stdlib

# 3. Run the built-in demo
python main.py

# Or run against a custom source file
python main.py sample_code.txt
```

---

## 🔧 Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.9+ (stdlib only — `re`) |
| Lexing | Regex-based tokenizer with named capture groups |
| Parsing | Hand-written recursive descent (no parser generators) |
| Concepts | EBNF grammar design, lookahead parsing, error recovery |

---

## 🗺️ Roadmap

- [x] Tokenizer with line tracking
- [x] Recursive descent parser for declarations, assignments, if, for
- [x] Detailed syntax error messages with line numbers
- [ ] Add `while` loop support
- [ ] Add string literal support
- [ ] Build an Abstract Syntax Tree (AST) instead of just validation
- [ ] Add a simple interpreter to actually execute valid programs

---

## 🤝 Contributing

Pull requests are welcome. For major changes, open an issue first to discuss what you'd like to change.

---

## 👨‍💻 Author

**Syed Ibrahim Ahmed**
[![GitHub](https://img.shields.io/badge/GitHub-syedibrahimdev-181717?style=flat&logo=github)](https://github.com/syedibrahimdev)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=flat&logo=linkedin)](https://linkedin.com/in/syedibrahimdev)

---

<div align="center">
  <sub>Built to understand how compilers actually read your code</sub>
</div>