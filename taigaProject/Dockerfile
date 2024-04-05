# FROM python:3.11
# WORKDIR /code
# COPY requirements.txt /code/
# RUN pip install --no-cache-dir --upgrade -r requirements.txt
# COPY . /code/taigaProject
# WORKDIR taigaProject/src
# EXPOSE 8000
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM python:3.11
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
COPY . /code/taigaProject
WORKDIR taigaProject/src
EXPOSE 8001
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
