# Consolidate CUR(Cost and Usage Report) data extractor
This project extracts CUR data from S3 and split CUR data by linked AWS account id. After then it uploads extracted data to linked account's S3 bucket. AWS account id will use to distinguish CUR data and S3 bucket location. 

# Structure
CUR Extractor/\
┣ apps/\
┃ ┣ Config/\
┃ ┃ ┣ Companies.json.sample\
┃ ┃ ┣ Config.py\
┃ ┃ ┣ S3Config.json.sample\
┃ ┃ ┣ \_\_init\_\_.py\
┃ ┃ ┗ logger.conf\
┃ ┣ Extractor/\
┃ ┃ ┣ Extractor.py\
┃ ┃ ┗ \_\_init\_\_.py\
┃ ┣ S3Handler/\
┃ ┃ ┣ S3Handler.py\
┃ ┃ ┗\_\_init\_\_.py\
┃ ┣ Utils/\
┃ ┃ ┣ GZIPHandler.py\
┃ ┃ ┣ JsonReader.py\
┃ ┃ ┗ \_\_init\_\_.py\
┃ ┗ main.py\
┣ .gitignore\
┣ Pipfile\
┣ Pipfile.lock\
┣ README.md\
┗ \_\_init\_\_.py

# Configurations

- Consolidate CUR data of payer account: Confiugration for **Payer account (Consolidate account)** S3 information that CUR data is stored.
    
    * Copy or Rename 'S3Config.json.sample' to 'S3Config.json'
    * Open 'S3Config.json'
    * Put **Payer account information**, **S3 information that CUR data is stored** with keys and **CUR report information**

- Company Information (Linked account information): Configuration for **linked account** S3 information to upload extracted CUR data

    * Copy or Rename 'Companies.json.sample' to 'Companies.json'
    * Open 'Companies.json'
    * Put **Linked account information** and **S3 information to upload extracted CUR data** with keys under 'Companies' field.

- Extractor Configuration: Configuration variables in Config/Config.py

    * RUNNING_INTERVAL - Interval to run extractor. Default is every 12 hours per day (Default is 0:00 and 12:00).\
    This configure follows **cron schedule expressions**. 
    * DOWNLOAD_PATH - Extractor path for CUR data download. Default is './tmp'
    * RESULT_PATH - Extractor path for extracted files. It includes .gz files. **It requires only folder name without '/'** . Default is 'result'
    * NEED_REMOVE_TEMP - Remove temp folder after extracted. Default is True

# Run Service
1. Using **pipenv**. Refer below link to install `pipenv`.
    - https://github.com/pypa/pipenv

2. Git clone the source code
    ```bash
    # Using ssh
    git clone git@github.com:grumatic/cur_extractor.git
    # Using https
    git clone https://github.com/grumatic/cur_extractor.git
    ```
3. Install the package via pipenv
    ```bash
    # Go to the source code folder
    pipenv install
    ```
4. Configure the config files (S3Config.json, Companies.json)
    Refer above **Setting** section. 
5. Run pipenv shell
    ```bash
    pipenv shell
    ```
6. Run service
    ```bash
    export PYTHONPATH=$PYTHONPATH:$PWD:$PWD/apps
    uvicorn --host 0.0.0.0 --port 80 --limit-concurrency 500 --workers 1 apps.main:scheduler --reload
    ```

# License 
Copyright (C) 2020 Grumatic

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Library General Public
License as published by the Free Software Foundation; either
version 2 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Library General Public License for more details.

You should have received a copy of the GNU Library General Public
License along with this library; if not, write to the
Free Software Foundation, Inc., 51 Franklin St, Fifth Floor,
Boston, MA  02110-1301, USA.
