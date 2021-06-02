import zipfile
import sys
import csv
import glob
import os.path

from lxml import etree

# import libecoli.utils as utils
import subprocess

HMDB_FILE_URL = "https://hmdb.ca/system/downloads/current/hmdb_metabolites.zip"


def listall(root, tag):
    return [elem.text for elem in root.findall(f'{{*}}{tag}')]


def read_metabolites(filename):
    with open(filename) as f:
        tree = etree.parse(f)

    writer = csv.writer(sys.stdout)
    for i, elem in enumerate(tree.iter('{*}metabolite')):
        kegg_id = elem.findall('{*}kegg_id')[0].text
        synonyms = listall(elem.findall('{*}synonyms')[0], 'synonym')
        assert all(';' not in synonym for synonym in synonyms)
        writer.writerow((listall(elem, 'accession')[0], kegg_id,
                         listall(elem, 'name')[0], ';'.join(synonyms)))


def load():
    # dirname = utils.DATA_PATH
    dirname = "./HMDB_RAW_DATA"
    filename = os.path.join(dirname, "hmdb_metabolites_noschema.xml")
    zipfilename = os.path.join(dirname, "hmdb_metabolites.zip")
    if not os.path.isfile(filename):
        if not os.path.isfile(zipfilename):
            # subprocess.call(f"wget {HMDB_FILE_URL}", shell=True)
            subprocess.call(f"mv hmdb_metabolites.zip {zipfilename}",
                            shell=True)
            # utils.fetch_url(HMDB_FILE_URL, zipfilename, encoding='binary')
        with zipfile.ZipFile(zipfilename) as zipin:
            zipin.extractall(dirname)

    read_metabolites(os.path.join(dirname, "hmdb_metabolites.small.xml"))
    # read_metabolites(filename)


if __name__ == '__main__':
    import logging

    logging.basicConfig(level=logging.DEBUG)
    load()
