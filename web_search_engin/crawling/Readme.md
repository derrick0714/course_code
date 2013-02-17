# Simple Crawler
The first project for Web Search Engine

<img src="https://raw.github.com/derrick0714/web_search_engin/master/crawling/docs/crawler_architecture.png" />
##Core
The core roles in crawler.

###Engine

The engine is responsible for controlling the data flow between all components of the system, and triggering events when certain actions occur. See the Data Flow section below for more details.

##Include
The common & base classes work for whole project

###Setting
In charge of reading and writing setting files, the setting files format show as blow:
```
[queue]
length = 500

#some annotation
[thread]
downloader = 10
parser = 5

[Strategies]
black_holds = enable
different_names = enable


...
```

###Log
In charge of writing log to screen or files

###Status
In charge of management all status such as runtime, donwload pages, duplicate detective times and etc. Meanwhile wirte theses data into files or remote mysql in realtime.

###Strategies

###Thread Poll


##Models

##Strategies
