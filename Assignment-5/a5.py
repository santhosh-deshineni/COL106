# The implementation of heap using a python list
class Heap:
    
    # Initializing the heap with empty list
    def __init__(self):
        self.heap = []
        self.size = 0

    # Index of the parent of given node
    def parentindex(self,index):
        return (index-1)//2
    
    # Index of the left child of given node
    def leftchildindex(self,index):
        return (2*index)+1
    
    # Index of the right child of given node
    def rightchildindex(self,index):
        return (2*index)+2
    
    # Checking if a node has atleast one child or not
    def HasChild(self,index):
        if (index*2) + 1 > self.size - 1:
            return False
        return True
    
    # Getting the index of child with larger key of the two children
    def MaxChild(self,index):

        # Checking if there is only one child
        if (index*2 + 2 > self.size - 1):
            return (index*2) + 1
        
        # Comparing the keys of the two children
        else:
            leftindex = self.leftchildindex(index)
            rightindex = self.rightchildindex(index)
            if self.heap[leftindex][2] > self.heap[rightindex][2]:
                return leftindex
            else:
                return rightindex

    # Heapup to send the given index up to right place in heap
    def HeapUp(self,index):
        parentindex = self.parentindex(index)

        # Loop over and switch as long as parent key is smaller than key of current node
        while parentindex >= 0 and self.heap[parentindex][2] < self.heap[index][2]:

            # Switching the keys
            self.heap[index],self.heap[parentindex] = self.heap[parentindex],self.heap[index]

            # Changing node to the parent
            index = parentindex
            parentindex = self.parentindex(index)
    
    # Heapdown to send the given index down to right place in the heap
    def HeapDown(self,index):

        # Checking if the given node has a child
        if self.HasChild(index):
            maxchildindex = self.MaxChild(index)

            # Loop over as long as there is a child with larger key than given node
            while self.heap[maxchildindex][2] > self.heap[index][2]:

                # Switching the keys
                self.heap[index],self.heap[maxchildindex] = self.heap[maxchildindex],self.heap[index]

                # Switch if child exists else break the loop
                index = maxchildindex
                if self.HasChild(index):
                    maxchildindex = self.MaxChild(index)
                else:
                    break
    
    # Adding a node with given key to the heap
    def Enqueue(self,key):

        # Append to the list
        self.heap.append(key)
        self.size += 1
        index = (self.size) - 1

        # Heapup the added key to the right place
        self.HeapUp(index)

    # Extract the minimum for the heap maintaining its heap property
    def ExtractMax(self):

        # If size is 1 then just pop
        if self.size == 1:
            self.size = 0
            return self.heap.pop()

        # Disconnect last node and put its key at the root
        max = self.heap[0]
        x = self.heap.pop()
        self.size -= 1
        self.heap[0] = x

        # Heapdown the root to the right place
        self.HeapDown(0)
        
        return max
    
    # Change the key of a node to the new key and maintain heap property
    def ChangeKey(self,index,newkey):

        # Put given key in place of node
        currentkey = self.heap[index]
        self.heap[index] = newkey

        # Heap up or down to the right place
        if newkey[2] < currentkey[2]:
            self.HeapDown(index)
        if newkey[2] > currentkey[2]:
            self.HeapUp(index)

def findMaxCapacity(n,links,s,t):

    # Creating an adjacency list of the given graph using a 2-D list
    # Note that we generally use a linked list for this
    # However, since there is no deletion, we can use a list instead
    vertlist = []
    for i in range(n):
        vertlist.append([])

    # Adding the neighbours of each vertex in edge form
    # It is ensured that the current vertex is first in the corresponding edges added
    for edge in links:
        vertlist[edge[0]].append(edge)
        vertlist[edge[1]].append((edge[1],edge[0],edge[2]))
    
    # Initiate a max heap
    Maxheap = Heap()

    # Enqueue the immediate neighbours of s
    for i in vertlist[s]:
        Maxheap.Enqueue(i)
    
    # Create a list to keep track of the path followed from s to reach t
    prevlist = []
    for i in range(n):
        prevlist.append(None)

    # Keep extracting the max from the heap as long as it is not empty
    while (Maxheap.size > 0):
        max = Maxheap.ExtractMax()

        # If a previous already does not exist then add it
        if prevlist[max[1]] == None:
            prevlist[max[1]] = (max[0],max[2])
            
            # Enqueue the neighbours of the current vertex
            for i in vertlist[max[1]]:
                Maxheap.Enqueue(i)
            
        # Stop if the target router is reached
        if max[1] == t:
            break
    
    # We start at t and go backwards to generate the sequence and get the appropriate C
    currentvert = t
    C = prevlist[t][1]

    # A list to store the sequence of elements that form the path from s to t
    seqlist = [t]

    # Loop over to go backwards from t and reach s
    while True:

        # take minimum of current C and that of previous edge
        C = min(C,prevlist[currentvert][1])
        currentvert = prevlist[currentvert][0]
        seqlist.append(currentvert)
        if currentvert == s:
            break
    
    # Reverse to get the sequence in right order
    seqlist.reverse()

    return (C,seqlist)

def convert(list):
    return tuple(i for i in list)

f = open("./hidden_testcase_7.txt","r")
n = [int(x) for  x in next(f).split()]

links = []
for line in f:
    lst = [int(x) for x in line.split()]
    links.append(convert(lst))

s = links[-2]
t = links[-1]
n = n[0]
s = s[0]
t = t[0]
links.pop()
links.pop()
print(findMaxCapacity(n,links,s,t))