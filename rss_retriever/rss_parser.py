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
        if posts is None:
            print("No entries found in website ")
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
                    
                    img_content = requests.get(img_url)
                    temp["Picture"] = img_content.content
                except Exception as e:
                    pass

                temp["Tags"] = [tag.term for tag in  post[os.getenv("RSS_TAGS")]] 

                try:
                    temp["Summary"] = post[os.getenv("RSS_SUMMARY")]
                except Exception as e:
                    pass

                try:
                    query = "INSERT INTO news_data ({columns}) VALUES ({value_placeholders})".format(
                    columns=", ".join(temp.keys()),
                    value_placeholders=", ".join(["%s"] * len(temp)),
                    )

                    cursor.execute(query, list(temp.values()))
                    # print(list(temp.values()))
                except Exception as e:
                    print("Unable to insert data")
                    print(e)
                    conn.rollback()

                additions += 1
            except Exception as e: 
                print("No items with the format found")
                print(e)

        
        if additions>=1:
            conn.commit()
            print("New news detected and added")
        else:
            print("No new news detected")
            

              
    else: 
        return None
  
if __name__ == "__main__":
  print("Starting rss_parser") 
  while(True):
    feed_url = os.getenv("RSS_FEED_URL")
    add_feed_data(rss = feed_url) 
    time.sleep(int(os.getenv('RSS_POLL_TIME')))
