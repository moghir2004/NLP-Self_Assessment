class Node:
    def __init__(self, id, form, lemma, cpos, pos, feats, head, relation):
        self.id = id
        self.form = form
        self.lemma = lemma
        self.cpos = cpos
        self.pos = pos
        self.feats = feats
        self.head = head
        self.relation = relation


class Tree:
    def __init__(self, nodes):
        self.nodes = {}
        self.deps = []
        self.root_id = None
        for node in nodes:
            self.nodes.update({node.id: node})
            if node.head == 0:
                self.root_id = node.id
            else:
                self.deps.append((node.head, node.relation, node.id))

    def isInv(self, nodes):
        verbs = {node.id:node.relation for node in nodes if node.pos == "V"}
        postverbal_verbs = set()
        for node in nodes:
            if node.relation == "suj" and node.head in verbs.keys():
                if node.id > node.head:
                    postverbal_verbs.add(node.head)
        rel_clause_heads = {
            node.id for node in nodes
            if node.pos == "V" and node.relation == "mod.rel"
        }
        postverbal_head_of_rel_clause = rel_clause_heads & postverbal_verbs
        return len(verbs), len(postverbal_verbs), len(postverbal_head_of_rel_clause)


def reader(file_path):
    sentences = []
    current = []
    with open(file_path, "r") as file:
        for line in file:
            if line.strip() == "":
                if current:
                    sentences.append(current)
                    current = []
            else:
                parts = line.strip().split("	")
                parsedId = int(parts[0])
                parsedHead = int(parts[6])
                data = Node(
                    parsedId,
                    parts[1],
                    parts[2],
                    parts[3],
                    parts[4],
                    parts[5],
                    parsedHead,
                    parts[7],
                )
                current.append(data)
        return sentences


conll_data = reader("sequoia.7.0.expanded.conll")
total_verbs = 0
postverbal_verbs = 0
head_of_rel_clause = 0
for sentence in conll_data:
    tree = Tree(sentence)
    t, p, h = tree.isInv(sentence)
    total_verbs += t
    postverbal_verbs += p
    head_of_rel_clause += h

probability_post = (postverbal_verbs / total_verbs) if total_verbs else 0.0
print("total:", total_verbs)
print("postverbal:", postverbal_verbs)
print("head of rel clause", head_of_rel_clause)
print("probability_post:", probability_post)