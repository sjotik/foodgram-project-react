<br/>
<p align="center">
  <a href="https://github.com/sjotik/foodgram-project-react">
    <img src="frontend/src/logo.svg" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">FOODGRAM</h3>

  <p align="center">
    Recipes Blog
    <br/>
    <br/>
  </p>
</p>

[![workflow](https://github.com/sjotik/foodgram-project-react/actions/workflows/main.yaml/badge.svg)](https://github.com/sjotik/foodgram-project-react/actions/workflows/main.yaml)

## Table Of Contents

* [About the Project](#about-the-project)
* [Getting Started](#getting-started)
  * [Installation](#installation)
* [Technologies](#used-technologies)
* [License](#license)
* [Authors](#authors)

## About The Project

Social Blog with Recipes.

## Getting Started

If you don't have Docker on your server, use manual from [Official page](https://docs.docker.com/engine/install/)

### Installation

1. [Clone](git@github.com:sjotik/foodgram-project-react.git) this project repo.

2. For starting this project locally use next command from project directory:

`docker compose -f docker-compose.yml up -d`

Open http://127.0.0.1:9090 in browser. **ENJOY**

### ENV variable

Project use PostgresQL database and for deploy you need create **.env** file in root directory with variables:
+ POSTGRES_DB=***set_name_for_DB***
+ POSTGRES_USER=***set_db_user***
+ POSTGRES_PASSWORD=***set_password***
+ DB_HOST=**db**
+ DB_PORT=**5432**

Also there is taken out django variables **SECREC_KEY** and **DEBUG**. You need to set them.

## Used Technologies

* Python
* REST_Framework
* React
* PostgresQL
* Docker Compose

## License

Distributed under the MIT License. See [LICENSE](https://github.com/sjotik/foodgram-project-react/blob/main/LICENSE.md) for more information.

## Authors

* [**Sjotik**](https://github.com/sjotik/)

