import math


# SET INDEX
# 0 = left bot | 1 = bot | 2 = right bot | 3 = left | 4 = center
# 5 = right | 6 = left top | 7 = top | 8 = right top
index = 0


def printMatrix4(matrix):
    # Only for scripting. Print Matrix4 in Script Editor
    row = '| ' + 4 * '{: .4f} ' + '|'
    print()
    print(row.format(matrix[0], matrix[4], matrix[8], matrix[12]))
    print(row.format(matrix[1], matrix[5], matrix[9], matrix[13]))
    print(row.format(matrix[2], matrix[6], matrix[10], matrix[14]))
    print(row.format(matrix[3], matrix[7], matrix[11], matrix[15]))


def getMatrixFromNode(node):
    # Get Matrix4 from node
    try:
        nodeMatrix = nuke.math.Matrix4()
        if 'world_matrix' in [k for k in node.knobs()]:
            knobname = 'world_matrix'
        elif 'matrix' in [k for k in node.knobs()]:
            knobname = 'matrix'
        else:
            raise NameError
 
        for x in range(node[knobname].width()):
            for y in range(node[knobname].height()):
                nodeMatrix[x*4+y] = node[knobname].value(y,x)

    except (NameError, AttributeError):
        nuke.message('No matrix found')
        nodeMatrix.makeIdentity()

    return nodeMatrix


def movePivotToAxis(selNode, newPivot=nuke.math.Vector3()):
    # variables
    oldTranslate = nuke.math.Vector3(selNode['translate'].x(), selNode['translate'].y(), selNode['translate'].z())
    oldPivot = nuke.math.Vector3(selNode['pivot'].x(), selNode['pivot'].y(), selNode['pivot'].z())
    oldLocalTranslate = -oldPivot
    oldGlobalPivot = oldTranslate + oldPivot

    # get matrix from node
    m1 = getMatrixFromNode(selNode)

    # get localTranslate
    oldFullGlobalTranslate = m1.transform(oldLocalTranslate)   
    oldFullGlobalTranslate = oldFullGlobalTranslate + oldGlobalPivot                    
    localTranslate = oldFullGlobalTranslate - newPivot
  
    # inverse node matrix
    m1 = m1.inverse()

    # multiply matrix to localTranslate and get new Vector3 value
    localTranslate = m1.transform(localTranslate)
   
    # set position and pivot values to card
    selNode['translate'].setValue(newPivot+localTranslate)    
    selNode['pivot'].setValue(-localTranslate)     

def getCardPointsDefaultPosition(oldCard):
    # Function creates card, find default corner position
    # and return sorted Vector3 values of corners

    card = nuke.nodes.Card(rows=2, columns=2)

    card['image_aspect'].setValue(1)
    card.setInput(0, oldCard.dependencies()[0])

    geoNode = nuke.nodes.PythonGeo(inputs=[card])
    points = geoNode['geo'].getGeometry()[0].points()

    points_sorted = []
    for i in range(0, len(points), 3):
        v = nuke.math.Vector3(points[i], points[i+1], points[i+2])
        points_sorted.append(v)

    nuke.delete(card)
    nuke.delete(geoNode)

    return points_sorted


def getPoints(card, index):
    # Get points position of Card3 according to Card3 Matrix4
    # card = node Card3 | index = which corner of Card3 get

    # pos = it is default position of all Card3 corners
    # starting with left bot to right top including center
    
    pos = getCardPointsDefaultPosition(card)

    # get card Matrix4
    matrix = getMatrixFromNode(card)

    # transform pos according to the Card3 Matrix4 and return new Vector3 value
    return matrix.transform(pos[index])
    
nodes = []
for i in nuke.selectedNodes():
    nodes.append(i)

for node in nodes:
    movePivotToAxis(node, getPoints(node, index))
