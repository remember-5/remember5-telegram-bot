# Telegram Media Forwarder & Cloud Uploader

## Project Description

This is an open-source tool designed to forward media files from Telegram messages to a bot, automatically download
them, and upload them to a cloud storage service. It is cross-platform and ideal for users who need to back up or
migrate Telegram media files.

## Installation Guide

### Requirements

- Python 3.10
- Poetry (dependency management tool)

### Installation Steps

1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo/telegram-media-forwarder.git
    cd telegram-media-forwarder
    ```

2. Install dependencies:
   ```bash
   poetry install
   ```

3. Create and edit the `.env` file:
   ```bash
   cp .env.example .env
   ```
   Modify the `.env` file according to your requirements.

## Usage Instructions

### Database Migrations

1. Generate migration scripts (when models change):
   ```bash
   poetry run alembic revision --autogenerate -m "add_user_table"
   ```

2. Apply migrations:
   ```bash
   poetry run alembic upgrade head
   ```

3. If Alembic is not initialized, initialize it first:
   ```bash
   poetry run alembic init bot/migrations
   ```

4. Configure the database connection:
    - Edit the `alembic.ini` file and update the database connection string:
      ```ini
      sqlalchemy.url = sqlite:///bot.db
      ```

    - Edit the `migrations/env.py` file and configure the `SQLAlchemy` model:
      ```python
      from bot.database import Base
      from bot.models.user import User  # Import your models
 
      target_metadata = Base.metadata
      ```

## Contribution Guidelines

We welcome issues and pull requests! Please follow these steps:

1. Fork the project and create your branch.
2. Commit your changes and create a pull request.
3. Ensure your code passes all tests and follows the project's coding style.

## References

- [tg-auto-install-bot](https://github.com/ershiyi21/myprogram)
- [tgtogd](https://github.com/Xiefengshang/tgtogd)
- [telegram_media_downloader](https://github.com/tangyoha/telegram_media_downloader)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
