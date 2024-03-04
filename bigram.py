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


#train-test split
n=int(0.8*len(data))
train_data=data[:n]
test_data=data[:n]

#taking snippets of prediction and target
block_size=8
x=train_data[:block_size]
y=train_data[1:block_size+1]

for t in range(block_size):
    context=x[:t+1]
    target=y[t]
    print("when input is",context,"target is",target)