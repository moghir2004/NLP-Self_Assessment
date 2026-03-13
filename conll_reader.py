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
        verbs = {node.id: node.relation for node in nodes if node.pos == "V"}
        eligible_verbs = set()  # verbs with only nominal subjects
        postverbal_verbs = set()
        for node in nodes:
            if (
                node.relation == "suj"
                and node.cpos == "N"
                and node.head in verbs.keys()
            ):
                eligible_verbs.add(node.head)
                if node.id > node.head:
                    postverbal_verbs.add(node.head)
        rel_clause_heads = {
            verb_id
            for verb_id in eligible_verbs
            if self.nodes[verb_id].relation == "mod.rel"
        }
        postverbal_head_of_rel_clause = rel_clause_heads & postverbal_verbs
        return (
            len(eligible_verbs),
            len(postverbal_verbs),
            len(rel_clause_heads),
            len(postverbal_head_of_rel_clause),
        )


def reader(file_path):
    sentences = []
    current = []
    with open(file_path, "r") as file:
        for line in file:
            if line.strip() == "":
                if current:
                    sentences.append(
                        current
                    )  # appnd current sentence to a list of sentences
                    current = []  # reset the current sentence
            else:
                parts = line.strip().split(
                    "	"
                )  # items of a node are separated by tab character
                parsedId = int(parts[0])  # store ids as numbers
                parsedHead = int(parts[6])
                data = Node(
                    parsedId,  # id
                    parts[1],  # form
                    parts[2],  # lemma
                    parts[3],  # cpos
                    parts[4],  # pos
                    parts[5],  # feats
                    parsedHead,  # head
                    parts[7],  # relation
                )
                current.append(data)  # append node to current sentence
        return sentences


conll_data = reader("sequoia.7.0.expanded.conll")
total_verbs = 0
postverbal_verbs = 0
head_of_rel_clause = 0
post_head_rel_clause = 0
for sentence in conll_data:
    tree = Tree(
        sentence
    )  # we can print dependency tuples with print(tree.deps) but thats not the final aim of exercice
    t, p, h, ph = tree.isInv(
        sentence
    )  # t = verb for this iteration, p = postverbal verb, h = head of rel clause,ph = postverbal head of rel clause
    total_verbs += t
    postverbal_verbs += p
    head_of_rel_clause += h
    post_head_rel_clause += ph
# calculate probabilities from corpus, other calculations are in the markdown file
probability_post = (postverbal_verbs / total_verbs) if total_verbs else 0.0
probability_rel = (head_of_rel_clause / total_verbs) if total_verbs else 0.0
probability_post_rel = (post_head_rel_clause / total_verbs) if total_verbs else 0.0
# print everithing
print("total:", total_verbs)
print("postverbal:", postverbal_verbs)
print("head of rel clause", head_of_rel_clause)
print("post_head_rel:", post_head_rel_clause)
print("probability_post:", probability_post)
print("probability_rel:", probability_rel)
print("probability_post_rel:", probability_post_rel)
