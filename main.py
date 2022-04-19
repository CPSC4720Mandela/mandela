from website import create_app
import datetime


app = create_app()
@app.context_processor
def inject_today_date():
    return {'today_date': datetime.date.today()}

if __name__ ==  '__main__': # only when we run main.py and not when we import import main.py we run below line
    app.run(debug = True) # runs the flask web server, with debug set to True, the webserver is automatically rerun whenever there is a change in code