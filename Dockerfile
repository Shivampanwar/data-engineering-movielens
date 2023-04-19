FROM python:3.8

EXPOSE 4200


COPY  requirement.txt . 

RUN pip install -r requirement.txt

# RUN cat requirements.txt | xargs -n 1 pip install

RUN mkdir project-folder

COPY  . /project-folder


CMD ["sh", "-c", "python /project-folder/prefect/full_prefect_flow.py && prefect orion start"]
