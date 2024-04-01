FROM python
WORKDIR /TelegramBot
COPY . /TelegramBot
RUN pip install update \
    && pip install -r requirements.txt

CMD python chatbot.py