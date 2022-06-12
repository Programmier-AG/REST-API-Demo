import ast
import requests
import time
from flask import Flask, render_template, request

# Instantiate Flask app/web server.
app = Flask(
    __name__,
    static_folder='/static/'
)

insults = requests.get("https://raw.githubusercontent.com/DavidRuoff/german-insults/master/src/index.json").text
insults = set(ast.literal_eval(insults))

app.config['TEMPLATES_AUTO_RELOAD'] = True


# Route for testing purposes.
@app.route('/')
def index():
    return '<a href="/api/text/get/">TEXT API</a>'


text = 'I am a test'
textColor = 'white'
backgroundColor = 'purple'


# Route to get the text.
@app.route('/api/text/get/')
def api_get_text():
    current_data = {
        'text': text,
        'textColor': textColor,
        'backgroundColor': backgroundColor,
    }
    if request.args.get("long_poll", "true") == "false":
        return current_data

    for i in range(30):
        new_data = {
            'text': text,
            'textColor': textColor,
            'backgroundColor': backgroundColor,
        }
        if new_data != current_data:
            return new_data
        time.sleep(1)

    return current_data

# Route to change the text.
@app.route('/api/text/change')
def api_change_text():
    # Use variables from global scope.
    global text, textColor, backgroundColor

    args = dict(request.args)

    # Figure out what variable the request wants to change.
    if 'text' in args.keys():
        if set([x.lower() for x in args['text'].split(" ")]) & insults:
            text = 'NOOO! BAAAD!!! 😡'
        else:
            text = args['text']
    elif 'textColor' in args.keys():
        textColor = args['textColor']
    elif 'backgroundColor' in args.keys():
        backgroundColor = args['backgroundColor']

    return {
        'text': text,
        'textColor': textColor,
        'backgroundColor': backgroundColor,
    }


# The display to show on a big screen.
@app.route('/display/')
def display():
    return render_template('display.html')


# Run app if called directly.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
