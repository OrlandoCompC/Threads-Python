# Threads-Python
This program is an animal zoo where each time an anime gets hungry, it will eat the food that is available.
If the food is not available, it will wait until the food is available.
It will use threads to simulate the animals eating the food.
It will also use threads to increase the amount of food available until an animal can eat it.
It will also use classes to create the animals.

There is a function called slowPrint which prints the text slowly.
I use ansi escape sequences to color the text, this way its easier to read the output.

Imports are: threading, random, time

threading is used to create the threads
random is used to generate random numbers
time is used to make the program sleep for a certain amount of time
