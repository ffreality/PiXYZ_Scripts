#--------------------------------------------------------
#   Export Hierarchy with JSON Format Script for PiXYZ Studio
#
#   This Python script is meant to be used in PiXYZ STUDIO
#   Open the script in STUDIO Script window, and click the Execute button (CTRL+E)
#
#   Script created by Frozen Forest Reality Technologies.
#   All rights about PiXYZ Studio and PiXYZ Python API belongs PiXYZ Software - 2019

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# [USER PARAMETER] Desired file path
FILE_PATH = 'D:/output.json'
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


componentsTypeAndNames=[[scene.ComponentType.InteractionBehavior, "InteractionBehavior"],[scene.ComponentType.Light, "Light"],[scene.ComponentType.PMI, "PMI"],[scene.ComponentType.Part, "Part"],[scene.ComponentType.VisualBehavior, "VisualBehavior"]]
core.removeConsoleVerbose(core.Verbose.INFO)


def writeLine(file,values, stop):
    line = '    {\"' + values[0] + '\":\"' + values[1] + '\"'
    if stop:
        line = line + '}'
    else:
        line = line + '},\n'
    file.write(str(line))  


def parseTree(node, file, stop):
    name = scene.getNodeName(node)
    try:
        parent = scene.getNodeName(scene.getParent(node))
    except:
        parent = "null"
    
    attributesValues = [name, parent]

    childCount = len(scene.getChildren(scene.getRoot()))
    lastElement = scene.getChildren(scene.getRoot())[childCount - 1]

    writeLine(file, attributesValues, stop)

    for child in scene.getChildren(node):
        if lastElement == child:
            parseTree(child, file, True)
        else:
            parseTree(child, file, False)


def main(filePath):
    root = scene.getRoot()
    with open(filePath, 'w') as file:
        file.write(str('[\n'))
        parseTree(root, file, False)
        file.write(str('\n]'))
    print('\nDone: structure tree exported at ' + filePath)


main(FILE_PATH)
core.addConsoleVerbose(core.Verbose.INFO)

