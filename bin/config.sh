# set default options
server_port="8080"          # -p
salt=""                     # -s
mongo_user="admin"          # -u
mongo_password="admin"      # -c
mongo_port="27017"          # -m
mongo_db_name="admin"       # -n
mongo_auth_db_name="admin"  # -a
jwt_secret=""               # -j

# get options
while test $# -gt 0; do
  case "$1" in 
    -p)
      shift
      if test $# -gt 0; then
        server_port=$1
      else
        echo "no process specified"
        exit 1
      fi
      shift
      ;;
    --server-port*)
      export server_port=`echo $1 | sed -e 's/^[^=]*=//g'`
      shift
      ;;
    -s)
      shift
      if test $# -gt 0; then
        salt=$1
      else
        echo "no output dir specified"
        exit 1
      fi
      shift
      ;;
    --salt*)
      salt=`echo $1 | sed -e 's/^[^=]*=//g'`
      shift
      ;;
    -u)
      shift
      if test $# -gt 0; then
        mongo_user=$1
      else
        echo "no process specified"
        exit 1
      fi
      shift
      ;;
    --mongo-user*)
      mongo_user=`echo $1 | sed -e 's/^[^=]*=//g'`
      shift
      ;;
    -c)
      shift
      if test $# -gt 0; then
        mongo_password=$1
      else
        echo "no process specified"
        exit 1
      fi
      shift
      ;;
    --mongo-password*)
      mongo_password=`echo $1 | sed -e 's/^[^=]*=//g'`
      shift
      ;;
    -m)
      shift
      if test $# -gt 0; then
        mongo_port=$1
      else
        echo "no process specified"
        exit 1
      fi
      shift
      ;;
    --mongo-port*)
      mongo_port=`echo $1 | sed -e 's/^[^=]*=//g'`
      shift
      ;;
    -n)
      shift
      if test $# -gt 0; then
        mongo_db_name=$1
      else
        echo "no process specified"
        exit 1
      fi
      shift
      ;;
    --mongo-db*)
      mongo_db_name=`echo $1 | sed -e 's/^[^=]*=//g'`
      shift
      ;;
    -a)
      shift
      if test $# -gt 0; then
        mongo_auth_db_name=$1
      else
        echo "no process specified"
        exit 1
      fi
      shift
      ;;
    --mongo-auth-db*)
      mongo_auth_db_name=`echo $1 | sed -e 's/^[^=]*=//g'`
      shift
      ;;
    -j)
      shift
      if test $# -gt 0; then
        jwt_secret=$1
      else
        echo "no process specified"
        exit 1
      fi
      shift
      ;;
    --jwt-secret*)
      jwt_secret=`echo $1 | sed -e 's/^[^=]*=//g'`
      shift
      ;;
    *)
      break
      ;;
  esac
done

# config main.py
echo "from backend import make_app" > main.py  
echo "" >> main.py
echo "" >> main.py
echo "app = make_app()" >> main.py
echo "" >> main.py
echo "if __name__ == '__main__':" >> main.py
echo "    app.run(host='0.0.0.0', port=$server_port, debug=True)" >> main.py

# config yaml
echo "app:" > ./yamls/config.yaml
echo "  name: FlaskTemplate" >> ./yamls/config.yaml
echo "  salt: $salt" >> ./yamls/config.yaml
echo "mongo:" >> ./yamls/config.yaml
echo "  host: mongodb://$mongo_user:$mongo_password@localhost:$mongo_port/$mongo_db_name?authSource=$mongo_auth_db_name" >> ./yamls/config.yaml
echo "jwt:" >> ./yamls/config.yaml
echo "  secret: $jwt_secret" >> ./yamls/config.yaml

# config gunicorn
echo "bind = '0.0.0.0:$server_port'" > gunicorn.conf.py
echo "workers = 4" >> gunicorn.conf.py
echo "accesslog = '-'" >> gunicorn.conf.py


python3 -m venv ./environment &&
source ./environment/bin/activate &&
python -m pip install --upgrade pip &&
pip install -r requirements.txt &&
