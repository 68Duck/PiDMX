def order_dictionaries(dictionaries,key):
    sorted_dictionaries = []
    try:
        a = dictionaries[0][key]
    except KeyError:
        raise Exception("The key is not correct")
    for dict in dictionaries:
        i=0
        for i,d in enumerate(sorted_dictionaries):
            if dict[key] < d[key]:
                break
        sorted_dictionaries.insert(i+1,dict)
    return sorted_dictionaries
