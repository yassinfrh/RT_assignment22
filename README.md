
# Python Robotics Simulator Assignment

Farah Yassin 4801788

## Assignment

Using the robot simulator provided by the professor, it is asked to write a python code to make the robot arrange the silver boxes, initially positioned at the center of the map, next to the golden boxes, as shown in the figures.

![Initial arrangement](begin.png)

![Final arrangement](end.png)

## Pseudocode

The content of the code is described by the following pseudocode:

    while true:
        look for silver token
        if not found:
            turn around
            continue
        if dist > threshold or robot not aligned:
            approach token
        else:
            grab token
            save silver token ID in list
            while true:
                look for golden token
                if not found:
                    turn around
                    continue
                if dist > threshold or robot not aligned:
                    approach token
                else:
                    release token
                    save golden token ID in list
                    break
            if number of silver tokens arranged = 6
                exit
                
## How to run the code

To run the code, simply write the following command in the terminal:

    $ python2 run.py assignment.py

## Possible improvements

1. Pair each silver token with the actually closest golden token and not just with the first golden token it finds.
2. Avoid bumping into other tokens while delivering one
3. Exit the program without knowing a priori the number of tokens to arrange
