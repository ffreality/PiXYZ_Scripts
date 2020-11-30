#------------------------------------------------------------------------------------------------------
#	Python script for optimizing mesh locations and pivots for VR.
# Script and API developed by PiXYZ Software - 2019 and edited by Frozen Forest Reality Technologies
#
#	This Python script is meant to be used in PiXYZ STUDIO 2019
#	Open the script in STUDIO Script window, and click the Execute button (CTRL+E)
#
#	Copyright PiXYZ Software - 2019
#------------------------------------------------------------------------------------------------------

# SCRIPT 1 = MOVE ROOT TO CENTER OF SCENE

# Editable Section. You can define your scale in here.
SCALE = 1   # Set the scale of your model

# PiXYZ script. Please do not edit.
aabb = scene.getAABB([scene.getRoot()])
print(aabb)
centerX = (aabb[1][0] + aabb[0][0])/2
centerY = (aabb[1][1] + aabb[0][1])/2
centerZ = (aabb[1][2] + aabb[0][2])/2
translationMatrix = [[1, 0, 0, -centerX],
                     [0, 1, 0, -centerY],
										 [0, 0, 1, -centerZ],
										 [0, 0, 0, 1]]
for child in scene.getChildren(scene.getRoot()):
	scene.applyTransformation(child, translationMatrix)
	
scaleMatrix = [[SCALE, 0, 0, 0],
              [0, SCALE, 0, 0],
							[0, 0, SCALE, 0],
							[0, 0, 0, 1]]
for child in scene.getChildren(scene.getRoot()):
	scene.applyTransformation(child, scaleMatrix)

#------------------------------------------------------------------------------------------------------
# SCRIPT 2 = MOVE PIVOTS EACH OBJECTS CENTER

# PiXYZ script. Please do not edit.
def aabbCenter(aabb):
	minCorner = aabb[0]
	maxCorner = aabb[1]
	center = [(maxCorner[0] + minCorner[0]) * 0.5,
            (maxCorner[1] + minCorner[1]) * 0.5,
						(maxCorner[2] + minCorner[2]) * 0.5]
	return center	

def subPoints(pt1, pt2):
	return [pt1[0] - pt2[0], pt1[1] - pt2[1], pt1[2] - pt2[2]]

def constructTranslationMatrix(translation):
	return [
		[1,0,0, translation[0]],
		[0,1,0, translation[1]],
		[0,0,1, translation[2]],
		[0,0,0, 1             ]
	]

def movePivotToCenterRecursively(occurrence, parentPivot):
	aabb = scene.getAABB([occurrence])
	pivot = aabbCenter(aabb)	
	if scene.hasComponent(occurrence, scene.ComponentType.Part):
		parentOcc = scene.getParent(occurrence)
		tmpAssy = scene.createOccurrence("tmp")
		scene.setParent(occurrence, tmpAssy)
		translation = constructTranslationMatrix([-pivot[0], -pivot[1], -pivot[2]])
		core.setProperty(occurrence, "Transform", str(translation))
		scene.resetTransform(tmpAssy)
		scene.setParent(occurrence, parentOcc)
		core.deleteEntities([tmpAssy])
	print(pivot, parentPivot)
	translation = subPoints(pivot, parentPivot)
	matrix = constructTranslationMatrix(translation)	
	
	for child in scene.getChildren(occurrence):
		movePivotToCenterRecursively(child, pivot)
	
	core.setProperty(occurrence, "Transform", str(matrix))
	
scene.resetTransform(scene.getRoot())
movePivotToCenterRecursively(scene.getRoot(), [0,0,0])

#------------------------------------------------------------------------------------------------------
# SCRIPT 3 = CREATE HIERARCHY XML

# Editable Section. You can define your XML location in here. Please do not use C:/ (Root Only)
# Sample path = C:/Users/UserName/Desktop/assembly_name_hierarchy.xml
FILE_PATH = 'D:/test.xml'

# PiXYZ script. Please do not edit.
componentsTypeAndNames=[[scene.ComponentType.InteractionBehavior, "InteractionBehavior"],[scene.ComponentType.Light, "Light"],[scene.ComponentType.PMI, "PMI"],[scene.ComponentType.Part, "Part"],[scene.ComponentType.VisualBehavior, "VisualBehavior"]]

core.removeConsoleVerbose(core.Verbose.INFO)

def writeLine(file, type, parameters, values, indent):
	line = ('  ' * indent) + '<' + type
	nParameters = len(parameters)
	for i in range(nParameters):
		parameter = parameters[i]
		value = values[i]
		line = line + ' ' + parameter + '=\"' + value + '\"'
	line = line + '>\n'
	file.write(str(line))
	
def endLine(file, type, indent):
	line = ('  ' * indent) + '</' + type + '>\n'
	file.write(str(line))
	
	
def parseTree(node, file, level):
	type = core.getEntityTypeString(node)
	name = scene.getNodeName(node)
	
	attributes = ['Name']
	attributesValues = [name]
	
	for componentType,componentName in componentsTypeAndNames:
		attributes.append("has" + componentName + "Component")
		attributesValues.append(str(scene.hasComponent(node, componentType)))
	
	writeLine(file, type, attributes, attributesValues, level)
	for child in scene.getChildren(node):
		parseTree(child, file, level+1)
	endLine(file, type, level)

def main(filePath):
	root = scene.getRoot()
	with open(filePath, 'w') as file:
		parseTree(root, file, 0)
	print('\nDone: structure tree exported at ' + filePath)

main(FILE_PATH)

core.addConsoleVerbose(core.Verbose.INFO)
#------------------------------------------------------------------------------------------------------