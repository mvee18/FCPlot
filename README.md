# FCPlot - Force Constant Plot

<b> Welcome to FC Plot! </b>

This program's purpose is to take the force constants / derivatives used by the program spectro, then to plot them as a
typical potential curve, which would allow us to extract the energies from the force constants without having to store them.

## Installation
Clone this folder to your computer using `git clone https://github.com/mvee18/FCPlot.git`.

The following are required:
- NumPy
- Pandas
- Python 3

## Usage
The test files for water are included in the "fort_files" directory. It is necessary to change the fort files in the directory to those of the molecule you are using. These are in the format for the inputs of the spectro program. (For further reference, consult *SPECTRO: A Theoretical Chemistry Package* Jan 1994.)

Once you have changed the above fort files to those of your molecule (including the top line!), you can then run the program by submitting the packaged fcplot.pbs file -- `qsub fcplot.pbs`. Its directives may need to be changed depending on the hardware or software requirements of your supercomputer. 

It can also be run locally though `python main.py -t local`, though at least 16 GB of RAM are necessary. Running the previous command without any arguments (or with any word other than "local") defaults to the supercomputer method.

## Output
The script will generate three files, each corresponding to the output for the second, third, and fourth derivatives (second.out, third.out, fourth.out). These will be a CSV containing its index, displacement, and the energy. 

### Example Ouput Energy
`0,"[4.0000000000 0.0000000000 0.0000000000 0.0000000000 0.0000000000, 0.0000000000 0.0000000000 0.0000000000 0.0000000000]",-76.3698395798804`

The first value, 0, means that this is the first energy ouput. 

The next nine values represent the three atoms of water in Cartesians in the following order: X1, Y1, Z1, X2, Y2, Z2, X3, Y3, Z3 ... Xn, Yn, Zn. Since water only has three atoms, the output ends at Z3. 

The final value is the corresponding energy for that displacement.

### Extraction
Extracting the list of energies can be done in one of two ways.
1. Using the bundled scanlines tool. Using the bundled tool will scan the output file and print the energies. Simply use `python scanlines.py [file]` to use it. To save the output, use `python scanlines.py [file] > [new_file]`

2. The regular expression -\d{2}\.\d+ will also yield the energies using a tool like grep. Using grep, you may wish to try something like `grep -P -- -\d{2}\.\d+ [file]` since the hyphen can interfere with the regex.

