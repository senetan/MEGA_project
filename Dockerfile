FROM python:3.10.6

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY .env .env

COPY MEGA_project_folder MEGA_project_folder
COPY models/MEGA_model.h5 /root/code/senetan/MEGA_project/models/MEGA_model.keras
COPY models/features_pipeline.pkl /root/code/senetan/MEGA_project/models/features_pipeline.pkl
COPY models/target_scaler.pkl /root/code/senetan/MEGA_project/models/target_scaler.pkl
COPY notebook/df_de_merged_update_timeline.csv /root/code/senetan/MEGA_project/notebook/

CMD ["sh", "-c","uvicorn MEGA_project_folder.api_file:app --host 0.0.0.0 --port $PORT"]
