# Biology- Hexagonal self organizing map (SOM)

#### Created by:
- Raviv Haham
- Peleg Haham

Project Description
-
In this project, we worked on several features:
We created a desktop application that runs the SOM algorithm on the election results (according to the input file we received which contains the election results in 197 cities).
We mapped the cities to the hexagonal SOM grid (which contains 61 cells), so at the end of the process each cell represents a number of cities.
In fact, the SOM network is a simple neural network that helps us to create mapping and division into groups (clustering).
This network relies on unsupervised learning and creates a mapping between a high dimension (of continuous) input to a low dimension (of discrete) output.
This network is the hexagonal SOM network and each cell in the beehive represents a node.
For each node (cell) we created the following features:
• A vector that initialized with random numbers that is associated with a cell in the hexagon.
• List of neighbors of the cell (node).
• Index that represents the current cell.

The different screens
-
The main screen has a graphic display which runs the SOM algorithm on the election results 10 times in a row (according to the input file we received), so that in each iteration the SOM board (the hexagon) containing 61 cells is displayed in the center of the screen (and at the end of running, each cell represents a number of cities).
Finally we presented the hexagon that represents the best solution.
![UML](https://imgur.com/VpORHu0.png)

You can see that in the best solution there is a clear division into colors, that describes the situation we expected to get: cities with same/similar socio-economic status often vote for the same parties (with the same ratio of voting). Since the vectors that represent these cities are similar, then their vectors mapping (to cells in the hexagon) are identical/adjacent, and thus we can see it visually.
We also added an information bar (in the upper right part of the screen) that explains what socio-economic status each color represents, so the user can understand the meaning of the output.
In addition, in the upper left part of the screen appears: the number of the solution (out of the 10 solutions), the distance of the best solution that was, the distance of the worst solution that was, and the average distance of all the solutions that were so far.
Also at the top of the screen you can see the iteration number. At the end of each iteration, we made sure that the board stops and displays the SOM in the center of the screen (so the user can see the path and not just the final result) and by pressing continue you can continue to the next iteration.
When the run is finished, a window opens with the graph that contains all 10 different runs of the SOM algorithm that we presented, when the average distance (of the data vectors from the vector of the cell to which they are mapped) is displayed per iteration.
![UML](https://imgur.com/7d3ETXi.png)




### Running
To run, enter to the folder that contains the main.exe executable file and the text file Elec_24.csv (which was provided to us), then click (double click) on the file: main.exe. A window will open that will display the 10 solutions of the hexagon board, and finally a graph will be displayed that describes the average distance, and the list of cities with their mapping will appear on the terminal page that opens automatically.



## Future improvements

As we continue to work on this app, we encourage anyone that wants to help out to do so!
Just open the project in Visual Studio Code and add your own touches!
Other than that, we would appreciate if you would try to stick to our design language and patterns.
Have fun with this project and don't forget to create a pull request once you're done so this project could have a little bit of YOU in it!






הקבצים כוללים את הקבצים עם הקוד עצמו, קובץ הרצה, והדוח המפורט.
