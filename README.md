
# farnamstreetPageRank 
FarnamStreet is the first website that introduce to me the concept of **multidiscipline thinking** and **mental models** learning.   
  
To maximize the value of this blog, I need to figure out the highest valueable articles to read first. And more, I need to analyse the relationship between concepts and pages so that I can explore the world of super-thinking easier.  
    
This tool will crawl the [fs.blog](fs.blog) website and build a graph between all pages, so that you could use any graphy-analysis tool of your choice to find most valuable knowledge.  
    
# How to run the crawler    
 ## First install Scrapy 

    $ sudo apt install python3 python3-pip python3-venv  
    
## Install crawler requirements  

    $ git clone https://github.com/vantt/farnamstreetPageRank  
    $ cd farnamstreetPageRank/crawler 
    
    $ python3 -m venv env  
    $ source env/bin/activate  
    $ pip3 install -r requirements.txt  

  
## Run Crawler  
### First run the crawler:  

    $ ./runspider.sh  

  
### Build Graph data  

    $ ./rebuild_graph.py  

  
crawling data and final graph data will be put in **[data]** folder

## Graph Analysis

