# export APP_CONFIG_FILE=config/default.py
# export FLASK_ENV=default
export FLASK_APP=index.py
export CONFIG_FILE="src.config.DevelopmentEnvironment"
# adding paths
# ROOT_DIR=.
# MAIN_DIR=./src/main/
# export PYTHONPATH=$MAIN_DIR:$ROOT_DIR

#export # showing all environment variables

flask db init --directory migrations
flask db migrate --directory migrations -m "create Priority table"
flask db upgrade --directory migrations
