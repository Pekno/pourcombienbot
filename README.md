# ![Logo](logo.png) Discord Betting Game Bot

<div align="center">
  

![GitHub Tag](https://img.shields.io/github/v/tag/pekno/pourcombienbot?label=latest%20version)
[![Docker pulls](https://img.shields.io/docker/pulls/pekno/pourcombienbot)](https://hub.docker.com/r/pekno/pourcombienbot)
  
</div>

## Description

Welcome to the Discord Betting Game Bot! This bot allows you and your friends to engage in a fun and interactive betting game right within your Discord server. Challenge your friends and see who comes out on top!

## Commands

Below is a table of commands available for the Discord Betting Game Bot:

| Command               | Description                        | Parameters                    |
|-----------------------|------------------------------------|-------------------------------|
| `/pourcombien`        | Initiate a betting game            | `member` (Who do you want to challenge?) |

## Setup

To get the Discord Betting Game Bot up and running, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up environment variables**:
    - Create a `.env` file in the root directory of your project.
    - Add the following environment variable to the `.env` file:

    ```env
    DISCORD_TOKEN=your_discord_bot_token_here
    ```

4. **Run the bot**:
    ```bash
    python bot.py
    ```
A Docker image is also available via [Docker Hub](https://hub.docker.com/r/pekno/pourcombienbot).

You should now have the Discord Betting Game Bot running in your server! Enjoy betting with your friends!
