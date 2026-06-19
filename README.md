# Ink Marker Production Line Simulator

Student: Selim Abaza  
Student ID: 100007310  
Course: Advanced Programming Project  
Product: Ink Marker Production Line

## Project overview
This project simulates a production line that assembles ink markers. It includes a Python backend, a Tkinter HMI, defect detection, Docker configuration, InfluxDB and Grafana files, a website and a project report.

## Run the website locally
Open:

```text
website/index.html
```

or from PowerShell inside this folder:

```powershell
start .\website\index.html
```

## Run the Python HMI

```powershell
pip install -r requirements.txt
python .\src\main.py
```

## Run InfluxDB and Grafana
Docker Desktop must be installed and running.

```powershell
docker compose up -d
```

Grafana opens at:

```text
http://localhost:3000
```

Login:

```text
admin / admin
```

If the dashboard needs data, run:

```powershell
python .\src\producer.py
```

## Code structure

```text
src/main.py                 starts the application
src/hmi.py                  Tkinter HMI frontend
src/production_line.py      backend production logic
src/stations.py             separate station classes
src/models.py               marker product model
src/database.py             optional InfluxDB writer
src/producer.py             optional telemetry sender
```

## AI usage
AI tools were used for project planning, debugging support, documentation drafting and website design support. The final project was reviewed, adjusted and tested before submission.
