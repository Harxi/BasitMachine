# BasitMachine (First version)
## Description
This is a virtual machine with its own Bas1x architecture, it reads the json tree.

## Installation linux

This is a mini-guide on how to install BasitMachine on linux
To begin with, we will install Python

```sh
apt install python3
```

after installing Python3, we will install pip.

```sh
apt install python3-pip
```

Good! Now clone the repository.
```sh
apt install git
git clone https://github.com/Harxi/BasitMachine
```
 and go to the directory of the virtual machine
```sh
cd BasitMachine
```

What's next? Then you can change the configuration, write to BasitMachineAssambler, whatever.

## BMASM Guide

| Register | Bit |
|----------|-----|
| `chr`    | `8` |
| `op`     | `8` |
| `ret`    | `8` |
| `p`      | `8` |
| `sp`     | `8` |
| `oth`    | `8` |
| `flags`  | `3` |

| Flag | Bit |
|------|-----|
| `eq` | `1` |
| `gt` | `1` |
| `lt` | `1` |

| Instruction          | Opernads                                                    | Example        | Description                                                                                                                                                      |   
|----------------------|-------------------------------------------------------------|----------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `mov`                | `<Register, address>`, `<Register, address, char, integer>` | `mov a, b`     | Move `b` to `a`                                                                                                                                                  |   
| `push`               | `<Register, char, integer>` (pushes multiple elements)      | `push a, b, c` | pushes elements `a, b, c` in stack                                                                                                                               |   
| `pop`                | `<Register>`                                                | `pop a`        | pop element to `a` from stack                                                                                                                                    |   
| `cmp`                | `<Register, char, integer>`, `<Register, char, integer>`    | `cmp a, b`     | compares `a` and `b` by setting flags depending on the result                                                                                                    |   
| `ret`                | `<Register, char, integer>`                                 | `ret a`        | set register ret, equal `mov ret, a`                                                                                                                             |   
| `goto`               | `<Register, char, integer>`, `<Register, char, integer>`    | `goto a, b`    | repeats the token with index `a`, `b` times, if it is a negative number, then infinitely                                                                         |   
| `j(mp/eq/neq/gt/lt)` | `<Point>`                                                   | `jmp a`        | executes the code in the label, `jeq` if the flag `eq` is true, `jneq` if the flag `eq` is false, `jgt` if the flag `gt` is true, `jlt` if the flag `lt` is true |
| `add`                | `<Register>`, `<Register, char, integer>`                   | `add a, b`     | add `b` to `a`                                                                                                                                                   |
| `set`                | `<Flag>`, `<Register, char, integer>` (only 1 or 0)         | `set a, b`     | set flag `a` with value `b`                                                                                                                                      |
| `int`                | `<Register, char, integer>`                                 | `int a`        | call the `a` interrupt                                                                                                                                         |
