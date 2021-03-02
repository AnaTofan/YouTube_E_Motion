from PIL import Image,ImageDraw
from math import  sqrt


class bicluster:
    def __init__(self,vec,left=None,right=None,distance=0.0,id=None):
        self.left=left
        self.right=right
        self.vec=vec
        self.id=id
        self.distance=distance


def readfile(filename):
    lines=[line for line in open(filename)]
# First line is the column titles
    colnames=lines[0].strip( ).split('\t')[1:]
    rownames=[]
    data=[]
    for line in lines[1:]:
        p=line.strip( ).split('\t')
        # First column in each row is the rowname
        rownames.append(p[0])
        # The data for this row is the remainder of the row
        data.append([float(x) for x in p[1:]])

    return rownames,colnames,data

def pearson_correlation(vb1,vb2):
    sum1=sum(vb1)
    sum2=sum(vb2)

    sum1Sq= sum([pow(w,2) for w in vb1])
    sum2Sq=sum([pow(w,2) for w in vb2])


    pSum=sum([vb1[i]*vb2[i] for i in range(len(vb1))])
    num=pSum-(sum1*sum2/len(vb1))


    den = sqrt((sum1Sq - pow(sum1, 2)/len(vb1)) * (sum2Sq - pow(sum2, 2)/len(vb1)))
    if den == 0: return 0
    return 1.0 - num/den


def printclust(clust, labels=None, n=0):

    # indent to make a hierarchy layout
    for i in range(n): print (' '),
    if clust.id<0:
        # negative id means that this is branch
        print ('-')

    else:

        if labels == None:print (clust.id)
        else: print (labels[clust.id])
        # now print the right and left branches
    if clust.left != None: printclust(clust.left, labels=labels, n=n + 1)
    if clust.right != None: printclust(clust.right, labels=labels, n=n + 1)

def hierarchical_clustering(rows,distance=pearson_correlation):
        distances={}
        currentclustid=-1
        # Clusters are initially just the rows
        cluster=[bicluster(rows[i],id=i) for i in range(len(rows))]
        while len(cluster)>1:
            lowestpair=(0,1)
            closest=distance(cluster[0].vec,cluster[1].vec)



            for i in range(len(cluster)):
             for j in range(i+1,len(cluster)):
        # distances is the cache of distance calculations
              if (cluster[i].id,cluster[j].id) not in distances:
                 distances[(cluster[i].id,clust[j].id)]=distance(cluster[i].vec,cluster[j].vec)
              d=distances[(cluster[i].id,cluster[j].id)]

              if d<closest:
                 closest=d
                 lowestpair=(i,j)
        # calculate the average of the two clusters
            mergevec=[
                (cluster[lowestpair[0]].vec[i]+cluster[lowestpair[1]].vec[i])/2.0
            for i in range(len(cluster[0].vec))]
        # create the new cluster
            newcluster=bicluster(mergevec,left=cluster[lowestpair[0]],
                             right=cluster[lowestpair[1]],
                             distance=closest,id=currentclustid)
        # cluster ids that weren't in the original set are negative
            currentclustid=-1
            del cluster[lowestpair[1]]
            del cluster[lowestpair[0]]
            cluster.append(newcluster)

        return cluster[0]

def getheight(clust):

     # Is this an endpoint? Then the height is just 1
        if clust.left == None and clust.right == None: return 1
        # Otherwise the height is the same of the heights of
        # each branch
        return getheight(clust.left) + getheight(clust.right)

def getdepth(clust):

        # The distance of an endpoint is 0.0
         if clust.left == None and clust.right == None: return 0
        # The distance of a branch is the greater of its two sides
        # plus its own distance
         return max(getdepth(clust.left), getdepth(clust.right)) + clust.distance

def drawdendrogram(clust, labels, jpeg='clusters.jpg'):

            # height and width
            h = getheight(clust) * 20
            w = 1200
            depth = getdepth(clust)
            # width is fixed, so scale distances accordingly
            scaling = float(w - 150) / depth-43
            # Create a new image with a white background
            img = Image.new('RGB', (w, h), (255, 255, 255))
            draw = ImageDraw.Draw(img)
            draw.line((0, h / 2, 10, h / 2), fill=(255, 0, 0))
            # Draw the first node
            drawnode(draw, clust, 10, (h / 2), scaling, labels)
            img.save(jpeg, 'JPEG')

def drawnode(draw,clust,x,y,scaling,labels):
    if clust.id<0:
        h1=getheight(clust.left)*20
        h2=getheight(clust.right)*20
        top=y-(h1+h2)/2
        bottom=y+(h1+h2)/2
        # Line length
        ll=clust.distance*scaling
        # Vertical line from this cluster to children
        draw.line((x,top+h1/2,x,bottom-h2/2),fill=(255,0,0))
        # Horizontal line to left item
        draw.line((x,top+h1/2,x+ll,top+h1/2),fill=(255,0,0))
        # Horizontal line to right item
        draw.line((x,bottom-h2/2,x+ll,bottom-h2/2),fill=(255,0,0))
        # Call the function to draw the left and right nodes
        drawnode(draw, clust.left, x + ll, top + h1 / 2, scaling, labels)
        drawnode(draw, clust.right, x + ll, bottom - h2 / 2, scaling, labels)
    else:
        # If this is an endpoint, draw the item label
        draw.text((x + 5, y - 7), labels[clust.id], (0, 0, 0))

def rotatematrix(data):
    newdata=[]
    for i in range(len(data[0])):
        newrow=[data[j][i] for j in range(len(data))]
        newdata.append(newrow)
    return newdata


