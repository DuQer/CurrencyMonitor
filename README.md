# CurrencyMonitor

## Table of contents
* [General info](#general-info)
* [Screenshots](#screenshots)
* [Installation](#installation)
* [System requirements](#system-requirements)
* [Technology stack](#technology-stack)


## General info
CurrencyMonitor is a simple application to watch currency exchange rates. It allows user to register an account, display currency symbols and download it, 
check historical data and preview popular exchange rates. It is also possible to predict exchange rates, using LSTM(Long short-term memory) artificial neural network.
Application can be run using docker container.
## Screenshots
1. **Main view**

![image](https://github.com/DuQer/CurrencyMonitor/assets/66977132/c3e2b9bf-6071-42cd-9d56-c0c017839a3d)

2. **Ticker table view**

![image](https://github.com/DuQer/CurrencyMonitor/assets/66977132/58220b67-8ed1-4cfe-a803-c3705a379e02)


3. **Historical data view**

![image](https://github.com/DuQer/CurrencyMonitor/assets/66977132/6aa22100-9f3f-47ee-a5f6-d472b8ca1b62)


4. **Prediction view**

![image](https://github.com/DuQer/CurrencyMonitor/assets/66977132/876334e3-6ba8-42aa-98ea-83deb35d23fb)


## Installation
Use this docker command to install project:
```bash
docker compose up
```
## System requirements
- Python 3.11.0 (or higher)
- Docker
## Technology stack:
- Python
- Django
- Yfinance
- Keras
- LSTM
- Pandas
- Numpy
- Docker
