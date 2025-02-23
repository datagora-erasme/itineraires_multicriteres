FROM python:3.11.11-bullseye

RUN apt update
RUN apt install gdal-bin -y

WORKDIR /app

COPY ./requirements.txt /app/
RUN pip install -r requirements.txt

COPY ./models/ /app/models

COPY ./score_calculation_it/input_data/bancs/bancs.json /app/score_calculation_it/input_data/bancs/bancs.json
COPY ./score_calculation_it/input_data/fontaines_ornementales/fontaines_ornementales.json /app/score_calculation_it/input_data/fontaines_ornementales/fontaines_ornementales.json
COPY ./score_calculation_it/input_data/fontaines_potables/fontaines_potables.json /app/score_calculation_it/input_data/fontaines_potables/fontaines_potables.json
COPY ./score_calculation_it/input_data/parcs/*.json /app/score_calculation_it/input_data/parcs/*.json
COPY ./score_calculation_it/input_data/toilettes/toilettes.json /app/score_calculation_it/input_data/toilettes/toilettes.json
COPY ./score_calculation_it/input_data/tourisme/*.json /app/score_calculation_it/input_data/tourisme/*.json

COPY ./score_calculation_it/output_data/network/graph/ /app/score_calculation_it/output_data/network/graph

COPY ./global_variable.py /app/
COPY ./load_graph.py /app/
COPY ./app.py /app/

CMD ["python", "app.py"]