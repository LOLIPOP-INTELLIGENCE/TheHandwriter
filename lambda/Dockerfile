FROM public.ecr.aws/lambda/python:3.9

# Copy requirements.txt
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Copy function code
COPY generate.py ${LAMBDA_TASK_ROOT}

# Install the specified packages
RUN pip install -r requirements.txt

# Copy media folder
COPY media ${LAMBDA_TASK_ROOT}/media

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "generate.lambda_handler" ]