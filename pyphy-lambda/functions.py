import rds_config
import pymysql
#rds settings
rds_host = rds_config.endpoint
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name

unknown = -1
no_rank = "no rank"

conn = pymysql.connect(host=rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)


def getNameByTaxid (taxid):
    """get taxonomic name given a taxid
    
    Args:
        taxid (str or int): query taxid
        
    
    Returns:
        str: return a taxonomic name if it is found otherwise unknown
    """
    command = f"SELECT name FROM tree WHERE taxid = '{taxid}';"
    
    cursor = conn.cursor()
    cursor.execute(command)
    
    result = cursor.fetchone()
    cursor.close()   
    if result:
        return result[0]
    else:
        return "unknown"


def getTaxidByName(name, limit=1, synonym=True):
    """get taxid given a taxonomic name or a synonym
    
    Args:
        name (str): query taxonomic name
        limit (int, optional): how many taxid to return
        synonym (bool, optional): should a synonym search be performed
    
    Returns:
        list: return a list of taxid if the name is found otherwise a list of unknown
    """
    cursor = conn.cursor()
    command = "SELECT taxid FROM tree WHERE name = '" + str(name).replace("'", "''") +  "';"

    cursor.execute(command)
    results = cursor.fetchall()
    
    
    temp = []
    for result in results:
        temp.append(result[0])
    
    if len(temp) != 0:
        temp.sort()
        cursor.close()
        return temp[:limit]
    elif synonym == True:
  
        command = "SELECT taxid FROM synonym WHERE name = '" + str(name).replace("'", "''") +  "';"
        cursor.execute(command)
        results = cursor.fetchall()
        cursor.close()
        temp = []

        for result in results:
            temp.append(result[0])

        if len(temp) != 0:
            temp.sort()
            return temp[:limit]

        else:
            return [unknown]

    else:
        cursor.close()
        return [unknown]
        

def getRankByTaxid(taxid):
    """get the rank given a taxid
    
    Args:
        taxid (int or str):query taxid
    
    Returns:
        str: the rank of the taxid
    """

    cursor = conn.cursor()
    command = "SELECT rank FROM tree WHERE taxid = '" + str(taxid) +  "';"
    cursor.execute(command)
       
    result = cursor.fetchone()
    cursor.close()
    if result:
        return result[0].strip()
    else:
        return no_rank
        

def getParentByTaxid(taxid):
    """get parent taxid given a taxid
    
    Args:
        taxid (str or int): query taxid
        
    
    Returns:
        int: return the parent taxid if it is found otherwise unknown
    """
    cursor = conn.cursor()
    command = "SELECT parent FROM tree WHERE taxid = '" + str(taxid) +  "';"
    cursor.execute(command)
    
    result = cursor.fetchone()
    cursor.close()
    if result:
        return result[0]
    else:
        return unknown
        
        
        
def getDictPathByTaxid(taxid):
    """get the taxonomic path with the ranks as keys given a taxid
    
    Args:
        taxid (str or int): query taxid
        
    
    Returns:
        dict: return a dict of rank: parent taxid if it is found otherwise an empty dict
    """

    path = {}

    current_id = -1

    try:
        current_id = int(taxid)
    except:
        pass
    rank = getRankByTaxid(current_id)
    path[rank] = current_id
    
    while current_id != 1 and current_id != unknown:
        #print current_id
        current_id = int(getParentByTaxid(current_id))
        rank = getRankByTaxid(current_id)

        path[rank] = current_id
    
    return path
    
    
def getSonsByTaxid(taxid):
    """get the 1st-level sons given a taxonomic name
    
    Args:
        name (str): query name
        
    
    Returns:
        list: return a list of son taxid if it is found otherwise an empty list
    """

    cursor = conn.cursor()
    command = "SELECT taxid FROM tree WHERE parent = '" + str(taxid) +  "';"

    cursor.execute(command)
    
    
    rows = cursor.fetchall()
    
    result = []
    for row in rows:
        result.append(row[0])
    
    cursor.close()
    return result