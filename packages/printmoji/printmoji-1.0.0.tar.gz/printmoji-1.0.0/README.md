# printmoji

## Description

A simple package to format text in the terminal with emojis rather than ANSI codes or HTML tags.


## Installation

`pip install printmoji`

## Usage

### Coloring

Use the following emojis to color your text:

- 🟥 - <span style="color: rgb(239, 51, 77);">Red</span>
- 🟧 - <span style="color: rgb(6, 180, 120);">Orange</span>
- 🟨 - <span style="color: rgb(17, 138, 178);">Yellow</span>
- 🟩 - <span style="color: rgb(255, 209, 102);">Green</span>
- ⏹ - <span style="color: rgb(170, 74, 178);">Cyan</span>
- 🟦 - <span style="color: rgb(108, 200, 230);">Blue</span>
- 🟪 - <span style="color: rgb(255, 127, 17);">Magenta</span>
- ⬜ - <span style="color: rgb(255, 255, 255);">White</span>
- ⬛ - <span style="color: rgb(255, 255, 255);">Black</span>
- ❎ - Reset

I know what you're thinking: "How do I type emojis on the computer? This seems really inconvenient". Stop that.

Press `Win+.` on Windows or `Ctrl+Cmd+Space` on Mac to open the emoji keyboard. Type "square" and these emojis will show up.

```python
from printmoji import print

print("🟦Hello 🟥world!")
```

Outputs:
<p style="color: rgb(108, 200, 230);">Hello <span style="color: rgb(239, 51, 77);">world!</span></p>

### Indentation

The print function returns a context manager that will indent all text printed within it.

```python
from printmoji import print

with print("Parent"):
    print("Hello")
    print("World")

with print('Parent', indent='  | '):
    print('Pipes!')
    print('More pipes!')

print.indent()
print('Indented manually')
print.dedent()
print('Dedented manually')
```

Outputs:
```
Parent
    Hello
    World

Parent
  | Pipes!
  | More pipes!

    Indented manually
Dedented manually
```

There is an optional `close` argument that will print a character after the block is closed. This is useful for creating tree structures.

```python
from printmoji import print

with print('Grandparent', close='---\n'):
    with print('Parent', close='+++\n'):
        print('Child')
```

Outputs:
```
Grandparent
    Parent
        Child
    +++
---
```
