FROM python:3.6
ARG work_dir=/work/mysql_django

WORKDIR $work_dir/

COPY conf/ $work_dir/conf/
COPY django/ $work_dir/django/
COPY data/ $work_dir/data/
COPY requirements.txt $work_dir

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# CMD ["python", "/work/mysql_flask/django/app.py"]