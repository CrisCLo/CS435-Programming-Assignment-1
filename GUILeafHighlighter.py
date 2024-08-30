from PIL import Image, ImageDraw
import glob
import re
import os

def retrieve_bounds(line):
    # Simple regex to recognize and retrieve bounds based on pattern
    bounds = re.search(r'bounds="(\[(\d)+,(\d)+\]\[(\d)+,(\d)+\]"',line)
    #Once retrieved, we must get each individual coordinate from the capturing groups and convert
    # them to integers within a tuple for drawing later
    north = int(bounds.groupd(2))
    south = int(bounds.groups(4))
    east = int(bounds.groups(3))
    west = int(bounds.groups(1))
    return (west,north,east,south)


def retrieve_leafs(xmlfilename):
    #Initialize an array to store the leaf bounds
    leafs = []
    # Initialize a stack to track open tags to match with corresponding closing tags to
    # identify leaf nodes
    stack = []

    #Open XML File for reading
    with open(xmlfilename,'r',encoding = 'UTF-8'):
        #Read file line by line to make it easier to parse
        lines = xmlfilename.readlines()

        for num, line in enumerate(lines):
            # Utilize simple regex to identify the tags when the lines are scanned 
            opentag = re.search(r'<(\w+)[^>]*>',line)
            closedtag = re.search(r'</(\w+)>',line)
            selfclosetag = re.search(r'<(\w+)[^>]*/>',line)

            # Three different scenarios 1. self close, 2. open and 3. close tag match
            # If a match for an open tag is found, add the tag name and line number
            # and look for matching non-self closing tag, we do not add self closing tags to the stack

            if opentag:
                #Add the tag name to the stack to compare with closing tag name
                stack.append(opentag.group(1))

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

def highlightLeafs(image,coords):
    # First retrieve image file and open it with PIL library then create a Draw object to draw 
    # boxes on the existing images
    png = Image.open(image)
    highlight = ImageDraw.Draw(png)

    # Highlight each of the leaf nodes in the given list with a yellow box
    for boundset in coords:
        highlight.rectangle(boundset,outline = "yellow",width = 3)

    # Save the highlighted image as a new image in the GeneratedPNGs folder
    nonhighlightedname = os.path.splitext(image)
    highlightedname = f"{nonhighlightedname}_highlighted.png"

    png.save(highlightedname)

    return
    



def matchFiles(directory = '\Programming-Assignment-Data\Programming-Assignment-Data'):
    pass



def main():
    pass
