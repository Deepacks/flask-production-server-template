if [ "$1" = "gunicorn" ]
then
    gunicorn main:app --access-logfile '-'
fi  

if [ "$1" = "python" ]
then
    python main.py
fi  