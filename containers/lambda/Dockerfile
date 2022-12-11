#FROM public.ecr.aws/lambda/python:3.8
FROM umihico/aws-lambda-selenium-python:latest

# copy code to container
COPY ./src/etl.py ${LAMBDA_TASK_ROOT}

# install function dependencies using requirements.txt
COPY requirements.txt .
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# set the CMD to your handler
CMD ["etl.indeed_scraper"]