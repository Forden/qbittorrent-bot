FROM python:3.9

WORKDIR /qbittorrent-bot

COPY requirements.txt /qbittorrent-bot/
RUN pip install -r /qbittorrent-bot/requirements.txt
COPY . /qbittorrent-bot/

CMD python3 /qbittorrent-bot/bot.py
