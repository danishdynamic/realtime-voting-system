from app.api.app import create_app

app = create_app()

# importing create app funciton from flask 

if __name__ == "__main__" :
    app.run(debug = True)

    