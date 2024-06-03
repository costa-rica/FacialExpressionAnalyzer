# Facial Expression Analyzer

![Flask and DashAndData Logo](https://venturer.dashanddata.com/website_assets_images/dd_and_flask_02-400x209.png)

## Description
This is an application that takes pictures of users and sends them to Google Vision for facial expression analysis.


## Documentation
This uses MySQL and in order to create the tables you must do it from a terminal:
```
from sqlalchemy import create_engine
from fea_models import Base,engine
from fea_config import ConfigWorkstation
config = ConfigWorkstation()
new_engine_str = f"mysql+pymysql://{config.MYSQL_USER}:{config.MYSQL_PASSWORD}@{config.MYSQL_SERVER}/{config.MYSQL_DATABASE_NAME}"
new_engine = create_engine(new_engine_str)
Base.metadata.create_all(new_engine)
```
