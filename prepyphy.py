import sys, sqlite3, os
import argparse

parser=argparse.ArgumentParser(
    description='''This script preprocess names.dmp and nodes.dmp from NCBI taxonomy.''')
parser.add_argument('input_folder', help='path to the unpacked taxdmp')
args=parser.parse_args()

#python prepyphy.py folder db


#taxid : Node
tree = {}

taxid_synonym = {}

folder = sys.argv[1]


names_dmp = os.path.join(folder, "names.dmp")
#process the names.dmp
for line in open(names_dmp, 'r'):
    fields = line.strip().split("\t")
    notion = fields[6]
    taxid = fields[0]
    name = fields[2]


    if notion== "scientific name":
        #tree[taxid] = None or [name,"0",""]
        if taxid not in tree:
            tree[taxid] = [name,"0",""]
    elif notion== "synonym" or notion == "equivalent name":
        if taxid not in taxid_synonym:
            taxid_synonym[taxid] = set()

        taxid_synonym[taxid].add(name)
        
        #synonym_taxid[name] = None or taxid



nodes_dmp = os.path.join(folder, "nodes.dmp")
#process the nodes.dmp
for line in open(nodes_dmp, 'r'):
    fields = line.strip().split("\t")
    
    taxid = fields[0]
    parent = fields[2]
    rank = fields[4]

    
    if taxid in tree:
        tree.get(taxid)[1] = parent
        tree.get(taxid)[2] = rank
        


with open("tree.tsv", 'a') as outfile:

    for taxid in tree.keys():
        outfile.write(f"{taxid}\t" + tree[taxid][0].replace("'","''") + f"\t{str(tree[taxid][1])}\t{tree[taxid][2]}\n")


with open("synonym.tsv", 'a') as outfile:
    index = 0

    for taxid in taxid_synonym:
        for taxon in taxid_synonym[taxid]:


            outfile.write(f"{index}\t{taxid}\t"+ taxon.replace("'","''") + "\n")


            index += 1

