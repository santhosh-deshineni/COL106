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
        while self.heap[parentindex][2] < self.heap[index][2] and parentindex >= 0:

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

    # Efficient way to build a heap from a list L
    def BuildHeap(self,L):
        self.heap = L
        self.size = len(L)
        x = self.size - 1

        # Heapdown backwards to make the heap
        while x >= 0:
            self.HeapDown(x)
            x -= 1