from bottle import Bottle, run, template
from cabin_map import generate_html

app = Bottle()

@app.route('/map')
@app.route('/map/<map_type>')
def map(map_type=None):
    return generate_html(map_type)

app.run(host='localhost', port=8080, debug=True, reloader=True)