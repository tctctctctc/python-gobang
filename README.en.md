# python-gobang

## Background  
  This project is a Gobang game just after learning Python socket.  
  This project is implemented with pyGame and socket, which is divided into server and client part,and can be played by two people in LAN.  
  In the windows environment, it runs normally after many tests.   
  [Zh Version](README.md)
      
## Main ideas

- LAN

For the local area network function, first establish a connection (TCP), and then send the coordinates of the pieces to the opponent each time they play chess.  
When the coordinate is received, it is instantiated into a chess sub object.  
The select function is used when receiving, because pyGame needs to render images in a loop, so it needs to receive messages in a non blocking way.

The select function provides the fd_set data structure, which is actually an array of long type.Each array element can be associated with an open file handle(Whether it's a socket handle, or another file or named pipe or device handle).  
The job of establishing a connection is done by the programmer,When select() is called, the kernel modifies the value of fd_set according to the IO state,Thus, the process that executed the select() is informed which socket or file is readable or writable.  
It is mainly used in socket communication.


- Player vs Computer

The idea of computer combat is also very simple. It should be the most common and simplest method.  
It is to cycle through each point of the chessboard, judge the value of the point, and select the point with the greatest value.This requires a certain understanding of Gobang's form. Here are some common types of chess(Agreement 1 is your chess piece,2 is the opponent's pieces,0 is empty)

    "Live 4"(011110)：At this time, the four pieces are connected, and the two ends are empty, which can not prevent one side from winning. At this time, the value should be set to the highest.
    "Death 4"(011112|10111|11011)：Among the four pieces, only one place can connect five pieces into a line. One's own chess pieces can win, and the other's can prevent the other from winning. At this time, the value is the second highest.
    ......
In this way, judge each type of chess and get the value of the point.  
When the computer chooses the position of the drop, it needs to traverse the chessboard twice to get the maximum value of attack and defense.


## Game screenshot
![](https://github.com/tctctctctc/python-/raw/master/resouse/a.png)
  
## License
  [Apache-2.0 License](LICENSE)

