from flask import Flask, render_template
from voice_command import voice_command 
import asyncio

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/userguide')
def userguide():
    return render_template('userguide.html')

@app.route('/contact')  
def contact():  
    return render_template('contact.html')

def async_route(route_function):
    def decorated_function(*args, **kwargs):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(route_function(*args, **kwargs))
        loop.close()
        return result
    return decorated_function

async def run_control_script(script_name):
    try:
        import importlib
        module = importlib.import_module(script_name)
        return f'Successfully imported and executed {script_name}.'
    except Exception as e:
        return f'Error importing {script_name}: {str(e)}'

@app.route('/run_face_mouse_control')
def run_face_mouse_control():
    try:
        import face_mouse_control  
        result = 'Face mouse control executed successfully'
    except Exception as e:
        result = str(e)

    return render_template('base.html', result=result)

@app.route('/run_hand_mouse_control')
def run_hand_mouse_control():
    try:
        import hand_mouse_control  
        result = 'Hand mouse control executed successfully'
    except Exception as e:
        result = str(e)

    return render_template('base.html', result=result)

@app.route('/run_keyboard_control')
def run_keyboard_control():
    try:
        import keyboard_control  
        result = 'Keyboard control executed successfully'
    except Exception as e:
        result = str(e)

    return render_template('base.html', result=result)


app.register_blueprint(voice_command)


if __name__ == "__main__":
    app.run(debug=True)