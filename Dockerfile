FROM python:alpine

ENV LANG zh_CN.UTF-8
ENV LANGUAGE zh_CN:zh
ENV LC_ALL zh_CN.UTF-8

ARG project_dir=/projects/
WORKDIR $project_dir

ADD requirements.txt $project_dir
ADD app.py $project_dir
ADD config $project_dir
ADD dc $project_dir

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "-m flask", "run", "-p 8080"]