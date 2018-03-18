"""
Merge function for 2048 game.
"""

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    line_result = []
    result = []
    merged = False
    for entry in line:
        if entry != 0:
            line_result.append(entry)
        
    while len(line_result) != len(line):
        line_result.append(0)
        
    for number in range(len(line_result) - 1):
        if line_result[number] == line_result[number + 1] and merged == False:
            result.append(line_result[number] * 2)
            merged = True
        elif line_result[number] != line_result[number + 1] and merged == False:
            result.append(line_result[number])
        elif merged == True:
            merged = False
    
    if line_result[-1] != 0 and merged == False:
        result.append(line_result[-1])
            
    while len(result) != len(line_result):
        result.append(0)
    
    print line_result
    print result
    return result
LINEA = [5,6,6]
merge(LINEA)
