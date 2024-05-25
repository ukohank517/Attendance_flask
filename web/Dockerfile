FROM python:3.6
ARG work_dir=/work/mysql_flask

WORKDIR $work_dir/

COPY conf/ $work_dir/conf/
COPY script/ $work_dir/script/
COPY data/ $work_dir/data/
COPY requirements.txt $work_dir
RUN pip install -r requirements.txt
CMD ["python", "/work/mysql_flask/script/app.py"]