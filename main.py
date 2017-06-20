from bottle import request, abort, route, run, template, static_file, response
import pyqrcode
import pdfkit
import io


@route('/')
def index():
    return template('index')

@route('/', method="post")
def create_qr():
    data = request.forms.get("data")
    if len(data) == 0 or len(data) >= 1450:
        return abort(400, "Length of data must be in range (0; 1450)")
    response.headers['Content-Type'] = 'application/pdf; charset=UTF-8'

    qr = pyqrcode.create(data)
    buffer = io.BytesIO()
    qr.svg(buffer, scale=40)
    pdfkit.from_string(str(buffer.getvalue())[2:-3], 'qr.pdf', options={'page-size': 'A4'})

    return static_file('qr.pdf', root='./')


@route('/views/style.css')
def server_css():
    return static_file('/views/style.css', root='./')


run(host='localhost', port=8080, debug=True)

