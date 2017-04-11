from data_retrieving import DataRetrieving
from bottle import Bottle, run
import codecs

app = Bottle()


@app.get('/<request_text>')
def get_basic(request_text=None):
    request_text = request_text.strip()
    request_text = codecs.decode(bytes(request_text, 'iso-8859-1'), 'utf-8')
    if request_text:
        result = DataRetrieving.get_data(request_text)
        return result.toJSON()


run(app, host='localhost', port=8019, debug=True)
