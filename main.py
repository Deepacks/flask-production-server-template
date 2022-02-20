from backend import make_app


app = make_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port="var#_server_port", debug=True)
