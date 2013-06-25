"""
The functions in this module supplement the xml.dom.minidom module in the
standard library.

"""

def get_node_text(element, tag, index=0):
    """
    Parse an xml element and return the text from the node with the given tag.

    Args:
    element -- an xml.dom.mindom Element.
    tag     -- the tag of the text node.
    index   -- the index of the text node.

    """
    try:
        text_node = element.getElementsByTagName(tag)[index].childNodes[0]
        return text_node.data
    except IndexError:
        # Probably indicates the tag couldn't be found.
        return ''
