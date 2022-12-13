FROM umihico/aws-lambda-selenium-python:latest

# copy code to container
COPY ./src/etl.py ${LAMBDA_TASK_ROOT}

# install python dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# set the CMD to handler
CMD ["etl.indeed_scraper"]