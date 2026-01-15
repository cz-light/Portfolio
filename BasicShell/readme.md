Background:
- BasicShell is a simple Unix-like command-line shell implemented in C. It supports basic command execution, directory navigation, input/output redirection, and background processing.
- The project was completed as part of a systems programming class to gain hands-on experience with process management and system calls in Unix-like operating systems.



Features:
- Execute standard shell commands (e.g., ls, ps)
- Change directories with cd
- Input (<) and output (>) redirection
- Run processes in the background using &
- Graceful exit with exit

To run the shell:
- Compile the C code using gcc:
  ```bash
  gcc -o basicshell basicshell.c
  ```
- Run the shell:
  ```bash
  ./basicshell
  ```