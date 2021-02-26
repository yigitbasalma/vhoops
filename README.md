<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/yigitbasalma/vhoops">
    <img src="docs/images/logo.png" alt="Logo" width="250" height="80">
  </a>

  <h3 align="center">Vhoops</h3>

  <p align="center">
    <a href="https://github.com/yigitbasalma/vhoops/tree/master/docs"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/yigitbasalma/vhoops/issues">Report Bug</a>
    ·
    <a href="https://github.com/yigitbasalma/vhoops/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#configure">Configure</a></li>
        <li><a href="#run">Run</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="https://github.com/yigitbasalma/vhoops/tree/master/docs/images/screenshots">Screenshots</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

The Vhoops is a tool for using consolidate alerts that comes from different sources. It collects, de-duplicates, and consolidates the alerts. Also, you could define routing definitions for these alerts and get some action when alerts come from sources that match the defined patterns.



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

1. Install following software components
   * RabbitMQ
   * Couchbase
   * MongoDB
   * MySQL
   * Redis
2. Clone the repo
   ```sh
   git clone https://github.com/yigitbasalma/vhoops.git
   ```
3. Go to static directory
   ```sh
   cd /path/to/vhoops/vhoops/static
   ```
4. Install necessaries npm packages and build css and js
   ```sh
   npm install && \
   gulp dist
   ```
5. Install python libraries. (you should run as root or pass the --user flag)
   ```bash
   pip install -r requirements.txt
   ```
   
### Configure

1. Move config.example.py to config.py
   ```sh
   mv /path/to/vhoops/vhoops/config/config.example.py /path/to/vhoops/vhoops/config/config.py
   ```
2. Create MySQL database.
   ```sh
   create database vhoops character set utf8 collate utf8_bin;
   ```
3. Configure the sqlalchemy connection string.
   ```python
   SQLALCHEMY_DATABASE_URI = "mysql+pymysql://username:password@192.168.56.2:3306/vhoops"
   ```
4. Configure the mail.
   ```python
   MAIL_USERNAME = "vhoops@vhoops.com"
   MAIL_PASSWORD = "123456"
   MAIL_SERVER = "smtp.mail.com"
   ```
5. Configure the couchbase. (You need to create buckets manually for now)
   ```python
   CACHE_CONN_STRING = "couchbase://192.168.56.2"
   CACHE_USERNAME = "Administrator"
   CACHE_PASSWORD = "123456*"
   CACHE_BUCKETS = [
       "app_cache"
   ]
   ```
6. Configure redis for page cache.
   ```python
   CACHE_TYPE = "redis"
   CACHE_REDIS_HOST = "192.168.56.2"
   ```
7. Configure celery.
   ```python
   CELERY_BROKER_URL = "redis://192.168.56.2:6379/1"
   ```
8. Configure AMQP for alert queue (in the celery_config.py)
   ```python
   amqp_config = dict(
       host="192.168.56.3:5672",
       userid="admin",
       password="admin",
       hearbeat=30
   )
   ```

### Run

1. Start run.py command. (you should run as root or manually create /var/log/vhoops directory)
   ```sh
   python /path/to/vhoops/run.py
   ```
2. Start celery
   ```bash
   cd /path/to/vhoops && \
   celery -A vhoops.celery worker --loglevel=info && \
   celery beat -l info -A vhoops.celery
   ```



<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_



<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/yigitbasalma/vhoops/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.