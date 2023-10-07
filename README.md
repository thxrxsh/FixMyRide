
# Overview

The FixMyRide API is a robust and scalable solution that facilitates the connection between vehicle owners and mechanics, optimizing the process of locating and securing mechanical services. Designed with a focus on efficiency and real-time communication, this API empowers developers to integrate the FixMyRide platform seamlessly into their applications


## Installation

Clone the Repository using Git

```bash
git clone https://github.com/thxrxsh/FixMyRide.git
```
```bash
cd FixMyRide
```

Create a virtual environment using python and activate it.

```bash
python3 -m venv venv
```
```bash
cd venv\Scripts
```
```bash
./activate
```


Install dependencies using `requirements.txt`

```bash
pip Install -r requirements.txt
```


> [!IMPORTANT]
> Create new database for FixMyRide API



## Environment Variables

To run this api, you will need to add the following environment variables to your `.env` file. Therefor create `.env` file in `/FixMyRide` directory

`DATABASE_HOSTNAME`

`DATABASE_PORT`

`DATABASE_PASSWORD`

`DATABASE_NAME`

`DATABASE_USERNAME`

`SECRET_KEY`

`ACCESS_TOKEN_EXPIRE_MINUTES`

`GOOGLE_DERECTIONS_API_KEY`
## Configure

Create an environment for alembic in `/FixMyRide` directory

```bash
alembic init alembic
```

Make changes to `/alembic/env.py` file
- Import modules

```bash
from App.models import Base
from App.config import Settings
```
- Set sqlalchemy URL

```bash
url = f"postgresql+psycopg2://{Settings.database_username}:{Settings.database_password}@{Settings.database_hostname}:{Settings.database_port}/{Settings.database_name}"
config.set_main_option("sqlalchemy.url", url)
```

- Set `target_metadata` to `Base.metadata`

```bash
target_metadata = Base.metadata
```

Create tables in the database

```bash
alembic revision --autogenerate -m "create tables"
```
```bash
alembic upgrade head
```

## Deployment

Change directory to `/App`
```bash
cd App
```

Run the API using uvicorn
```bash
uvicorn main:app
```

Access the API using this URL :
```http
http://127.0.0.1:8000/
```

> [!NOTE]
> Please note that when running the API in a development environment, it is only accessible on your local machine (localhost). If you want to make the API accessible over the internet or share it with others, you will need to use a tool like NGINX or ngrok to expose it externally. These tools can help you set up a secure tunnel to your local server, allowing external access while maintaining security and control over the exposure of your API.
> Ensure that you have the necessary configurations in place to expose your API securely when needed for testing or sharing with others.


## Screenshots

![API-root Postman view](https://github.com/thxrxsh/FixMyRide/assets/76760967/1e77eb0f-2c60-465a-a869-da9aa4de4c63)
![API-root Browser view](https://github.com/thxrxsh/FixMyRide/assets/76760967/2096609b-7675-4272-ae62-26b5a61726db)
![API Documentation](https://github.com/thxrxsh/FixMyRide/assets/76760967/09f6bc35-2611-40b1-a371-b214032e9d19)



## API Reference

For comprehensive references and detailed documentation of the API, please access the documentation through the following URL after running the API locally:

[API Documentation](http://127.0.0.1:8000/docs#/) : 
```http
http://127.0.0.1:8000/docs#/
```

## License

[MIT](https://choosealicense.com/licenses/mit/)

