## Tasks overview ##
- A common <i>postgres</i> service is run which will be used by all the other services with a <i>db_env</i> file set up for authorization.
- The logs of this service alone are disabled to prevent unnecessary logging of 'INSERT INTO' statements.
- <b>Task 1</b>:
    - A service <i>db_init</i> is created for the purpose of this task.
    - A <i>db_env</i> file is setup for accesing the <i>postgres</i> database.
    - This is run as a separate service to let postgres start before any other commands.
    - We make use of the <i>depends_on</i> feature for this purpose.
    - We use <i>executer.sh</i> shell script to wait for the server to get ready to accept commands(<i>depends_on</i> only cares about building).
    - We then use the same script to execute statements in <i>table.sql</i> script.
    - Primary key is enforced on <i>Title</i>. We can't enforce it on the published date because it's a timestamp now.
- <b>Task 2</b>:
    - A python script <i>rss_parser.py</i> is executed upon startup which takes in RSS feed and inserts into database.
    - <i>feedparser</i> library is used to parse the feeds and <i>psycopg</i> library is used to connect and insert.
    - The image is downloaded and stored as <i>BYTEA</i> object.
    - Print statements log the exceptions and status if necessary and the same can be viewed in docker logs.
- <b>Task 3</b>
    - A docker-compose file is set up in the home directory, which takes care of all the containerized applications.
- <b>Brownie</b>
    - The brownie service is set up as an additional service in compose file.
    - The data is retrieved from the database using <i>psycopg</i> and converted to HTML.
    - The images are <i>base_64</i> encoded and then put inside <i>img</i> tag.
    - The <i>Title</i> and <i>Picture</i> are embedded with hyperlinks from the <i>Weblink</i> we extracted, using <i>href</i> tag.
    - With some styling, the data is then fed to a server upon <i>get</i> request.
    - <i>Fastapi</i> with <i>uvicorn</i> provide the necessary facilities for hosting a server.

## Steps to run ##
  ```bash
  docker compose up #yep, that's it
