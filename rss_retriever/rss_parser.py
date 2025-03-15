import psycopg2
import os
import feedparser
import requests
import time



def create_conn():
    conn = psycopg2.connect(
    database=os.getenv("PGDATABASE"), user=os.getenv("PGUSER"), password=os.getenv("PGPASSWORD"), host='postgres'
    )
    return conn


def add_feed_data(rss=None): 
    
    """ 
    Take link of rss feed as argument 
    """
    if rss is not None: 

        blog_feed = feedparser.parse(rss) 
        posts = blog_feed.entries

        conn = create_conn()
        cursor = conn.cursor()

        additions = 0

        for post in posts: 
            # print(post)
            temp = dict() 
              
            try: 
                temp["Title"] = post[os.getenv("RSS_TITLE")] 
                temp["Weblink"] =  [link.href for link in post[os.getenv("RSS_LINK")]][0]
                temp["Pub_timestamp"] =  post[os.getenv("RSS_DATE_TIME")] 

                try:
                    # ll
                    img_url = post[os.getenv("RSS_IMAGE")][0][os.getenv("RSS_IMAGE_URL")]
                    
                    if(len(post[os.getenv("RSS_IMAGE")])>1):
                        print("Multiple images found")
                    img_content = requests.get(img_url)
                    temp["Picture"] = img_content.content
                except:
                    print("No image found")

                temp["Tags"] = [tag.term for tag in  post[os.getenv("RSS_TAGS")]] 

                try:
                    temp["Summary"] = post[os.getenv("RSS_SUMMARY")]
                except:
                    print("No summary found")

                try:
                    query = "INSERT INTO news_data ({columns}) VALUES ({value_placeholders})".format(
                    columns=", ".join(temp.keys()),
                    value_placeholders=", ".join(["%s"] * len(temp)),
                    )

                    cursor.execute(query, list(temp.values()))
                    print(list(temp.values()))
                except:
                    print("Unable to insert")

                additions += 1
            except: 
                print("No items with the format found")

        
        if additions>=1:
            conn.commit()
            print("More than 1 news")
            

              
    else: 
        return None
  
if __name__ == "__main__":
  print("Starting rss_parser") 
  while(True):
    feed_url = os.getenv("RSS_FEED_URL")
    add_feed_data(rss = feed_url) 
    time.sleep(600)
