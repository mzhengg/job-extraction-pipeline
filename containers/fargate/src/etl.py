import random
import string
from datetime import date
from tempfile import mkdtemp
import os

from selenium import webdriver
from selenium.webdriver.common.by import By

import boto3

import psycopg2

# have to set a bunch of options for headless chrome driver to work on lambda
options = webdriver.ChromeOptions()
options.binary_location = '/opt/chrome/chrome'
options.add_argument('--user-agent="Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166"')
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1280x1696")
options.add_argument("--single-process")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-dev-tools")
options.add_argument("--no-zygote")
options.add_argument(f"--user-data-dir={mkdtemp()}")
options.add_argument(f"--data-path={mkdtemp()}")
options.add_argument(f"--disk-cache-dir={mkdtemp()}")
options.add_argument("--remote-debugging-port=9222")

# get from variables.tf: "aws_s3_bucket_name"
bucket_name = os.getenv('AWS_S3_BUCKET_NAME')
# get from variables.tf: "aws_redshift_db_name"
db_name = os.getenv('AWS_REDSHIFT_DATABASE_NAME')
# get from variables.tf: "aws_redshift_master_username"
username = os.getenv('AWS_REDSHIFT_MASTER_USERNAME')
# get from variables.tf: "aws_redshift_master_password"
password = os.getenv('AWS_REDSHIFT_MASTER_PASSWORD')
# get from AWS console -> Redshift -> Clusters -> Port
port = os.getenv('AWS_REDSHIFT_PORT')
# get from AWS console -> Redshift -> Clusters -> Endpoint (remove port and db)
host = os.getenv('AWS_REDSHIFT_HOST')

# jobs to scrape
jobs = [['software engineer', '', 1]]

def get_page_links(job, location, no_of_pages):
    # modify url to include job
    job = job.replace(' ', '%20')
    url = f'https://www.indeed.com/jobs?q={job}'

    # modify url to include job and location
    location = location.replace(' ', '%20')
    url = url + f'&l={location}'

    # links for each page to be scraped
    page_links = []

    for page in range(no_of_pages):
        page_links.append(url + f'&start={page*10}')

    return page_links

def get_job_links(page_links):
    # initializes chrome driver
    driver = webdriver.Chrome("/opt/chromedriver", options=options)
    
    # list of all href links from all the pages
    links = []
    
    # list of all job links from all the pages 
    job_links = []
    
    # cycle through each page of indeed
    for link in page_links:
        # opens the link 
        driver.get(link)

        # list of all elements on the page with <a>
        elements = driver.find_elements(By.TAG_NAME, 'a')
    
        # finds the href link in each <a> element
        for element in elements:
            link = element.get_attribute('href')
            links.append(link)
      
      # filter the links by job links
        for link in links:
            if link is None:
                continue
        
            if 'clk?' in link:
                job_links.append(link)

    # make sure that job links are being scraped
    if len(job_links) == 0:
        print("No links were scraped")

    return job_links

def scraper(job_link):
    # initializes chrome driver
    driver = webdriver.Chrome("/opt/chromedriver", options=options)

    # opens the url
    driver.get(job_link)
    
    # return all the text on the page
    job_info = driver.find_element(By.TAG_NAME, 'body').text

    return job_info

def upload_to_s3(job_links, bucket_name, directory):
    # connection to s3
    s3_client = boto3.client('s3')

    # list of scraped job postings
    job_posts = []

    # scrape information from each job post
    for link in job_links:
        # raw file to be uploaded
        scraped_posting = scraper(link)

        # append scraped_posting to job_posts for further processing later
        job_posts.append(scraped_posting)

        # file name for scraped posting
        file_name = ''.join(random.choices(string.ascii_letters, k=20))

        # uploads raw job post file to s3 bucket
        s3_client.put_object(Bucket=bucket_name, Body=scraped_posting, Key=f'{directory}/{file_name}.txt')
    
    return job_posts

def transformer(job_posts):
    # list of processed job posts
    processed_job_posts = []

    # process each job_post
    for job_post in job_posts:
        # split job_post by new line character
        job_post = job_post.split('\n')

        # get job title
        job_title = job_post[12]

        # get scraped date (DD/MM/YYYY)
        today = date.today()
        scraped_date = today.strftime("%Y/%m/%d")
        
        # dataframe containing job information
        job_info = [job_title, scraped_date]

        # append job_info to processed_job_posts
        processed_job_posts.append(job_info)

    return processed_job_posts

def upload_to_redshift(processed_job_posts):
    # information to connect to redshift
    connection_string = f"dbname={db_name} port={port} user={username} password={password} host={host}"

    # establish connection to redshift
    connection = psycopg2.connect(connection_string)

    # object to execute commands in redshift database
    cursor = connection.cursor()

    # create table if it doesn't already exist
    query = 'CREATE TABLE IF NOT EXISTS jobs (job_title VARCHAR(200), scraped_date DATE);'
    cursor.execute(query)

    # insert each processed_job_post into the redshift table
    for processed_job_post in processed_job_posts:
        # insert query
        query = f"INSERT INTO jobs (job_title, scraped_date) VALUES ('{processed_job_post[0]}', '{processed_job_post[1]}');"
        cursor.execute(query)

    # cursor.execute('SELECT * FROM jobs;')
    # print(cursor.fetchall())

    connection.close()

# this is the lambda_handler function, which takes two parameters: 'event' and 'context'
# 'event' and 'context' are just placeholder parameters
def indeed_scraper(event, context):
    # scrape postings for each 'job' type
    for job in jobs:
        page_links = get_page_links(job[0], job[1], job[2])
        job_links = get_job_links(page_links)
        job_posts = upload_to_s3(job_links, bucket_name, job[0])
        processed_job_posts = transformer(job_posts)
        upload_to_redshift(processed_job_posts)

if __name__ == '__main__':
    # normally, the parameters are passed to the function when we use the lambda emulator via the command line
    # however, we simply pass in the 'jobs' variable of this script into the function and ignore 'event' and 'context'
    event = None
    context = None

    indeed_scraper(event, context)