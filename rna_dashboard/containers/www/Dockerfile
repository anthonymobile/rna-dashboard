FROM public.ecr.aws/amazonlinux/amazonlinux:2022
RUN yum install python3 && \
curl -O https://bootstrap.pypa.io/get-pip.py && \
python3 get-pip.py && \
pip install --upgrade pip

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt


RUN alias python=python3

ENV FLASK_APP app.py
ENV PLATFORM 'Amazon ECS'

WORKDIR /app
COPY . /app/

CMD ["python3", "app.py"]
