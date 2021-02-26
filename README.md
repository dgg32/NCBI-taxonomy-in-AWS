# Serve NCBI Taxonomy as API in AWS

This repository hosts the code for the blog post: [Serve NCBI Taxonomy in AWS, Serverlessly](https://dgg32.medium.com/serve-ncbi-taxonomy-in-aws-serverlessly-d2725b5e2c41).


# Files

It contains two parts. "prepyphy.py" transforms the NCBI taxdmp file into tsv files for import into Aurora. The pyphy-lambda folder contains the Lambda function code for upload into AWS Lambda.



# Usage

##  Prepyphy
To prepare the tsv files. First download taxdmp from [NCBI taxonomy](https://ftp.ncbi.nih.gov/pub/taxonomy/) and unpack it. Then run:

    python prepyphy.py taxdmp_folder

It will generate two files (tree.tsv and synonym.tsv) in the current folder. 

## Lambda
Before you upload the pyphy-lambda, you need to open rds_config.py and fill in the details of your Aurora database. 

    #config file containing credentials for RDS MySQL instance
    
    endpoint = ""
    
    db_username = ""
    
    db_password = ""
    
    db_name = ""

Once done, zip the files in this folder (please don't zip the folder itself). And the zip file is ready for upload to Lambda.

# Author
* **Sixing Huang** - *Concept and Coding*
