from fastapi import FastAPI
import os
import pandas as pd
from fastapi.responses import HTMLResponse
import psycopg2
import uvicorn
from datetime import datetime
import base64

app = FastAPI()

def create_conn():
    conn = psycopg2.connect(
    database=os.getenv("PGDATABASE"), user=os.getenv("PGUSER"), password=os.getenv("PGPASSWORD"), host='postgres'
    )
    return conn

# sql_query = f"SELECT title FROM {os.getenv('PGTABLE')};"
def image_to_base64(image_data):
    return base64.b64encode(image_data).decode('utf-8')

@app.get("/read_table",response_class=HTMLResponse)
async def read_table(date:str = None):
    try:
    # Establish a connection to the database using service principal authentication
        conn = create_conn()
        cursor = conn.cursor()
        html_table = ""

        if date:
            # Ensure the date is in the correct format (YYYY-MM-DD)
            try:
                date_obj = datetime.strptime(date, '%Y-%m-%d')
                sql_query = f"SELECT Title, Picture, Summary, Weblink FROM {os.getenv('PGTABLE')} \
                            WHERE CAST(Pub_timestamp AS DATE) = %s;"
                cursor.execute(sql_query, (date_obj,))
            except ValueError:
                return HTMLResponse(content="<h1>Error: Invalid date format. Use YYYY-MM-DD.</h1>", status_code=400)
        else:
            sql_query = f"SELECT Title, Picture, Summary, Weblink FROM {os.getenv('PGTABLE')};"
            cursor.execute(sql_query)

        output = cursor.fetchall()

        if output is None:
            return HTMLResponse(content=f"<h1>No data in table</h1>", status_code=500)

        columns = ["Title", "Picture", "Summary", "Weblink"]
        df = pd.DataFrame(output, columns = columns)

        df['Picture'] = df['Picture'].apply(lambda x: f"<img src='data:image/jpeg;base64,{image_to_base64(x)}' style='max-width:150px; max-height:150px;' />" if x else "")

        df['Title'] = df.apply(lambda row: f"<a href = {row['Weblink']}>{row['Title']}</a>", axis = 1)
        df['Picture'] = df.apply(lambda row: f"<a href = {row['Weblink']}>{row['Picture']}</a>", axis = 1)

        df = df.drop(columns=['Weblink'])

        html_table = df.to_html(index=False, escape=False)
        html_table = html_table.replace('<th>', '<th style="text-align: center;">')
        html_table = html_table.replace('<td>', '<td style="text-align:center;">')
        html_table = html_table.replace('<img', '<img style="max-width:150px; max-height:150px;"')  
        
        table = "NEWS FOR YOU"
        html_table = f"<h2 style='text-align: center;'><b>{table}</b></h2>" + html_table

        cursor.close()
        conn.close()
        return HTMLResponse(content=html_table, status_code=200)  

    except Exception as e:
        return HTMLResponse(content=f"<h1>Error: {str(e)}</h1>", status_code=500)

uvicorn.run(app, host='0.0.0.0', port=7000)

