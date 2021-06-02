"""
Created on 2021/06/02

@author: akirakaren
"""
from lxml import etree, objectify


def remove_namespace(doc, namespace):
    """Remove namespace in the passed document in place."""
    ns = u'{%s}' % namespace
    nsl = len(ns)
    for elem in doc.getiterator():
        if elem.tag.startswith(ns):
            elem.tag = elem.tag[nsl:]
    objectify.deannotate(doc, cleanup_namespaces=True)


if __name__ == '__main__':
    # filename = "HMDB_RAW_DATA/hmdb_metabolites_short.xml"
    filename = "HMDB_RAW_DATA/hmdb_metabolites.xml"

    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(filename, parser)
    root = tree.getroot()
    remove_namespace(root, "http://www.hmdb.ca")

    tree.write('HMDB_NOSCHEMA/hmdb_metabolites_noschema.xml',
               pretty_print=True, xml_declaration=True, encoding='UTF-8')
