def markFileUpload(d: dict[str, dict[str, str | bool]]):
    filenames = []
    for (key, item) in d.items():
        if item['Saved'] == True:
            filenames.append(key)

    output = "*User uploaded files: "
    for i in range(0, len(filenames)):
        if i == 0:
            output += filenames[i]
        elif i == len(filenames) -1:
            output += ", " + filenames[i] + "*"
        else:
            output += ", " + filenames[i]

    return output