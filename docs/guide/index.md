# User guide

<p align="center">
    <img src="../images/structure.png" width="1200px" style="width: 100%; max-width:1200px; min-width:400px;" />
</p>

## Community data collection

### Basic Principles	

The toolbox makes use of online forums as a data source for the investigation of peer communities. 
For further processing, the Toolbox requires a certain data structure that records the time of contribution, the text, a unique contributor and the associated thread for each forum post, where each post forms a data point.
The data model links the table of individual contributions (posts) with a table of contributors (authors) and a table with information on the discussion threads. The three data tables form the basis for the analysis of online interactions in peer communities. 
The data required can be obtained using two approaches: Loading the data dynamically or from a static file. 
The data tables available as files correspond to the [specified data structure](pici/docs/guide/indicators).
Alternatively, the data can be loaded dynamically from publicly accessible online forums via web scraping, a database or another interface (API).
Thereby, appropriate adjustments must be made for each new data source. If the data of the forums of several communities are structured in the same way, e.g. because they use the same forum software (e.g. Discourse), they can be collected with a comprehensive query. 

### Example of [Peer Innovation research project](https://www.peer-innovation.de/)

For the research project, data was collected from the online forums of three peer communities to analyse their innovation activities: [Precious Plastic](https://davehakkens.nl/community/forums/forum/precious-plastic/index.html), [OpenEnergyMonitor](https://community.openenergymonitor.org/) and [OpenStreetMap](https://forum.openstreetmap.org/index.php). 
All contributions in the forums of the communities were scrapped and analysed for the period from 01/2017 to 12/2019.
In total, the data set comprises more than 200,000 contributions (in 20,000 threads) from 12,000 users.
In the three communities examined, the dynamic data links have already been created. Thus, new data of the community forums can be loaded automatically from the internet on a regular basis. 

## Data preprocessing (Calculation of networks)

Based on the forum data, the toolbox calculates two different interaction networks: Directed and undirected network relationships between contributors. 
Thus, for the calculation of network metrics, different graphs are created, where the nodes of the networks refer to the contributors in the online forum, and the edges represent their interactions. 

In this context, a distinction is made between co-contributors and commentators. The co-contributor network considers which contributors contribute to the same discussion (thread). There is an undirected relationship between two contributors sharing participation in a thread. The strength of the relationship increases with the number of threads shared. In contrast, the commenter network maps the contributions to discussions initiated by others. There is a directed relationship between commentators and the initial contributor of a thread. The strength of a relationship between two forum contributors increases with the number of comments by one contributor to the other's initial contributions.

### Example of [Peer Innovation research project](https://www.peer-innovation.de/)

The research project examines online forum discussion threads as measurable manifestations of knowledge exchange in peer communities. The co-contributor networks map which community members exchange information with each other. The pooling of distributed knowledge and the recombination of experiences from different fields is considered a basic mechanism for the emergence of innovative ideas. The commenter network, on the other hand, maps directed knowledge flows within the peer community. Here, the focus is on who receives information and through whom. From this, conclusions can be drawn about the position of certain members and the significance of their contributions to the community.

### Extension possibilities
There are other rules of network formation possible. For example, the respective positions of the posts in the threads could be taken into account. Furthermore, the contributors could be differentiated between established members and newcomers based on their previous history to examine community entry [^1]. Expanding the toolbox to include other network types is possible, but requires modification of the code.

## Indicator generation 

The indicator metrics implemented in the toolbox are fed from the literature analysis conducted in the [Peer Innovation research project](https://www.peer-innovation.de/) in the research context of open innovation and user innovation [^2]. These metrics are each assigned to different observation levels. When adding further metrics, it must be taken into account at which level the new metric is to be located. An overview of the current implementations can be found here.
[Graphic PI-AB 2 or slide from BMBF workshop]
	Example from PI The research project aims to develop suitable indicators for innovation activities in peer communities. Metrics that are associated with the occurrence of innovations in the research literature are therefore calculated at the different observation levels (Pohlisch et al. 2021). With the help of these metrics, threads in the online forum will then be identified that contain indications of relevant community activities, such as presenting, evaluating, implementing, modifying and improving innovative ideas.
	Extension possibilities Furthermore, additional metrics can be added to the toolbox by extending the indicator library. The procedure is explained in the online manual [link]. A new method must then be defined at the respective observation level, which can be called like metrics that have already been implemented. For example, additional text-based indicators could focus on certain keywords in the contributions or mark certain features in the contributors' response behaviour.



[^1]: Paxton, A., Varoquaux, N., Holdgraf, C., & Geiger, R. S. (2022). Community, Time, and (Con) text: A Dynamical Systems Analysis of Online Communication and Community Health among Open‐Source Software Communities. Cognitive Science, 46(5), e13134.

[^2]: Pohlisch, J. (2021). Measuring household sector innovation in online communities (Working Paper).
