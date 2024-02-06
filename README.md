# 🤖 ChatGPT telegram bot

![image](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
![image](https://img.shields.io/badge/ChatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white)
![image](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![image](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)

Implementation of ChatGPT in telegram bot.

## 🚀 Getting started

### Get VPN

To use ChatGPT API you need a VPN (currently this bot working with OpenVPN).
You can get OpenVPN config [here](https://t.me/FCK_RKN_bot)

### Set credentials

Create `credetionals.txt` file and put there your vpn credentials (login and password line by line)

### Set config

Create `test.ovpn` and put there OpenVPN config.
Change line `auth-user-pass` to `auth-user-pass /etc/openvpn/credentials.txt`

## 🛠️ Build and run

To start bot run docker compose:

`docker compose up --build`

## 🔐 Environment

In the `.env` file, or through the `-e` flags, you must set the required variables from
tables below.

| Variable       | Default        | Description             |
|----------------|----------------|-------------------------|
| `BOT_TOKEN`    | **(required)** | Telegram bot token      |
| `OPENAI_TOKEN` | **(required)** | OpenAI API token        |
| `YA_TOKEN`     | **(required)** | Yandex speech kit token |
