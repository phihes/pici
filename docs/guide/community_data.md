# Community data collection

### Basic Principles	

The toolbox makes online forums usable as a data source for the investigation of peer communities. 
For further processing, the Toolbox requires a certain data structure that records the time of contribution, the text, a unique contributor and the associated thread for each forum post. Each forum post forms a data point.
The data model links the table of individual contributions (posts) with a table of contributors (authors) and a table with information on the discussion threads. The three data tables form the basis for the analysis of online interactions in peer communities. 

The data required to evaluate the forums of peer communities can be loaded using two approaches. 

## Loading data from file

The data tables are available as files. The static file must correspond to the [specified data structure](pici/docs/guide/indicators):

- contribution meta data: contributor, date, associated thread, position in thread, sub-forum
- contribution content: text, html, extracted links, images
- contributor properties: name/id
- thread: title

## Loading data dynamically

Alternatively, the data can be loaded dynamically from publicly accessible online forums via web scraping, database or other interface (API).
Thereby, appropriate adjustments must be made for each new data source. If the data of the forums of several communities are structured in the same way, e.g. because they use the same forum software (e.g. Discourse), they can be collected with a comprehensive query. 

### Example from [Peer Innovation research project](https://www.peer-innovation.de/)

For the research project, data was collected from the online forums of three peer communities to analyse their innovation activities: [Precious Plastic](https://davehakkens.nl/community/forums/forum/precious-plastic/index.html), [OpenEnergyMonitor](https://community.openenergymonitor.org/) and [OpenStreetMap](https://forum.openstreetmap.org/index.php). 
All contributions in the forums of the communities were scrapped and analysed for the period from 01/2017 to 12/2019.
In total, the data set comprises more than 200,000 contributions (in 20,000 threads) from 12,000 users.
In the three communities examined, the dynamic data links have already been created. Thus, new data of the community forums can be loaded automatically from the internet on a regular basis. 
