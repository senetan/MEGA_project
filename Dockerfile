FROM python:3.10-slim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY MEGA_project_folder MEGA_project_folder
COPY models models

CMD uvicorn MEGA_project_folder.api_file:app --host 0.0.0.0
