import sys
from getch import getch
'''
import getch to take single character input without printing in console.
pip install py-getch to use this Module
[DISCLAIMER]:
    The name of import changes from time to time..
    So If There's Any Change 
'''

# List of symbols in BrainF*ck
SYMBOLS=[",",".",">","<","[","]","+","-"]

def Execute(filename):
    '''
    Reads The File And Filters Out The Symbols In The Code and Ignore Other Text Like Comments.
    Only the symbols involved in BrainF*ck Languages are taken into consideration.
    After filtering the code, it is then evaluated inside the Evaluate() function
    '''
    with open(filename,"r") as f:
        code=list(filter(lambda c: True if c in SYMBOLS else False,f.read()))
    ProcessCode(code)

def ProcessCode(code):
    '''
    This Functions iterates over the code,
    performing appropriate functions depending on the symbol.
    '''
    # Look At Docstring of CreateBracketDicts(code) First to Get A Better Idea Of How It Works..
    beginsAt,endsAt=CreateBracketDicts(code)
    codeptr,cellptr,cells=0,0,[0]
    while codeptr<len(code):
        c=code[codeptr]
        print(c,end="")
        if c==">":
            cellptr+=1
            # Handling List Index From Getting Out Of Range By Adding New Cell with Value 0
            if cellptr==len(cells):
                cells.append(0)
        elif c=="<":
            cellptr=cellptr-1 if cellptr>0 else 0
        elif c=="+":
            # ASCII Values Range From 0 to 127 Only 
            # But We Are Handling Unicode Characters as well
            # making it a range of 256 characters(0 to 255)
            cells[cellptr]=cells[cellptr]+1 if cells[cellptr]<255 else 0
        elif c=="-":
            # ASCII Values Range From 0 to 127 Only 
            # But We Are Handling Unicode Characters as well
            # making it a range of 256 characters(0 to 255)
            cells[cellptr]=cells[cellptr]-1 if cells[cellptr]>0 else 255
        elif c==",":
            cells[cellptr]=ord(getch())
        elif c==".":
            sys.stdout.write(chr(cells[cellptr]))
        elif c=="[" and cells[cellptr]==0:
            # If The Value At Current Cell Becomes 0(False) , 
            # Break The Loop by reaching at the Closing Bracket
            codeptr=endsAt[codeptr]
        elif c=="]" and cells[cellptr]!=0:
            # If The Value At Current Cell Becomes 0(False) ,
            # Do Not Go Back To Opening Bracket And Continue...
            # Else Go Back To Opening Bracket And Iterate. 
            codeptr=beginsAt[codeptr]

        codeptr+=1

def CreateBracketDicts(code):
    '''
    Creates Two Dictionaries:
    1.beginsAt={}
        Stores Closing Bracket Index as key and its correspondig Opening Bracket Index as value
        beginsAt[CloseIndex] returns its Opening Bracket Index
    2.endsAt={}
        Stores Opening Bracket Index as key and its correspondig Closing Bracket Index as value
        beginsAt[OpenIndex] returns its Closing Bracket Index

    And Finally Returns These Dictionaries
    '''
    beginsAt={}
    endsAt={}
    tempBraceIndex=[]
    for index,c in enumerate(code):
        if c=="[":
            tempBraceIndex.append(index)
        if c=="]":
            OpenBraceIndex=tempBraceIndex.pop()
            beginsAt[index]=OpenBraceIndex
            endsAt[OpenBraceIndex]=index
    return beginsAt,endsAt

def main():
    if len(sys.argv)==2:
        Execute(sys.argv[1])
    else:
        sys.stderr.write("\n[FATAL ERROR] No Input File Given.\n")
if __name__ == "__main__":
    main()