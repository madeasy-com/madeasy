with open("dwaynewadeisawoman.json", "r+") as file:
    content = file.read()
    file.seek(0)
    content.replace("}{", "}, ")
    content.replace("}}}}}", "}}}}")
    file.write(content)
