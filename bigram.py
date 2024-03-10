import torch
import torch.nn as nn
from torch.nn import functional as f
device="cuda" if torch.cuda.is_available() else "cpu"
block_size=8
batch_size=4

with open("wizard_of_oz.txt","r",encoding="utf-8") as f:
    text=f.read()


#all characters in text in ascending order
chars =sorted(set(text ))
vocab_size=len(chars)


#encoder,decoder
string_to_int = {ch:i for i,ch in enumerate(chars) }
int_to_string = {i:ch for ch,i in enumerate(chars)}
encode= lambda s:[string_to_int[c] for c in s]
decode= lambda l:" ".join([int_to_string[i] for i in l])
data=torch.tensor(encode(text),dtype=torch.long)



#train-test split
n=int(0.8*len(data))
train_data=data[:n]
test_data=data[n:]

def get_batch(split):
    data=train_data if split=="train" else test_data
    ix=torch.randint(len(data)-block_size,(batch_size,))
    print(ix)
    x=torch.stack([data[i:i+block_size] for i in ix])
    y=torch.stack([data[i+1:i+block_size+1] for i in ix])
    x,y=x.to(device),y.to(device)
    return x,y

x,y=get_batch("train")
print("inputs:")
print(x)
print("targets")
print(y)

class BigramLanguageModel(nn.Module):
    def __init__(self,vocab_size):
        super().__init__()
        self.token_embedding_table=nn.Embedding(vocab_size,vocab_size)
    
    def forward(self,index,targets=None):
        logits=self.token_embedding_table(index)
        if targets is None:
            loss=None
        else:   
            B,T,C=logits.shape
            logits=logits.view(B*T,C)
            targets=targets.view(B*T)
            loss=f.cross_enteropy(logits,targets)
        return logits,loss
    
    def generate(self,index,max_new_tokens):
        for i in range(max_new_tokens):
            logits,loss=self.forward(index)
            logits=logits[:,-1,:]
            probs=f.softmax(logits,dim=-1)
            index_next=torch.multinomial(probs,num_samples=1)
            index=torch.cat((index,index_next),dim=1)
        return index
    
model=BigramLanguageModel(vocab_size)
m=model.to(device)

context=torch.zeroes((1,1),dtype=torch.long,device=device)
generated_chars=decode(m.generate(context,max_new_tokens=500)[0].tolist())
print(generated_chars)
            