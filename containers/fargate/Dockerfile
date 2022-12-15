FROM umihico/aws-lambda-selenium-python:latest

# copy code to container
COPY ./src/etl.py ${LAMBDA_TASK_ROOT}

# copy .env to container
COPY ./.env ${LAMBDA_TASK_ROOT}

# install python dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# set CMD to handler
CMD ["etl.indeed_scraper"]

# execute script when container starts
ENTRYPOINT ["python3", "etl.py"]