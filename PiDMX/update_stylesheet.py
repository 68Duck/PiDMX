def update_stylesheet(stylesheet,propertyToChange,newPropertyValue):
    splitStylesheet = stylesheet.split(";")
    splitProperties = []
    for property in splitStylesheet:
        if property == "":
            splitStylesheet.remove("")
        else:
            splitProperty = property.split(":")
            if splitProperty[0] == propertyToChange:
                # print(splitProperty)
                splitProperty[1] = newPropertyValue
            splitProperty = ":".join(splitProperty)
            splitProperties.append(splitProperty)
    # print(splitProperties)
    splitStylesheet = ";".join(splitProperties)
    splitStylesheet = splitStylesheet + ";"
    return splitStylesheet



if __name__ == "__main__":
    update_stylesheet("background-color:white;border: 5px solid white;","border","blue")
