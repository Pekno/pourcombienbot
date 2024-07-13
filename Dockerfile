FROM python:3
ENV DISCORD_TOKEN=$DISCORD_TOKEN
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python3", "pourcombien.py"]