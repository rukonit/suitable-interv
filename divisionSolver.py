# Variables

# Sample data: Please change the list based the division you want to solve
x = [[16,[8,2],4],2,80]

# List to hold breakdown of elements
y = []

# Recursive Method to breakdown and calculate nested items until the list beomes a plain list of elememts 
def resolveArray(input):
    
    for i in input:
        if type(i) is list:
            if len(i) == 2:
            
                y.append(i[0]/i[1])
            else:
                resolveArray(i)
        else:
            y.append(i)
    return y

# Method to calculate find result of division
def divisionSolver(input):

    k = resolveArray(input)
    result = k[0]
    for j in range(len(k)-1):
        result = result/k[j+1]
    return result

# Call the method and print the result
print("-------")
print('The result is: ' + str(divisionSolver(x)))