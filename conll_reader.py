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
    def __init__(self,nodes):
        self.nodes = {}
        self.deps = []
        self.root_id = None
        for node in nodes:
            self.nodes.update({node.id:node})
            if node.head == 0:
                self.root_id = node.id
            else:
                self.deps.append((node.head, node.relation, node.id))

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
                parts = line.strip().split("	")
                parsedId = int(parts[0])
                parsedHead = int(parts[6])
                data = Node(parsedId,parts[1],parts[2],parts[3],parts[4],parts[5],parsedHead,parts[7])
                current.append(data)
        return sentences

conll_data = reader("sequoia.7.0.expanded.conll")
for sentence in conll_data:
    tree = Tree(sentence)
    print(tree.deps)