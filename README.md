# NLP Self-Assessment
This exercice was found in Université Paris Cité's website relating to their computational linguistics program.
Here's the exercice statement :
> ### Reading a dependency tree
> Download the file sequoia.conll and familiarise yourself with it. It contains 3,099
> sentences from L’Est Républicain, EMEA, French Wikipedia, and Europarl, annotated
> with morphological and syntactic information, more precisely dependency trees.
> A dependency is represented as a triple (governor word, dependency label, dependent
> word). \
> To familiarise yourself with this representation :\
> — draw the dependency tree for the second sentence in the file ;\
> — identify the particularity of the root of this tree.\
> Write a programme that reads these dependency trees. Note that the CoNLL format
> is not inherently suited to recursive reading. You may choose between :\
> — a non-recursive structure using a Node class and a Tree class that stores nodes,
governor and dependent relations ;\
> — a recursive structure where each Tree instance contains node information and a
list of dependent subtrees.\
> In both cases, aim for a single pass over the sequence of words. Since one does not
> know in advance where a sentence ends, you must handle a partially built tree structure. (you will see how i dodged this kind of)\
> Moreover, a governor may appear earlier than the line describing it, so you must manage
> partially filled node instances and maintain a list of node instances for all positions in
> the sentence, including in the recursive version.3.2 Estimation using relative frequencyProbability estimation Consider verbs that have (at least one) nominal > subject.\
> Using the provided corpus, estimate by relative frequency :\
> — p = P(INV) : the probability that the subject is inverted (i.e. post-verbal),\
> — P(REL) : the probability that such a verb is the head of a relative clause,\
> — P(REL | INV) and P(INV | REL) : compute this in two ways — directly by restricting the fundamental set, and via Bayes’ theorem.\
> Likelihood Express the likelihood of the parameter p = P(INV), given the observations
(verb occurrences and the position of their subject). What property does the estimator
obtained in the previous section have ? Provide a precise and developed explanation.

## Method
To answer the questions posed in the exercise, the corpus must first be read and converted into an internal representation of dependency trees.
## Reading the CoNLL Corpus
The Sequoia corpus is provided in CoNLL format, where each line corresponds to a token and contains several columns describing its linguistic properties `(form, lemma, POS tag, morphological features, syntactic head, and dependency relation)`.
Sentences are separated by blank lines.\
The reader processes the file sequentially and groups tokens into sentence-level structures.\
Each token is stored as a Node object containing the relevant fields:\
`token id` `form` `lemma` `coarse POS tag` `fine POS tag` `morphological features` `syntactic head` `dependency relation` \
This representation allows the program to reconstruct the dependency relations between words.

### Building Dependency Structures
For each sentence, a Tree object is created.\
The tree stores:
- a dictionary mapping `token id`s to `nodes`
- a list of dependency relations
- the `root` node (identified by head = 0)

This structure allows the program to easily retrieve the governor of each node and inspect the syntactic relations between words.

### Identifying Relevant Verb Occurrences

The analysis focuses on verbs that have at least one nominal subject.\
During traversal of the sentence, the script identifies nodes whose dependency relation corresponds to a subject and whose governing node is a verb.\
For each such verb occurrence, the program records:
- whether the subject appears before or after the verb
- whether the verb is the head of a relative clause
### Detecting Subject Inversion
Subject inversion is defined as a configuration where the subject appears after the verb in the linear order of the sentence. \
This is determined by comparing the token positions: \
`subject_id` > `verb_id` \

If this condition holds, the subject is considered postverbal (inverted).

### Detecting Relative Clause Heads

The script then checks whether the verb heads a relative clause, which is indicated in the corpus by the dependency relation `mod.rel`. \
This allows the program to count how often verbs with nominal subjects occur in relative clauses.

### Estimating Probabilities

Once the counts are collected across all sentences, the script computes the following relative frequencies:

𝑃(𝐼𝑁𝑉) probability that a subject is postverbal. \
𝑃(𝑅𝐸𝐿) probability that a verb with a nominal subject heads a relative clause. \
𝑃(𝐼𝑁𝑉∩𝑅𝐸𝐿) probability that both conditions occur.

From these values, conditional probabilities can be derived:
Via restricting the set:

$$P(REL|INV) = \frac{P(REL \cap INV)}{P(INV)} = \frac{\frac{18}{1179}}{\frac{69}{1179}} = \frac{18}{69}$$ 

$$P(INV|REL) = \frac{P(INV \cap REL)}{P(REL)} = \frac{\frac{18}{1179}}{\frac{58}{1179}} = \frac{18}{58}$$

Via Bayes' Theorem

$$P(INV|REL) = \frac{P(REL|INV)\cdot P(INV)}{P(REL)} = \frac{\frac{18}{69}\cdot \frac{69}{1179}}{\frac{58}{1179}} = \frac{18}{58}$$

These probabilities provide an empirical estimate of how subject inversion interacts with relative clause structures in the corpus.
