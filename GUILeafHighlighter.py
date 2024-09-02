from PIL import Image, ImageDraw
import glob
import re
import os

def retrieve_bounds(line):
    # Simple regex to recognize and retrieve bounds based on pattern
    bounds = re.search(r'bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"',line)
    #Once retrieved, we must get each individual coordinate from the capturing groups and convert
    # them to integers within a tuple for drawing later
    if bounds:
        west = int(bounds.group(1))
        north = int(bounds.group(2))
        east = int(bounds.group(3))
        south = int(bounds.group(4))
        return (west,north,east,south)
    return None

def retrieve_leafs(xmlfilename):
    # Initialize an array to store the leaf bounds
    leafs = []
    # Initialize a stack to track open tags to match with corresponding closing tags
    stack = []

    # Open XML File for reading
    with open(xmlfilename, 'r', encoding='UTF-8') as file:
        # Read file line by line to make it easier to parse
        xmlfile = file.read()
        # Find all tags in xml file using regex and return the matches as an iterable
        # to be able to extract start position, tag name and whether its opening,closing or
        # self-closing
        tags = re.finditer(r'<(/?)(\w+)[^>]*>',xmlfile)

        for tag in tags:
            startpos = tag.start()
            tagtype = tag.group(1)
            name = tag.group(2)

            # Handle closing tags by identifying closing slash
            if tagtype == '/':
                # Verify that top of stack contains matching open tag
                if stack and stack[-1][0] == name:
                    tagname, openpos = stack.pop()
                    # If the position of the opening tag on the top of the stack matches
                    # that of the current tag's opening it is a leaf node
                    if openpos == tag.start():
                        # Retrieve the bounds from the tag 
                        bounds = retrieve_bounds(xmlfile[openpos:tag.end()])
                        if bounds:
                            # If found, add them to the list of leafs
                            leafs.append(bounds)

            # Handle self-closing tags and opening tags based on absence of closing /
            else:
                # Check if entire tag ends with /> to verify if it is self-closing
                # Self-closed tag is automatically a leaf node, so retrieve bounds from tag
                if tag.group(0).endswith('/>'):
                    bounds = retrieve_bounds(tag.group(0))
                    if bounds:
                        leafs.append(bounds)
            
            # Handle opening tags
                else:
                    # Add the tag type and line number to the stack to track
                    stack.append((name, startpos))

    return leafs

def highlightLeafs(image,coords,outputDirectory = 'GeneratedPNGs'):
    # First retrieve image file and open it with PIL library then create a Draw object to draw 
    # boxes on the existing images
    png = Image.open(image)
    highlight = ImageDraw.Draw(png)

    # Highlight each of the leaf nodes in the given list with a yellow box
    for boundset in coords:
        highlight.rectangle(boundset,outline = "yellow",width = 5)

    # Save the highlighted image as a new image in the GeneratedPNGs folder by creating a new 
    # file path
    nonhighlightedname = os.path.splitext(os.path.basename(image))[0]
    highlightednamepath = os.path.join(outputDirectory,f"{nonhighlightedname}_highlighted.png")

    png.save(highlightednamepath)
    print(f"{nonhighlightedname}_highlighted.png", "saved to",outputDirectory)
    return
    



def MatchandHighlight(directory = 'Programming-Assignment-Data\Programming-Assignment-Data'):
    #First, Retrieve all files ending in .xml files from input folder and put them in a list
    xmls = glob.glob(os.path.join(directory,"*.xml"))
    #For each xml, determine if it's pair exists within the directory and notify the user
    # if it does not
    for xml in xmls:
        # Get file name excluding the extension to match it with corresponding PNG
        basefilename = os.path.splitext(xml)[0]
        pngmatchname = os.path.join(f"{basefilename}.png")
        #Verify that matching PNG file exists within directory and if it does
        # extract the bounds of the leaf components with other nested functions
        if os.path.exists(pngmatchname):
            boundset = retrieve_leafs(xml)
            # once bounds are retrieved, highlight the png image accordingly
            highlightLeafs(pngmatchname,boundset)

        else:
            # if png doesn't exist, notify user
            print(pngmatchname,"does not exist in input Directory! Please name file accordingly for highlighting")
    # Notify user that process has completed
    print("Process Complete! Please refer to the GeneratedPNGs directory for your images")
    return


if __name__ == "__main__":
    MatchandHighlight()

