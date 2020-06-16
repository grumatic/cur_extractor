# CUR data extractor
This project extract CUR data from S3 and separate CUR data by AWS account id.
After then it upload to S3 bucket. 
AWS account id will use to distinguish CUR data. 
Created CUR data based on usage account id.

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

# Structure
CUR Extractor/
CUR Extractor/
┣ apps/
┃ ┣ Config/
┃ ┃ ┣ Companies.json.sample
┃ ┃ ┣ Config.py
┃ ┃ ┣ S3Config.json.sample
┃ ┃ ┣ __init__.py
┃ ┃ ┗ logger.conf
┃ ┣ Extractor/
┃ ┃ ┣ Extractor.py
┃ ┃ ┗ __init__.py
┃ ┣ S3Handler/
┃ ┃ ┣ S3Handler.py
┃ ┃ ┗ __init__.py
┃ ┣ Utils/
┃ ┃ ┣ GZIPHandler.py
┃ ┃ ┣ JsonReader.py
┃ ┃ ┗ __init__.py
┃ ┗ main.py
┣ .gitignore
┣ Pipfile
┣ Pipfile.lock
┣ README.md
┗ __init__.py

# Setting
- CUR data
    1. Copy or Rename 'S3Config.json.sample' to 'S3Config.json'
    2. Open 'S3Config.json'
    3. Put S3 information with keys and CUR report information

- Company Information
    1. Copy or Rename 'Companies.json.sample' to 'Companies.json'
    2. Open 'Companies.json'
    3. Put companies information with keys under 'Companies'

- Config
    * RUNNING_INTERVAL - Interval to run extracte. Default is At minute 0 past every 12th hour
    * DOWNLOAD_PATH - Path for CUR data download. Default is './tmp'
    * RESULT_PATH - Path for extracted files. It include .gz files. Need to write with out '/'. Default is 'result'
    * NEED_REMOVE_TEMP - Remove temp folder after extracted. Default is True

# Run Service
Run below command >>
export PYTHONPATH=$PYTHONPATH:$PWD:$PWD/apps
uvicorn --host 0.0.0.0 --port 80 --limit-concurrency 500 --workers 1 apps.main:scheduler --reload