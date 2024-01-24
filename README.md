# python-cf-gen-tf
Simple python script to generate TF code for all domains and their dns records via user API requests

## Requirements 
 - Python3
 - the pip packages in requirements.txt
 - internet connection

## Setup and usage
 ```bash
 git clone https://github.com/boznius/python-cf-gen-tf.git
 cd python-cf-gen-tf
 python3 -m venv .venv
 source .venv/bin/activate
 pip install -r requirements.txt
 vim/nano cf-generate-tf3.py
 # Generate a user api code and add it to api_token = '' inside of the script.
 # Then run the script:
 python cf-generate-tf3.py
 # This is expected to generate domain files with all the records you have inside of the terraform_files/ folder under the repository or create it if it does not exist.
 
```
