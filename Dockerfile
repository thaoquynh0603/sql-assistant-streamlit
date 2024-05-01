FROM python:3.10


COPY . /ui
WORKDIR /ui


RUN pip install -r requirements.txt
EXPOSE 8501


CMD ["streamlit","run","streamlit_app.py"]