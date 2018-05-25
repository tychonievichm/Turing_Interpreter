# Turing Machine Interpreter

This is a prototype interpreter for a one-tape Turing machine, written in Python 2.7.  See test1.txt and test2.txt in the codes directory for sample Turing machine code files.  The main program is turing_gui.py.  To convert example code from turingmachinesimulator.com, save it as a text file and use the option in the GUI.  The code will be remade into a .tur file for you view with a text editor if you witness any unexpected behavior.

## What is a Turing Machine?

Alan Turing defined an automatic machine in his [1936 paper](https://www.cs.virginia.edu/~robins/Turing_Paper_1936.pdf).  In the present day, this model of a computer is typically called a Turing Machine.  In the code in thie repository, I refer to it as ``machine'' and hold all of the relevant information in the Machine class.

### A machine has the following parts:
* A finite-length tape, made up of a discrete number of cells in which symbols may be written.  Many of the cells are blank.
* A read/write head, that is cabaable of focusing on only one cell at a time.  It may read what is in the cell, and it may write any symbol into that cell.  The head is able to move to the left or to the right on the tape only one cell at a time.
* A finite and predetermined tape alphabet: a list symbols that determines what the read/write head will be able to read or write.  "Blank" is always part of this alphabet, and erasing the contents of the cell is the same as writing "blank".
* A finite list of machine states.  The machine's current state determines how it will react to whatever it is currently viewing.
* A program, or a list of instructions that tell the machine how to react to different combinations of states and read symbols.
* A special state that the machine is initialized with.
* A list of special states that the machine recognizes as good states for a computation to end in.  If the machine runs out of program in one of these states, then it will deliver its current tape as an output and say that the input given to it was accepted.  If the machine runs out of program in any other state, then it will say (at least) that the input was rejected.

### What is a program?
A program for a machine will be a list of instructions, each containing two "chunks" of information.
**Antecedent information:** this information is what the machine looks for when deciding what instruction to next execute.  It consists of a state name and a symbol that might be found on a tape.  Together, these form a key for a sort of code dictionary.  Each key should only show up in a program once, of the machine will not behave well!

**Consequent information:** this information tells the machine what it is to do once it has found the line of code corresponding to the antecedent key.  It consists of three separate pieces of information: a state name, a tape symbol, and a direction.  Upon determining what instruction to execute, the machine takes this information and performs the following actions:

* The read/write head writes the instructed symbol onto the current cell, overwriting whatever was there.
* The machine state changes to whatever state the instruction named.
* The read/write moves (or not) one cell to the right or one cell to the left as instructed.

If no entry in the code dictionary has the key made from the antecedent information, then the program stops and the machine produces output of some sort.

* If the final state was an "accepting" state, then the machine clips off any blank spaces at the ends of the the tape and delivers the result as output, stating that its input was accepted.
* Otherwise, the machine states that its input was rejected.

## Implementation
This implementation of the Turing machine uses a Python dictionary to hold code information that is read from a flat text file.  Instructions in such a file are written in a specified format; read test1.tur to see the format used.  The Machine object then steps through the code and updates a list of strings representing a tape.  Certain characters are reserved for use in the program: underscores are used for blank symbols, spaces are used as delimiters, and the hash symbol # is used to indicate comment lines in a code file.  Comments may also be placed after instructions, but this is not a good idea.  When the program is running, you can make the tape display in a console window, but I have provided a GUI to handle that instead.  To run the code with no fuss, turing_gui.py is the file you want to run, and it will link turing.py as a module.  The GUI code may create a codes directory to hold programs that it writes.

### Other implementations

Martin Ugarte's [turingmachinesimulator.com](https://turingmachinesimulator.com/) simulator works on code in a similar fashion to this one, and I have provided a method for translating code for that simulator into code for this one.  This translation will always produce a new code file to give you a chance to check for errors, which will sometimes be indicated by a # BAD LINE comment in the new file.

Anthony Morphett's [Turing machine simulator](http://morphett.info/turing/turing.html) is not compatible with this program due to its allowance of wildcard characters, which Turing's model does not support.  There is a [Github repo](https://github.com/awmorp/jsturing) for this simulator if you are insterested.
