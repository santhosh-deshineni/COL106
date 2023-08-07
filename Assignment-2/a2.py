# The implementation of heap using a python list
class Heap:
    
    # Initializing the heap with empty list and a tracker for collisions
    def __init__(self,numofblocks):
        self.heap = []
        self.size = 0
        self.tracker = []
        for i in range(numofblocks-1):
            self.tracker.append(i)

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
    
    # Getting the index of child with smaller key of the two children
    def MinChild(self,index):

        # Checking if there is only one child
        if (index*2 + 2 > self.size - 1):
            return (index*2) + 1
        
        # Comparing the keys of the two children
        else:
            leftindex = self.leftchildindex(index)
            rightindex = self.rightchildindex(index)
            if self.heap[leftindex] < self.heap[rightindex]:
                return leftindex
            else:
                return rightindex

    # Heapup to send the given index up to right place in heap
    def HeapUp(self,index):
        parentindex = self.parentindex(index)

        # Loop over and switch as long as parent key is greater than key of current node
        while self.heap[parentindex] > self.heap[index] and parentindex >= 0:
            colnum = self.heap[index][1]
            parentcolnum = self.heap[parentindex][1]

            # Switching the keys and the tracker
            self.heap[index],self.heap[parentindex] = self.heap[parentindex],self.heap[index]
            self.tracker[colnum],self.tracker[parentcolnum] = self.tracker[parentcolnum],self.tracker[colnum]

            # Changing node to the parent
            index = parentindex
            parentindex = self.parentindex(index)
    
    # Heapdown to send the given index down to right place in the heap
    def HeapDown(self,index):

        # Checking if the given node has a child
        if self.HasChild(index):
            minchildindex = self.MinChild(index)

            # Loop over as long as there is a child with smaller key than given node
            while self.heap[minchildindex] < self.heap[index]:
                colnum = self.heap[index][1]
                childcolnum = self.heap[minchildindex][1]

                # Switching the keys and the tracker
                self.heap[index],self.heap[minchildindex] = self.heap[minchildindex],self.heap[index]
                self.tracker[colnum],self.tracker[childcolnum] = self.tracker[childcolnum],self.tracker[colnum]

                # Switch if child exists else break the loop
                index = minchildindex
                if self.HasChild(index):
                    minchildindex = self.MinChild(index)
                else:
                    break
    
    # Adding a node with given key to the heap
    def Enqueue(self,key):

        # Append to the list and update tracker
        self.heap.append(key)
        self.size += 1
        index = (self.size) - 1
        self.tracker[key[1]] = index

        # Heapup the added key to the right place
        self.HeapUp(index)

    # Extract the minimum for the heap maintaining its heap property
    def ExtractMin(self):

        # If size is 1 then just pop
        if self.size == 1:
            return self.heap.pop()

        # Disconnect last node and put its key at the root
        min = self.heap[0]
        x = self.heap.pop()
        self.size -= 1
        self.heap[0] = x

        # Update the tracker
        self.tracker[x[1]] = 0
        self.tracker[min[1]] = None

        # Heapdown the root to the right place
        self.HeapDown(0)
        
        return min
    
    # Change the key of a node to the new key and maintain heap property
    def ChangeKey(self,index,newkey):

        # Put given key in place of node
        currentkey = self.heap[index]
        self.heap[index] = newkey

        # Heap up or down to the right place
        if newkey > currentkey:
            self.HeapDown(index)
        if newkey < currentkey:
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

# The function that returns a list of the collisions in chronological order
# Note that it takes care of two collisions at same time
# This is because python compares tuples lexicographically
# So a block to right is chosen later than a block to the left with lower index
def listCollisions(M,v,x,m,T):

    # initialize time and number of collisions
    currenttime = 0
    currentcol = 0
    n = len(M)
    listofcols = []

    # fill the above list with all the current possible collisions
    # Fill with (T,i,0) if the blocks are moving away from each other
    # This cannot happen in time T which is the limit
    for i in range(0,n-1):
        if v[i+1] - v[i] < 0:
            time = abs((x[i+1]-x[i])/(v[i+1]-v[i]))
            pos = x[i] + v[i]*time
            listofcols.append((time,i,pos))
        else:
            listofcols.append((T,i,0))
    
    # Convert the above list into a heap
    colsheap = Heap(n)
    colsheap.BuildHeap(listofcols)

    # This is the list to be returned containing the collisions in order
    collisionlist = []

    # The formula for velocities after an elastic collision
    def velchanger(i):
        v[i],v[i+1] = ((M[i]-M[i+1])*v[i] + 2*M[i+1]*v[i+1])/(M[i]+M[i+1]), ((M[i+1]-M[i])*v[i+1] + 2*M[i]*v[i])/(M[i]+M[i+1])

    # If the heap is empty then there are no collisions
    if not colsheap.heap:
        return []
    
    # A list to maintain the time of last collision of each block
    lastcoltimelist = [0]*n

    collision = colsheap.ExtractMin()

    # loop as long as collisions is less than m and final time is less than T
    while (currentcol < m) and (collision[0] < T):
        
        # Round to 4 digits and append collision tuple to final list
        roundedtuple = (round(collision[0],4),round(collision[1],4),round(collision[2],4))
        collisionlist.append(roundedtuple)

        # Increase the time and count of collisions
        currentcol += 1
        currenttime = collision[0]

        # update the positions and velocities of colliding blocks
        index = collision[1]
        velchanger(index)
        x[index],x[index+1] = collision[2],collision[2]

        # Update last collision time of colliding blocks
        lastcoltimelist[index] = currenttime
        lastcoltimelist[index+1] = currenttime

        # Since the blocks move away from each other after collision we enqueue this
        colsheap.Enqueue((T,index,0))
        
        # If there is a block to the left of colliding blocks
        if index - 1 >= 0:

            # current position of block at index-1
            currentpos = x[index-1] + (currenttime-lastcoltimelist[index-1])*v[index-1]

            # Update the collision tuple of blocks at index and index-1
            if v[index] - v[index-1] < 0:
                extratime = abs((x[index]-currentpos)/(v[index]-v[index-1]))
                finaltime = extratime + currenttime
                finalpos = currentpos+extratime*v[index-1]
                colsheap.ChangeKey(colsheap.tracker[index-1],(finaltime,index-1,finalpos))
            else:
                colsheap.ChangeKey(colsheap.tracker[index-1],(T,index-1,0))

        # If there is a block to the right of colliding blocks
        if index + 2 <= n-1:

            # current position of block at index+2
            currentpos = x[index+2] + (currenttime-lastcoltimelist[index+2])*v[index+2]

            # Update the collision tuple of blocks at index+1 and index+2
            if v[index+2] - v[index+1] < 0:
                extratime = abs((currentpos-x[index+1])/(v[index+2]-v[index+1]))
                finaltime = extratime + currenttime
                finalpos = currentpos + extratime*v[index+2]
                colsheap.ChangeKey(colsheap.tracker[index+1],(finaltime,index+1,finalpos))
            else:
                colsheap.ChangeKey(colsheap.tracker[index+1],(T,index+1,0))

        # Update collision to the next one
        collision = colsheap.ExtractMin()
    
    return collisionlist
        
#l=listCollisions([100000, 1, 100000, 1, 100000], [0, -2.3, 0, -2.5, 0], [0, 10, 20, 30, 40], 100, 100.0)
l=listCollisions([23, 44, 77], [-2.5, 3, 6], [10, 20, 30], 200, 200.0)

print(l)



