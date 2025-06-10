Setting up enviroment:


mkdir fastapi-project
cd fastapi-project

python -m venv env
source env/bin/activate   # On Windows use: env\Scripts\activate

pip install "fastapi[all]"  

#run the environment with this commamnd:
uvicorn main:app --reload

