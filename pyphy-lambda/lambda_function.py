


import functions

def lambda_handler(event, context):
    """
    This function fetches content from MySQL RDS instance
    """
    
    output = None
    
    if "method" in event:
        if event["method"] == "getnamebytaxid":
            if "taxid" in event:
                output = functions.getNameByTaxid(event["taxid"])
                
                
        
        elif event["method"] == "gettaxidbyname":
            if "name" in event:
                output = functions.getTaxidByName(event["name"])
                
        elif event["method"] == "getrankbytaxid":
            if "taxid" in event:
                output = functions.getRankByTaxid(event["taxid"])
                
        elif event["method"] == "getparentbytaxid":
            if "taxid" in event:
                output = functions.getParentByTaxid(event["taxid"])
                
        elif event["method"] == "getdictpathbytaxid":
            if "taxid" in event:
                output = functions.getDictPathByTaxid(event["taxid"])
                
        elif event["method"] == "getsonsbytaxid":
            if "taxid" in event:
                output = functions.getSonsByTaxid(event["taxid"])
    
    
    response = response = {
        "statusCode": 200,
        "headers": {},
        "body": output
    }


    return response
    #return event