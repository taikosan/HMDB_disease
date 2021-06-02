"""
Created on 2021/06/02

@author: akirakaren
"""
import pandas as pd


def disease_accession_table(infile, outfile):
    df = pd.read_csv(infile, header=0)
    nestedlst = df['omim_id'].values.tolist()
    nonanlst = [x for x in nestedlst if type(x) is not float]
    sepratedlst = [string.split(";") for string in nonanlst]
    # print(sepratedlst)
    flatlst = [item for sublist in sepratedlst for item in sublist]
    uniquelst = sorted(set(flatlst))
    omimdict = {omim: [] for omim in uniquelst}
    for i, omimlst in enumerate(df['omim_id']):
        if type(omimlst) is not float:
            for id in omimlst.split(";"):
                # print(id)
                # print(df.iloc[i, df.columns.get_loc('accession')])
                omimdict[id].append(df.iloc[i, df.columns.get_loc('accession')])
    omimdict.pop('NA', None)

    disease_index_table = pd.DataFrame(columns=['omim_id', 'accessions'])
    disease_index_table['omim_id'] = omimdict.keys()
    acclst = [";".join(values) for values in omimdict.values()]
    disease_index_table['accessions'] = acclst
    disease_index_table.to_csv(outfile, index=False)


if __name__ == '__main__':
    disease_accession_table(
        "ACCESSION_DISEASE_TABLE/hmdb_acc_disease_short.csv",
        "OMIM_ACCESSION_TABLE/hmdb_omim_acc_short.csv")
    disease_accession_table(
        "ACCESSION_DISEASE_TABLE/hmdb_acc_disease.csv",
        "OMIM_ACCESSION_TABLE/hmdb_omim_acc.csv")