"""
Created on 2021/05/31

@author: akirakaren
"""
import pandas as pd
from lxml import etree, objectify
import sys
import csv

from remove_namespace import remove_namespace


def parse_xml(filename):
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(filename, parser)
    return tree.getroot()


def accession_disease_parser(filename, outfile):
    root = parse_xml(filename)
    # remove_namespace(root, namespace)

    with open(outfile, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(("accession", "chebi_id", "disease_name", "omim_id"))

        for elem in root.iter('{*}metabolite'):
            accession = elem.findall('{*}accession')[0].text
            chebiid = elem.findall('{*}chebi_id')[0].text
            disease_name = \
                [item.text for item in elem.findall(".diseases/disease/name")]
            omim_id_text = \
                [item.text for item in
                 elem.findall("./diseases/disease/omim_id")]
            omim_id = ["NA" if omi is None else omi for omi in omim_id_text]

            writer.writerow((accession, chebiid, ";".join(disease_name),
                            ';'.join(omim_id)))


if __name__ == '__main__':
    accession_disease_parser(
        "HMDB_NOSCHEMA/hmdb_metabolites_short_noschema.xml",
        "ACCESSION_DISEASE_TABLE/hmdb_acc_disease_short.csv")
    accession_disease_parser("HMDB_NOSCHEMA/hmdb_metabolites_noschema.xml",
                             'ACCESSION_DISEASE_TABLE/hmdb_acc_disease.csv')
