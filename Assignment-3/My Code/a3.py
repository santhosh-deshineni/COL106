from cmath import inf

# A class for a tree representing the recursive structure of merge sort
class TreeNode:
    def __init__(self,data,leftnode,rightnode,xrange):
        self.left = leftnode
        self.right = rightnode
        self.data = data
        self.xrange = xrange
    
# Function to merge two sorted lists
def merge (l1, l2):

    retval = []
    idx_l1 = 0
    idx_l2 = 0
    while idx_l1 < len(l1) and idx_l2 < len(l2):
        if (l1[idx_l1][1] < l2[idx_l2][1]):
            retval.append(l1[idx_l1])
            idx_l1 += 1
        else:
            retval.append(l2[idx_l2])
            idx_l2 += 1
    
    while idx_l1 < len(l1):
        retval.append(l1[idx_l1])
        idx_l1 += 1

    while idx_l2 < len(l2):
        retval.append(l2[idx_l2])
        idx_l2 += 1

    return retval
    
# Function to build a Y-sorted tree based on merge sort
def buildtree(inputlist):
    
    length = len(inputlist)

    if length >= 2:
        leftlist = inputlist[:length//2]
        rightlist = inputlist[length//2:]
        lefttree = buildtree(leftlist)
        righttree = buildtree(rightlist)

        minofx = min(lefttree.xrange[0],righttree.xrange[0])
        maxofx = max(lefttree.xrange[1],righttree.xrange[1])

        return TreeNode(merge(lefttree.data,righttree.data),lefttree,righttree,(minofx,maxofx))
    
    return TreeNode(inputlist,None,None,(inputlist[0][0],inputlist[0][0]))

# Function to search where q lies with respect to a list a
# q is the lower bound on Y
def minSearch(a,q):
    if len(a) == 0:
        return -inf

    i = 0
    j = len(a)-1

    mid = (i+j+1)//2

    if a[mid][1] == q:
        return mid
    elif a[mid][1] > q:
        if mid == 0:
            return mid
        elif a[mid-1][1] == q:
            return mid-1
        elif a[mid-1][1] < q:
            return mid
        else:
            return minSearch(a[:mid], q)
    else:
        if mid == j:
            return -inf
        elif a[mid+1][1] >= q:
            return mid+1
        else:
            return mid+minSearch(a[mid:], q)

# Function to search where q lies with respect to a list a
# q is the upper bound on Y
def maxSearch(a,q):
    if len(a)==0:
        return -inf
    
    i = 0
    j = len(a)-1

    mid=(i+j+1)//2

    if a[mid][1] == q:
        return mid
    elif a[mid][1] > q:
        if mid == 0:
            return -inf
        elif a[mid-1][1] <= q:
            return mid-1
        else:
            return maxSearch(a[:mid], q)
    else:
        if mid == j:
            return j
        elif a[mid+1][1] > q:
            return mid
        elif a[mid+1][1] == q:
            return mid+1
        else:
            return mid+maxSearch(a[mid:], q)
    

# A function that allows us to check whether a node in the tree is completely contained in feasible interval
# If not then we recurse on its child nodes
def searchNearby_recur(root,q,d):
    outputlist = []

    if root == None:
        return []

    elif root.xrange[0] >= q[0]-d and root.xrange[1] <= q[0]+d:
        a = minSearch(root.data,q[1]-d)
        b = maxSearch(root.data,q[1]+d)
        if a == -inf or b == -inf or a > b:
            return []
        for i in range(a,b+1):
            outputlist.append(root.data[i])
            
    elif (q[0]-d <= root.xrange[0] <= q[0]+d and root.xrange[1] > q[0]+d) or (q[0]-d <= root.xrange[1] <= q[0]+d and root.xrange[0] < q[0]-d) or (root.xrange[0] < q[0]-d and root.xrange[1] > q[0]+d):
        out1 = searchNearby_recur(root.left,q,d)
        out2 = searchNearby_recur(root.right,q,d)
        outputlist.extend(out1)
        outputlist.extend(out2)
    return outputlist

# The class to be implemented with an init and searchNearby
class PointDatabase:

    def __init__(self, pointlist):
        # Sorting pointlist based on X
        pointlist.sort()
        self.segmenttree = buildtree(pointlist)

    def searchNearby(self, q, d):
        return searchNearby_recur(self.segmenttree,q,d)