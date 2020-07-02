lencheck = False
len_y = input("Input the length of the screen in pixels")
len_x = input("Input the width of the screen in pixels")
Bool_len_y = False
Bool_len_x =False
if len(maze) == len_y:
    Bool_len_y = True
else:
    print("Error, length of the outer list is incorrect"
for y in len(maze):
    if len(maze[y]) == len_x:
        Bool_len_x = True
        if Bool_len_x == False:
            print("Error, length of line", y+1,"is incorrect"

if Bool_len_y and Bool_len_x:
    lencheck = True
        
 
