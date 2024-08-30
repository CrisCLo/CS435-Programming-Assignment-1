import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw
import glob
import re

def retrieve_bounds(leaf):
    pass

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
                #if it does not contain the match, it is not a leaf
                # if it does match, pop
                if stack and stack[-1][0] == closedtag.group(1):
                    linenum = stack.pop()
                    if linenum == num - 1:
                        bounds = retrieve_bounds(lines[linenum])
                        leafs.append(bounds)
    return leafs


