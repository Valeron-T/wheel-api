from io import BytesIO

from cm import concatenate_tables_with_headers
from app.initialize import celery


@celery.task()
def example_task():
    # Write your task code here
    return "OK"


@celery.task()
def process_pdf(pdf_data):
    # This is a mock function for PDF processing
    # Replace it with your actual PDF processing logic
    print("Begin Processing pdf")

    res = concatenate_tables_with_headers(BytesIO(pdf_data))
    print(res)

    return "Processing complete"
