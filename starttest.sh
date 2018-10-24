export $(egrep -v '^#' .env | xargs)

coverage run --source='.' manage.py test
