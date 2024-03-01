import torch

with open("wizard_of_oz.txt","r",encoding="utf-8") as f:
    text=f.read()


#all characters in text in ascending order
chars =sorted(set(text ))
vocabulary_size=len(chars)


#encoder,decoder
string_to_int = {ch:i for i,ch in enumerate(chars) }
int_to_string = {i:ch for ch,i in enumerate(chars)}
encode= lambda s:[string_to_int[c] for c in s]
decode= lambda l:" ".join([int_to_string[i] for i in l])
data=torch.tensor(encode(text),dtype=torch.long)
print(data[:100])
