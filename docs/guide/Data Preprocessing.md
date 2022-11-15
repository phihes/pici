# Data preprocessing (Calculation of networks) 

The toolbox calculates interaction networks based on forum data. Directed and undirected network relationships between contributors are considered. 
Thus, different graphs are created for the calculation of network metrics.
	
Two different interaction networks are calculated from the forum data. The nodes of the networks form the participants in the online forum, the edges represent their interactions. 
A distinction is made between contributors and commentators. 
The contributor network considers which forum participants contribute to the same discussions. 
There is an undirected relationship between two contributors to the same thread. 
The strength of the relationship increases with the number of threads shared. 
In contrast, the comment network maps who contributes to discussions opened by others. 
There is a directed relationship of contributors to the founder of a thread. 
The strength of a relationship between two forum participants increases with the number of comments by one person on the other's initial contributions.
[Graphic Philipp: Network Types] 

### Example from PI 
The research project examines online forum discussion threads as measurable manifestations of knowledge exchange in peer communities. 
The contributor networks map which community members exchange information with each other. 
The pooling of distributed knowledge and the recombination of experiences from different fields is considered a basic mechanism for the emergence of innovative ideas. 
The commentator network, on the other hand, maps directed knowledge flows within the peer community. 
Here, the focus is on who receives information and through whom. From this, conclusions can be drawn about the position of certain members and the significance of their contributions within the community.

### Extension possibilities 
Other rules of network formation are conceivable and possibly revealing. 
For example, the respective positions of the posts in the threads could be taken into account or the contributors could be differentiated into members and newcomers on the basis of their previous history in order to examine the entry into the community (e.g. Paxton et al. 2022). 
Expanding the toolbox to include other network types is possible, but requires modification of the code. 
