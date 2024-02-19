with open("wizard_of_oz.txt","r",encoding="utf-8") as f:
    text=f.read()
print(len(text))

#all characters in text in ascending order
chars =sorted(set(text))
print(chars)