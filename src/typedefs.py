def MEDFORD_Version(inp: str) -> bool :
    return inp in ["beta","1.0","2.0"]

def Validators(majortoken: str, typename: str) -> callable :
    fullname = majortoken + "_" + typename
    if fullname.lower() == "medford_version" : 
        return MEDFORD_Version
    
    raise NotImplementedError("Unknown validator requested.")