# CUR data extractor
This project extract CUR data from S3 and separate CUR data by AWS account id.
After then it upload to S3 bucket.
AWS account id will use to distinguish CUR data.
Created CUR data based on usage account id.

# Structure
CUR Extractor/\
┣ apps/\
┃ ┣ Config/\
┃ ┃ ┣ Companies.json.sample\
┃ ┃ ┣ Config.py\
┃ ┃ ┣ S3Config.json.sample\
┃ ┃ ┣ __init__.py\
┃ ┃ ┗ logger.conf\
┃ ┣ Extractor/\
┃ ┃ ┣ Extractor.py\
┃ ┃ ┗ __init__.py\
┃ ┣ S3Handler/\
┃ ┃ ┣ S3Handler.py\
┃ ┃ ┗ __init__.py\
┃ ┣ Utils/\
┃ ┃ ┣ GZIPHandler.py\
┃ ┃ ┣ JsonReader.py\
┃ ┃ ┗ __init__.py\
┃ ┗ main.py\
┣ .gitignore\
┣ Pipfile\
┣ Pipfile.lock\
┣ README.md\
┗ __init__.py

# Setting
- CUR data
    Setting for **Payer account (Consolidate Account)** information - include S3 that has CUR data
    1. Copy or Rename 'S3Config.json.sample' to 'S3Config.json'
    2. Open 'S3Config.json'
    3. Put **Payer account information**, **S3 information that has CUR data** with keys and **CUR report information**

- Company Information
    Setting for **Linked account** information - include S3 to upload extracted CUR data
    1. Copy or Rename 'Companies.json.sample' to 'Companies.json'
    2. Open 'Companies.json'
    3. Put **Linked account information** and **S3 information to upload extracted CUR data** with keys under 'Companies'

- Config
    * RUNNING_INTERVAL - Interval to run extracte. Default is At minute 0 past every 12th hour.\
    This configure follow **cron schedule expressions**. 
    * DOWNLOAD_PATH - Path for CUR data download. Default is './tmp'
    * RESULT_PATH - Path for extracted files. It include .gz files. **Need to write without '/'**. Default is 'result'
    * NEED_REMOVE_TEMP - Remove temp folder after extracted. Default is True

# Run Service
1. Using **pipenv**. Refer below link to install pipenv.
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