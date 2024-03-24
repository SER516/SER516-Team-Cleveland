FROM python:3.11
WORKDIR /code
COPY / /code/
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY . /code/taigaProject
WORKDIR taigaProject/src
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
