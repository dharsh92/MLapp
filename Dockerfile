FROM continuumio/anaconda3
COPY . /usr/app/
EXPOSE 5000
ENV FLASK_APP=flask_api.py
WORKDIR /usr/app/
RUN pip install -r requirements.txt
ENTRYPOINT [ "flask"]
CMD [ "run", "--host", "0.0.0.0" ]
