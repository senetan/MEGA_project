FROM python:3.10.6

COPY . /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY MEGA_project_folder /root/code/senetan/MEGA_project_folder
COPY models /root/code/senetan/MEGA_project/models

ENV MODEL_PATH=/root/code/senetan/MEGA_project/models/MEGA_model.h5
ENV PIPELINE_PATH=/root/code/senetan/MEGA_project/models/MEGA_model.pkl

CMD uvicorn MEGA_project_folder.api_file:app --host 0.0.0.0
