FROM public.ecr.aws/docker/library/python:3.9

RUN mkdir -p /src
WORKDIR /src

COPY requirements.txt /src/requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "re_enrich_music_works.py"]
