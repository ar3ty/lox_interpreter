A Python and C implementation of the Lox language, from the in-progress book [Crafting Interpreters](https://craftinginterpreters.com/) by [Bob Nystrom](https://github.com/munificent).

Interpreter developed in Python 3.12+ for educational purposes, using Python as Java replacement due to familiarity. 
The consequential compiler implementation is in C for **gcc** 13.3.0. Also, small pretty framework for unittests in C is built.
Workspace is Ubuntu 13.3.0 on WSL2.

Execution of pylox: **python3 pylox/pylox.py [path to the input.txt]** or **python3 pylox/pylox.py** (for REPL mode)
Execution of clox (for my convenience): **./buildclox_execute.sh** for auto building and consequential clox/input.txt execution. REPL mode is also available, build only **clox** and proceed with **./clox**

As expected, **test_clox.sh** and **text_pylox.sh** are for autotesting.