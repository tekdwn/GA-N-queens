To use our program N-Queen-Solver you can do it in two ways

First, you have to execute this command : 

pip install -r .\requirements.txt

Then, just go in the folder path and double click on the .exe program. (It will takes 20/30 s to open the first time)

Else, just run the command :

python .\N-Queen-Solver.py

To run the python file correctly, you have to be on windows for the window size of the graphical application. On linux or macOS, you will have a window of 1500 * 1200 with bad graphic visual.

Explanation of our program :

You will have a first tab, with 3 textboxes, "Board size", "Mutation rate" and "Maximum generation". You have to write a value (all the intervals in the values are written on the label) and then click the button "Start algorithm".
When you click that button, you will see few seconds after clicking it(depending on the board size chosed) the board displayed with all the queens correctly positionned as red tales or white and black tales for the positions without a queen.
In parralel, we did a log file that contains all the statistics about those run on the program called "stats.csv". This file is used on the second tab of our program.
When you click the button "Go other page". There will be another page with three textboxes here. You can write in those textboxes the values you want do to statistics with. If you did not do any algorithm computing with those 3 parameters that you set in textboxes, you will have an error message. If you don't have the stats.csv file, you will have an error too. Else, you will see the time and generation where you found the solution mean of all your computations with those parameters.

Since genetic algorithm have much random, sometimes you will have in the stats.csv really irrelevants statistics, we call those abberations. The remove_aberration.py file is the program that will remove those and create a .csv file without those aberations if you want clean values to make some computing, just execute this command :

python .\remove_aberration.py
