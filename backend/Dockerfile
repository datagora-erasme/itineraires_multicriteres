FROM python:3.10.8-buster

RUN apt update
RUN apt install gdal-bin -y

WORKDIR /app

COPY ./requirements.txt /app/
RUN pip install -r requirements.txt

COPY ./models/ /app/models
# COPY ./script_python/ /app/script_python
COPY ./score_calculation_it/input_data /app/score_calculation_it/input_data
COPY ./score_calculation_it/input_data/fetch_data_docker.py /app/score_calculation_it/input_data/fetch_data_docker.py
#COPY ./score_calculation_it/output_data/network/graph/final_network_bounding_scaled_no_na.gpkg /app/score_calculation_it/output_data/network/graph/final_network_bounding_scaled_no_na.gpkg
COPY ./score_calculation_it/output_data/network/graph/final_network_P0_01O5At0_01Ar10C0_01E5Ca.gpkg /app/score_calculation_it/output_data/network/graph/final_network_P0_01O5At0_01Ar10C0_01E5Ca.gpkg
# COPY ./data/geojson /app/data/geojson
# COPY ./data_informations.json /app/data_informations.json
# COPY ./raw_data/ /app/raw_data

COPY ./global_variable.py /app/
COPY ./calculate_itinerary.py /app/
COPY ./load_graph.py /app/
COPY ./app.py /app/

#CMD ["Flask", "run", "-h", "0.0.0.0", "-p", "3002",]
# RUN cd  /app/score_calculation_it/input_data/ && python3 ./app/score_calculation_it/input_data/fetch_data_docker.py

# CMD ["python", "./score_calculation_it/input_data/fetch_data_docker.py"]
# CMD ["sh", "-c", "python ./score_calculation_it/input_data/fetch_data_docker.py && python app.py"]

CMD ["python", "app.py"]
