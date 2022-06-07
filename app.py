from flask import Flask, render_template, request

# Instantiate Flask app/web server.
app = Flask(
    __name__,
    static_folder='/static/'
)

with open('insults.txt', 'r') as file:
    global insults
    insults = file.read().splitlines()


app.config['TEMPLATES_AUTO_RELOAD'] = True


# Route for testing purposes.
@app.route('/')
def index():
    return 'Hello World!'


text = 'I am a test'
textColor = 'white'
backgroundColor = 'purple'


# Route to get the text.
@app.route('/api/text/get')
def api_get_text():
    return {
        'text': text,
        'textColor': textColor,
        'backgroundColor': backgroundColor,
    }


# Route to change the text.
@app.route('/api/text/change')
def api_change_text():
    # Use variables from global scope.
    global text, textColor, backgroundColor

    args = dict(request.args)

    # Figure out what variable the request wants to change.
    if 'text' in args.keys():
        if args['text'] in insults:
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