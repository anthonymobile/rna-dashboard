FROM public.ecr.aws/amazonlinux/amazonlinux:2023
RUN yum install python3 && \
curl -O https://bootstrap.pypa.io/get-pip.py && \
python3 get-pip.py && \
pip install --upgrade pip && \
pip install flask 

WORKDIR /app

COPY ./requirements.txt .
RUN pip install -r requirements.txt

RUN alias python=python3

ENV FLASK_APP app.py
ENV PLATFORM 'Amazon ECS'

EXPOSE 5000
COPY ./app .

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
