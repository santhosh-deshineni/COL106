# The implementation of class for each node in a linked list
class Node:
    
    # Initializes node with a value and next pointing to None
    def __init__(self,value):
        self.value = value
        self.next = None

# The implementation of class for stack using linked list
class Stack:

    # Initializes head of linked list
    def __init__(self):
        self.head = None

    # Checks if the stack is empty or not
    def is_empty(self):
        if self.head == None:
            return True
        return False

    # Pushes a new element into the stack
    def push(self,value):
        if self.is_empty():
            self.head = Node(value)
        else:
            newnode = Node(value)
            newnode.next = self.head
            self.head = newnode
    
    # Removes top element from stack and returns it
    def pop(self):
        if self.is_empty():
            return None
        oldnode = self.head
        self.head = self.head.next
        oldnode.next = None

        return oldnode.value

    # Returns the top element of stack without removing it
    def top(self):
        if self.is_empty():
            return None
        return self.head.value

# This is the implementation of the function for finding final coordinates and distance of drone
# It is based on storing the value of [x,y,z,d,multiplier] in a stack
# It is similar to recursion
# This is because each element of the stack represents a layer of variables
def findPositionandDistance(P):

    # Initialize coordinates of drone and multiplier to 1
    x,y,z,d = 0,0,0,0
    multiplier = 1

    # Create a new stack
    stack = Stack()

    # Find length of string and create i to keep track of character in string
    length = len(P)
    i = 0

    # While loop to iterate over the input string P
    while (i < length):
        # If character is '+' then increase distance and coordinate accordingly
        if P[i] == '+':
            d += 1
            if P[i+1] == 'X':
                x += 1
            elif P[i+1] == 'Y':
                y += 1
            else:
                z += 1
            i += 2
        
        # If character is '-' then increase distance and decrease coordinate accordingly
        elif P[i] == '-':
            d += 1
            if P[i+1] == 'X':
                x -= 1
            elif P[i+1] == 'Y':
                y -= 1
            else:
                z -= 1
            i += 2

        # If character is ')' then we pop the stack and update variables
        # We pop the stack in order to go back to the previous layer of variables
        elif P[i] == ')':
            tup = stack.pop()
            x = tup[0] + multiplier*x
            y = tup[1] + multiplier*y
            z = tup[2] + multiplier*z
            d = tup[3] + multiplier*d
            multiplier = tup[4]  
            i += 1

        # Observe that if the character is not any of the above then it must be an int
        # This is because of the way the while loop is set up
        # It cannot be 'X','Y' or 'Z' because they must be preceded by a '+' or '-'
        # It also cannot be a '(' because it must also be preceded by an int
        # In this case, we must create a new layer of variables
        # We do this by pushing into stack and reinitializing variables
        else:
            stack.push([x,y,z,d,multiplier])
            x,y,z,d = 0,0,0,0
            alpha = ''
            while P[i] != '(':
                alpha += P[i]
                i += 1
            i += 1
            multiplier = int(alpha)
    
    # We return a list of the final coordinates and distance travelled
    return [x,y,z,d]