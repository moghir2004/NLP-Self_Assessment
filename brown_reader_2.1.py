collection: dict[str, int] = {}


def br_reader(file):
    counter = 1
    with open(file, "r") as f:
        for line in f:
            items = line.strip().split(" ")
            for item in items:  # item = word/pos pair
                # pairs = list of word then POS ([word,POS])
                pairs = item.split("/")
                if pairs[0] in collection.keys():  # increment if word
                    collection[pairs[0]] += 1  # is already in collection
                else:
                    collection.update({pairs[0]: counter})
        return collection


def sort(collection: dict[str, int]):
    l = sorted(zip(collection, collection.values()), reverse=True, key=lambda x: x[1])
    return l[:99]


br_reader("emea-fr.brown")
print(sort(collection))
