from PIL import Image, ImageDraw
import glob
import re
import os

def retrieve_bounds(line):
    print("In retrieve bounds")
    # Simple regex to recognize and retrieve bounds based on pattern
    bounds = re.search(r'bounds="\[(\d)+,(\d)+\]\[(\d)+,(\d)+\]"',line)
    #Once retrieved, we must get each individual coordinate from the capturing groups and convert
    # them to integers within a tuple for drawing later
    if bounds:
        north = int(bounds.group(2))
        south = int(bounds.group(4))
        east = int(bounds.group(3))
        west = int(bounds.group(1))
        return (west,north,east,south)
    return None

def retrieve_leafs(xmlfilename):
    print('In retrieve leafs')
    #Initialize an array to store the leaf bounds
    leafs = []
    # Initialize a stack to track open tags to match with corresponding closing tags to
    # identify leaf nodes
    stack = []

    #Open XML File for reading
    with open(xmlfilename,'r',encoding = 'UTF-8') as file:
        #Read file line by line to make it easier to parse
        lines = file.readlines()

        for num, line in enumerate(lines):
            # Utilize simple regex to identify the tags when the lines are scanned 
            opentag = re.search(r'<(\w+)[^>]*>',line)
            closedtag = re.search(r'</(\w+)>',line)
            selfclosetag = re.search(r'<(\w+)[^>]*/>',line)

            # Three different scenarios 1. self close, 2. open and 3. close tag match
            # If a match for an open tag is found, add the tag name and line number
            # and look for matching non-self closing tag, we do not add self closing tags to the stack

            if opentag:
                #Add the tag name to the stack to help with retrieving bounds
                stack.append((opentag.group(1),num))

            elif selfclosetag:
                # If it is a self closed tag, extract the bounds immediately as it is 
                # automatically a leaf node
                bounds = retrieve_bounds(line)
                leafs.append(bounds)
            
            elif closedtag:
                #If closing tag, verify that top of stack contains matching open tag
                #if it does not contain the match, continue because it could be a nested
                # if it does match, it is a leaf
                # pop and retrieve the bounds utilizing the line number from the opening tag
                if stack and stack[-1][0] == closedtag.group(1):
                    tagname,openlinenum = stack.pop()
                    # if the opening tag number is one line before the closing tag, it is the
                    # corresponding closing tag so we retrieve the bounds of the leaf
                    if openlinenum == num - 1:
                        bounds = retrieve_bounds(lines[openlinenum])
                        leafs.append(bounds)
    return leafs

def highlightLeafs(image,coords,outputDirectory = 'GeneratedPNGs'):
    print('InhighlightLeafs')
    # First retrieve image file and open it with PIL library then create a Draw object to draw 
    # boxes on the existing images
    png = Image.open(image)
    highlight = ImageDraw.Draw(png)

    # Highlight each of the leaf nodes in the given list with a yellow box
    for boundset in coords:
        highlight.rectangle(boundset,outline = "yellow",width = 3)

    # Save the highlighted image as a new image in the GeneratedPNGs folder
    nonhighlightedname = os.path.splitext(os.path.basename(image))[0]
    highlightednamepath = os.path.join(outputDirectory,f"{nonhighlightedname}_highlighted.png")

    png.save(highlightednamepath)
    print("Saved ",highlightednamepath," in output directory ")
    return
    



def MatchandHighlight(directory = 'Programming-Assignment-Data\Programming-Assignment-Data'):
    print('In MatchandHighlight')
    #First, Retrieve all files ending in .xml files from input folder and put them in a list
    xmls = glob.glob(os.path.join(directory,"*.xml"))
    #print(xmls)
    #For each xml, determine if it's pair exists within the directory and notify the user
    # if it does not
    for xml in xmls:
        # Get file name with no extension
        basefilename = os.path.splitext(xml)[0]
        pngmatchname = os.path.join(f"{basefilename}.png")
        #print(pngmatchname)
        #Verify that matching PNG file exists within directory and if it does
        # extract the bounds of the leaf components with other nested functions
        if os.path.exists(pngmatchname):
            boundset = retrieve_leafs(xml)
            # once bounds are retrieved, highlight the png image accordingly
            highlightLeafs(pngmatchname,boundset)

        else:
            # if png doesn't exist, notify user
            print(pngmatchname,"does not exist in input Directory! Please name file accordingly for highlighting")
    return


if __name__ == "__main__":
    MatchandHighlight()


