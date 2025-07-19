FROM public.ecr.aws/lambda/python:3.11

# Copy requirements and install dependencies
COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install -r requirements.txt --target ${LAMBDA_TASK_ROOT}

# Copy application code
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

# Set the Lambda handler
CMD ["lambda_function.lambda_handler"]