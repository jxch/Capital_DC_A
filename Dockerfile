FROM python:slim

ENV LANG zh_CN.UTF-8
ENV LANGUAGE zh_CN:zh
ENV LC_ALL zh_CN.UTF-8

ARG project_dir=/projects/
WORKDIR $project_dir

ADD requirements.txt $project_dir
ADD app.py $project_dir
ADD env.sh $project_dir
ADD product.sh $project_dir
ADD config $project_dir
ADD dc $project_dir

RUN apk update && apk add build-base
RUN pip install -r requirements.txt --ignore-installed
RUN ./product.sh

EXPOSE 11002
ENTRYPOINT ["python", "-m flask", "run", "-p 11002 --host=0.0.0.0"]