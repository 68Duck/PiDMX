def sortByTerm(unsortedList,term):  #term is zero indexed
    removingList = []
    for i in range(len(unsortedList)):
        if not unsortedList[i]:
            removingList.append(unsortedList[i])
    for item in removingList:
        unsortedList.remove(item)
    sortedList = []
    if len(unsortedList)>1:
        for i in range(len(unsortedList)):
            insertionPlace = 0
            for j in range(len(sortedList)):
                if int(sortedList[j][term]) < int(unsortedList[i-len(sortedList)][term]):
                    insertionPlace = insertionPlace + 1
            sortedList.insert(insertionPlace,unsortedList[i-len(sortedList)])
            unsortedList.remove(unsortedList[i-len(sortedList)+1])
    else:
        sortedList = unsortedList
    return sortedList
