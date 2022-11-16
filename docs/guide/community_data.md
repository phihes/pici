# Community data collection

### Basic Principles	

The toolbox makes online forums usable as a data source for the investigation of peer communities. 
The data required to evaluate the forums can be loaded using two approaches. 

## Loading data from file

The data tables are available as files. The static file must correspond to the [specified data structure](pici/docs/guide/indicators):

- contribution meta data: contributor, date, associated thread, position in thread, sub-forum
- contribution content: text, html, extracted links, images
- contributor properties: name/id
- thread: title

## Loading data dynamically

Alternatively, the data can be loaded dynamically from publicly accessible online forums via web scraping, database or other interface (API).
Thereby, appropriate adjustments must be made for each new data source. If the data of the forums of several communities are structured in the same way, e.g. because they use the same forum software (e.g. Discourse), they can be collected with a comprehensive query. 
