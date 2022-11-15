# User guide

<p align="center">
    <img src="../images/structure.png" width="1200px" style="width: 100%; max-width:1200px; min-width:400px;" />
</p>


## Community data collection

#### Concept

The toolbox makes use of online forums as a data source for the investigation of peer communities. 
For further processing, the Toolbox requires a certain data structure that records the time of contribution, the text, a unique contributor and the associated thread for each forum post, where each post forms a data point.
The data model links the table of individual contributions (posts) with a table of contributors (authors) and a table with information on the discussion threads. The three data tables form the basis for the analysis of online interactions in peer communities. 
The data required can be obtained using two approaches: Loading the data dynamically or from a static file. 
The data tables available as files correspond to the [specified data structure](../../../indicators).
Alternatively, the data can be loaded dynamically from publicly accessible online forums via web scraping, a database or another interface (API).
Thereby, appropriate adjustments must be made for each new data source. If the data of the forums of several communities are structured in the same way, e.g. because they use the same forum software (e.g. Discourse), they can be collected with a comprehensive query. 

#### Example of [Peer Innovation research project](https://www.peer-innovation.de/)

For the research project, data was collected from the online forums of three peer communities to analyse their innovation activities: [Precious Plastic](https://davehakkens.nl/community/forums/forum/precious-plastic/index.html), [OpenEnergyMonitor](https://community.openenergymonitor.org/) and [OpenStreetMap](https://forum.openstreetmap.org/index.php). 
All contributions in the forums of the communities were scrapped and analysed for the period from 01/2017 to 12/2019.
In total, the data set comprises more than 200,000 contributions (in 20,000 threads) from 12,000 users.
In the three communities examined, the dynamic data links have already been created. Thus, new data of the community forums can be loaded automatically from the internet on a regular basis. 

## Data preprocessing (Calculation of Networks)

#### Concept

Based on the forum data, the toolbox calculates two different interaction networks: Directed and undirected network relationships between contributors. 
Thus, for the calculation of network metrics, different graphs are created, where the nodes of the networks refer to the contributors in the online forum, and the edges represent their interactions. 

In this context, a distinction is made between co-contributors and commentators. The co-contributor network considers which contributors contribute to the same discussion (thread). There is an undirected relationship between two contributors sharing participation in a thread. The strength of the relationship increases with the number of threads shared. In contrast, the commenter network maps the contributions to discussions initiated by others. There is a directed relationship between commentators and the initial contributor of a thread. The strength of a relationship between two forum contributors increases with the number of comments by one contributor to the other's initial contributions.

#### Example of [Peer Innovation research project](https://www.peer-innovation.de/)

The research project examines online forum discussion threads as measurable manifestations of knowledge exchange in peer communities. The co-contributor networks map which community members exchange information with each other. The pooling of distributed knowledge and the recombination of experiences from different fields is considered a basic mechanism for the emergence of innovative ideas. The commenter network, on the other hand, maps directed knowledge flows within the peer community. Here, the focus is on who receives information and through whom. From this, conclusions can be drawn about the position of certain members and the significance of their contributions to the community.

#### Extension possibilities
There are other rules of network formation possible. For example, the respective positions of the posts in the threads could be taken into account. Furthermore, the contributors could be differentiated between established members and newcomers based on their previous history to examine community entry [^1]. Expanding the toolbox to include other network types is possible, but requires modification of the code.

## Data labelling 

#### Concept

A part of the data set must be labelled so that the supervised classification algorithm can be trained with it. For this part of the data, the relevance of the forum content must be defined, because the performance of the indicators is measured by this ground truth. The training data set can be created in different ways. 
	
#### Example of [Peer Innovation research project](https://www.peer-innovation.de/) 

The research project investigated how peer communities drive sustainable innovation. For this purpose, those processes were determined, which provide information about the further development and dissemination of sustainable technologies by the community. In the forum discussions, there is evidence of activities with which community members contribute to the innovation process: not only sharing blueprints and designs, but also testing and evaluating technical solutions, and pointing out alternatives or ways to overcome difficulties in implementation. So with the training dataset, the toolbox should detect indications of these multiple activities.
The assessment of the prevalence of innovation activities and the innovation potential of the threads' content was manually conducted by the project team and outsourced using an online survey. For this purpose, rules were first defined [^3], according to which the evaluators assigned labels to the threads. The evaluated threads were then used as training data for validating the suitability of the various metrics for identifying peer innovation. The quality of the training data can be assessed using interrator agreement metrics. In case of labeller disagreements, it was necessary to apply a rule on which labels to choose to finalize the shape of the training data.

#### Extension possibilities 

The classification of forum content could also be based on completely different criteria, depending on the research interest and application context. As indications of innovation activities or innovation potential, other content-related criteria could be used for labelling as well, and labelling could also be carried out at other observation levels than the thread. For example, individual forum posts could also be evaluated. Furthermore, other innovation aspects than activities such as innovation inputs and outcomes could be focused on for identifying peer innovation. 

## Indicator generation 

#### Concept

The indicator metrics implemented in the toolbox stem from the literature analysis conducted in the [Peer Innovation project](https://www.peer-innovation.de/) in the research context of open innovation and user innovation [^2]. These metrics are each assigned to different observation levels (initial idea, feedback, interaction). When adding further metrics, it must be taken into account to which level the new metric refers. An overview of the current implementations can be found [here](../../indicators).

#### Example of [Peer Innovation research project](https://www.peer-innovation.de/)

The research project aims to validate suitable indicators for innovation activities in peer communities. Metrics that are associated with the occurrence of innovations in the research literature [^2] are therefore calculated at the different observation levels. These metrics then can identify threads that contain indications of relevant activities, such as presenting, evaluating, implementing, modifying and improving innovative ideas.

#### Extension possibilities 

Furthermore, additional metrics can be added to the toolbox by extending the indicator library. The procedure is explained in the [Examples for Creating a custom indicator](../../Examples/Creating a custom indicator.ipynb). A new metric must then be defined at the respective observation level. For example, additional text-based indicators could focus on certain keywords in the contributions or mark certain features in the contributors' response behaviour.

## Indicator evaluation  

#### Concept

Using supvervised machine learning, the performance of the indicator metrics in classifying forum content is evaluated based on the training dataset. In this way, suitable indicators and their best possible combination are selected for the automated detection of relevant content in the community forum.
The toolbox uses various machine learning techniques to train classification models that combine the most suitable metrics for classifying forum content.

#### Example of [Peer Innovation research project](https://www.peer-innovation.de/) 

In the research project, the classification algorithm was trained with the manually labelled threads. 

In this way, the previously generated metrics could be validated in terms of how well they can predict the occurrence of innovation activities in discussion threads.



[^1]: Paxton, A., Varoquaux, N., Holdgraf, C., & Geiger, R. S. (2022). Community, Time, and (Con) text: A Dynamical Systems Analysis of Online Communication and Community Health among Open‐Source Software Communities. Cognitive Science, 46(5), e13134.

[^2]: Pohlisch, J. (2021). Measuring household sector innovation in online communities (Working Paper).

[^3]: Heß, P., & Gleu, A. (2022). Measuring peer innovation in online communities: Discussion pa-per for the expert workshop "How innovative are peer communities? Approaches to the empiri-cal assessment of peer innovation" on 14 January 2022.
