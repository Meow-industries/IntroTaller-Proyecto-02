"""
0 == Water
1 == OurBoats 
-1 == EnemyBoat
3 == Debris
5 == X (Miss attack)
4.1 == PlaneUp
4.2 == PlaneDown
4.3 == PlaneRight
4.4 == PlaneLeft
7 == Limit
9.1 == arrowUp
9.2 == arrowDown
9.3 == arrowRight
9.4 == arrowLeft

"""

playerAtPc =    [[7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], 
                 [7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7], 
                 [7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7], 
                 [7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7], 
                 [7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7], 
                 [7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7], 
                 [4.3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 7], 
                 [7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 7], 
                 [7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 7], 
                 [7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 7], 
                 [7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 7], 
                 [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]]

pcAtPlayer =    [[7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], 
                 [7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7], 
                 [7, 0, 0, 0, -1, 0, 0, -1, 0, -1, 0, 7], 
                 [7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7], 
                 [7, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 7], 
                 [7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7], 
                 [7, 0, 0, 0, -1, 0, 0, 0, -1, 0, 0, 7], 
                 [7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7], 
                 [7, 0,-1, 0, 0, 0, 0, 0, 0, 0, 0, 7], 
                 [7, 0, 0, 0, -1, -1, -1, -1, 0, 0, 0, 7], 
                 [7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7], 
                 [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]]