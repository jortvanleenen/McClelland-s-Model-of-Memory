# McClelland's Model of Memory
## The Model
The model proposed by McClelland \[1] suggests that generalisations are not stored in the human mind, but specific objects or events, from which we can then deduce generalisations by seeing how these entities relate to one another. Within the model, each entity is referred to by an _instance node_, whereas all properties of these entities are referred to by _property nodes_. We group all mutually exclusive properties in inhibitory sets; if one of the properties within such a set is active, it tries to inhibit the other present properties. Additionally, we bidirectionally connect all directly related nodes, representing excitatory connections. For example, if an object is a brown chair, we would connect the instance node "chair" to the property node "brown".

## Implementation Detail
To calculate the inhibitory connections, we are interested in efficiently querying all neighbours of a node; in this case its inhibitory neighbours. The group of nodes that form inhibitory connections to each other are sets of mutually exclusive properties, e.g. a group of colours, age ranges, marriage status, etc.. Within the given CSV file, these groups of properties are placed after each other, resulting in _column blocks_. Two examples: the first 27 columns (a column block) represent the inhibitory set of instance nodes and the next 2 (another column block) represent the inhibitory set for the property of gang alliance.

## Reference
\[1]: McClelland, J. L. (1981). Retrieving general and specific information from stored knowledge of specifics. In Proceedings of the annual meeting of the cognitive science society (Vol. 3) ([https://escholarship.org/content/qt9qr1n7jv/qt9qr1n7jv.pdf](https://escholarship.org/content/qt9qr1n7jv/qt9qr1n7jv.pdf))
