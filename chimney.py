
"""
Assignment: Heat Transfer Hw.7 Chimney Problem
Name: Roman Hunter
Date: 2/29/24
"""
import copy

# define given constants
hi = 85; # W/m^2-C
ho = 10; # W/m^2-C
k = 3.1; # W/m-C
Ti  = 380+273; # C
To = 25+273; # C
delX = 0.01; # m
run = 0;
iter = 0

# initialize temperature array and names array to track derivations needed
rows, cols = (8, 11)
arr = [[273 for i in range(cols)] for j in range(rows)]
arrNam = [["NA" for i in range(cols)] for j in range(rows)]
rowsf, colsf = (16, 22);
arrf = [[0 for i in range(colsf)] for j in range(rowsf)]

# initialize the names array and the temperature array
def initialize():
    #print("initialize T_inf");
    for cols in range(5):
        for rows in range(2):
            arr[rows][cols] = Ti;
    for cols in range(11):
            arr[7][cols] = To;
    for rows in range(8):
        arr[rows][10] = To;
    #print("initialize node type matrix");
    for cols in range(5):
        for rows in range(2):
            arrNam[rows][cols] = "hInf";
    for cols in range(11):
            arrNam[7][cols] = "lInf";
    for rows in range(8):
        arrNam[rows][10] = "lInf";
    for rows in range(6):
        arrNam[rows][9] = "cas3";
    for cols in range(9):
        arrNam[6][cols] = "cas3";
    arrNam[6][9] = "cas4";
    arrNam[2][5] = "cas2";
    for cols in range(5):
        arrNam[2][cols] = "cas3";
    for rows in range (2):
        arrNam[rows][5] = "cas3";
    for cols in range(11):
        for rows in range(8):
            if (arrNam[rows][cols] == "NA"):
                arrNam[rows][cols] = "cas1";

# iterate every node using name array to decide what equations to use
def changeTemps():
    global arrOld
    # save copy of Temp array to compare for error function
    arrOld = copy.deepcopy(arr)
    #print('Iterate over entire array');
    for rows in range(8):
        for cols in range(11):
            global run;
            run = run + 1;
            #print(str(run) + " Row " + str(rows) + " Col " + str(cols));
            if (arrNam[rows][cols] == "hInf"):
                continue
                #print("break hInf");
            elif (arrNam[rows][cols] == "lInf"):
                continue
                #print("break lInf");
            elif (arrNam[rows][cols] == "cas1"):
                case1(rows, cols);
            elif (arrNam[rows][cols] == "cas2"):
                case2(rows, cols);
            elif (arrNam[rows][cols] == "cas3"):
                case3(rows, cols);
            elif (arrNam[rows][cols] == "cas4"):
                case4(rows, cols);

# derivations - some include edge case functions that also determine orientation
def case1(rows, cols):
    rowsm, rowsp, colsm, colsp = edgeCase1(rows, cols)
    num = (arr[rows][colsp] + arr[rows][colsm] + arr[rowsp][cols] + arr[rowsm][cols]);
    den = 4;
    arr[rows][cols] = round(num / den, 6);
    #print(f"{run} case1 {rows} {cols} {arr[rows][cols]}")
    return

def case2(rows, cols):
    rowsm, rowsp, colsm, colsp = edgeCase1(rows, cols);
    num = (2*(arr[rows][colsp] + arr[rowsm][cols]) + (arr[rows][colsm] + arr[rowsm][cols]) + (2*(hi*delX/k))*arr[rowsm][colsm]);
    den = (2*((3 + hi*delX/k)));
    arr[rows][cols] = round(num / den, 6);
    #print(f"{run} case2 {rows} {cols} {arr[rows][cols]}")
    return

def case3(rows, cols):
    a, b, c, Tinf, he = edgeCase3(rows, cols)
    num = (2*b + a + c) + ((2*he*delX/k) * Tinf);
    #print(num);
    den = (2*(((he*delX)/k) + 2));
    #print(den);
    arr[rows][cols] = round(num / den, 6);
    #print(f"{run} case3 {rows} {cols} {arr[rows][cols]}")
    return

def case4(rows, cols):
    num = (arr[rows][cols-1] + arr[rows-1][cols] + 2*ho*delX/k);
    #print(num);
    den = (2*((hi*delX/k) + 1));
    #print(den);
    arr[rows][cols] = round(num / den, 6);
    #print(f"{run} case4 {rows} {cols} {arr[rows][cols]}")
    return

# edge case function for case3
def edgeCase3(rows, cols):
    global To, Ti;
    rowsm, rowsp, colsm, colsp = edgeCase1(rows, cols);
    #print('edgeCase3');
    if (arrNam[rowsm][cols] == "hInf" or arrNam[rowsm][cols] == "lInf"):
        #print('edge1');
        a = arr[rows][colsm];
        b = arr[rowsp][cols];
        c = arr[rows][colsp];
        Tinf = arr[rowsm][cols];
        if (arrNam[rowsm][cols] == "hInf"):
            he = hi;
        else:
            he = ho;
        #print(str(a) + " " + str(b) + " " + str(c) + " " + str(he));
    elif (arrNam[rowsp][cols] == "hInf" or arrNam[rowsp][cols] ==  "lInf"):
        #print('edge2');
        a = arr[rows][colsp];
        b = arr[rowsm][cols];
        c = arr[rows][colsm];
        Tinf = arr[rowsp][cols];
        if (arrNam[rowsp][cols] == "hInf"):
            he = hi;
        else:
            he = ho;
        #print(str(a) + " " + str(b) + " " + str(c) + " " + str(he));
    elif (arrNam[rows][colsm] == "hInf" or arrNam[rows][colsm] ==  "lInf"):
        #print('edge3');
        a = arr[rowsp][cols];
        b = arr[rows][colsp];
        c = arr[rowsp][cols];
        Tinf = arr[rows][colsm];
        if (arrNam[rows][colsm] == "hInf"):
            he = hi;
        else:
            he = ho;
        #print(str(a) + " " + str(b) + " " + str(c) + " " + str(he));
    elif (arrNam[rows][colsp] == "hInf" or arrNam[rows][colsp] ==  "lInf"):
        #print('edge4');
        a = arr[rowsm][cols];
        b = arr[rows][colsm];
        c = arr[rowsp][cols];
        Tinf = arr[rows][colsp];  
        if (arrNam[rows][colsp] == "hInf"):
            he = hi;
        else:
            he = ho;
    return a, b, c, Tinf, he;

# edge case function for case 1
def edgeCase1(rows, cols):
    rowsp = rows + 1;
    rowsm = rows - 1;
    colsp = cols + 1;
    colsm = cols - 1;
    if (rowsp > 8):
        rowsp = rows;
    if (rowsm < 0):
        rowsm = rows;
    if (colsp > 11):
        colsp = cols;
    if (colsm < 0):
        colsm = cols;
    return rowsm, rowsp, colsm, colsp;

# this reflects array to show complete temperatures for chimney
def mirrorXY():
    for cols in range(11):
        for rows in range(8):
            arrf[rows+8][cols+11] = round(arr[rows][cols])-273; 
            arrf[rows][cols] = round(arr[7-rows][10-cols])-273;
            arrf[rows][cols+11] = round(arr[7-rows][cols])-273;
            arrf[rows+8][cols] = round(arr[rows][10-cols])-273;

# returns true if there is still error over 1e-6
def error():
    for cols in range(11):
        for rows in range(8):
            if (arrNam[rows][cols] != "hInf" and arrNam[rows][cols] != "lInf"):
                if (arr[rows][cols] > (arrOld[rows][cols] + .000001)):
                    #print(abs(arr[rows][cols]) - abs(arrOld[rows][cols]));
                    return True
    return False

initialize()

# iterate calling changeTemps() until error() returns false, track iterations
while True:
    changeTemps()
    iter += 1  # Update the iteration count
    if not error():
        break
    
for row in arrNam:
    print(row)

mirrorXY();

for rowsf in arrf:
    print(rowsf);
    
print("Final Iteration Count: " + str(iter));