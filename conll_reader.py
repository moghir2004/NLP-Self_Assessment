class Node:
    def __init__(self,id,form,lemma,cpos,pos,feats,head,relation):
        self.id = id
        self.form = form
        self.lemma = lemma
        self.cpos = cpos
        self.pos = pos
        self.feats = feats
        self.head = head
        self.relation = relation

class Tree:
    def __init(self,nodes,deps)
    def render(node,governor,deprel):
        governor = node.head
        deprel = node.deprel
        if governor == 0:
                    
        
        
    

def reader(file_path):
    sentences = []
    current = []
    
    with open(file_path,'r') as file:
        for line in file:
            if line.strip() == "":
                if current:
                    sentences.append(current)
                    current = []
            else:
                parts = line.strip().split()
                data = Node(parts[0],parts[1],parts[2],parts[3],parts[4],parts[5],parts[6],parts[7])
                # parts[0] = dependent word
                # parts[6] = governor word
                # parts[7] = dependency label
                current.append(data)
            if current:
                sentences.append(current)
    return sentences

conll_data = reader("sequoia.7.0.expanded.conll")
for sentence in conll_data:
    print("tree:")      
    for token in sentence:
        print(token)