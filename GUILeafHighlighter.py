import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw
import glob


def retrieve_leafs(xmlfilename):
    # Retrieve root of overall XML tree to begin parsing
    tree = ET.parse(xmlfilename)
    root = tree.getroot()
    # Goal will be to retrieve the bounds of all the leaf components to then draw
    # through them using PIL
    components = []
    # Iterate through tree to retrieve leafs
    for leaf in root.iter():
        #If the length of an ElementTree element is zero, it has no children and is therefore
        # a leaf node
        if not list(leaf):
            # Use ElementTree method to retrieve bounds directly from leaf component
            bounds = leaf.get('bounds')
            print(bounds)
    return 

retrieve_leafs("Programming-Assignment-Data\Programming-Assignment-Data\com.apalon.ringtones.xml")

