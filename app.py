from flask import Flask, render_template, redirect, jsonify
import flask, json, requests

app = Flask(__name__)
if __name__ == '__main__':
	app.run(debug=True, port=5000)

class Movil:
	def __init__(self, identificador, tipo):
		self.identificador = identificador
		self.tipo = tipo


class Ubicacion:
	def __init__(self, **kwargs):
		if 'date' in kwargs:
			self.fecha_hora = kwargs.pop('date')
		if 'tipo' in kwargs:
			self.tipo = kwargs.pop('tipo')
		if 'id' in kwargs:
			self.id_movil = kwargs.pop('id')
		if 'lat' in kwargs:
			self.latitud = kwargs.pop('lat')
		if 'lon' in kwargs:
			self.longitud = kwargs.pop('lon')	


@app.route('/')
def index():
	return render_template('home.html')


@app.route('/movil/')
def movil():
	return render_template('movil/movil.html')


@app.route('/ubicacion/')
def ubicacion():
	return render_template('ubicacion/ubicacion.html')


###### MOVIL #####

@app.route('/movil/registrar-movil/', methods=['GET', 'POST'])
def registrar_movil():
	if flask.request.method == 'GET':
		return render_template('movil/registrar_movil.html')
	url = "http://localhost:8080/movil/rest/movil"
	headers = {'content-type': 'application/json'}
	movil_dict = Movil(flask.request.form['identificador'], flask.request.form['tipo']).__dict__
	response = requests.post(url, data=json.dumps(movil_dict), headers=headers)
	return redirect('/movil/obtener-moviles/')


@app.route('/movil/obtener-movil/', methods=['GET', 'POST'])
def obtener_movil():
	if flask.request.method == 'GET':
		return render_template('movil/obtener_movil.html', search_id = 1)
	url = "http://localhost:8080/movil/rest/movil/"
	response = requests.get(url+flask.request.form['identificador']).json()
	movil = Movil(response['identificador'], response['tipo'])
	return render_template('movil/obtener_movil.html', movil=movil)


@app.route('/movil/obtener-moviles/')
def get_moviles():
	url = "http://localhost:8080/movil/rest/movil/"
	response = requests.get(url).json()
	movil_query=[]
	for x in response:
		movil_query.append(Movil(x['identificador'], x['tipo']))
	return render_template('movil/obtener_moviles.html', movil_query=movil_query)


@app.route('/movil/borrar-movil/', methods=['GET', 'POST'])
def borrar_movil():
	if flask.request.method == 'GET':
		return render_template('movil/borrar_movil.html')
	url = "http://localhost:8080/movil/rest/movil/" 
	response = requests.delete(url+flask.request.form['identificador'])
	return redirect('/movil/obtener-moviles/')


###### UBICACIONES ######

@app.route('/ubicaciones/registrar-ubicacion/', methods=['GET', 'POST'])
def registrar_ubicacion():
	if flask.request.method == 'GET':
		return render_template('ubicacion/registrar_ubicacion.html')
	url = "http://localhost:8080/movil/rest/ubicacion"
	headers = {'content-type': 'application/json'}
	movil_dict = Ubicacion(id=flask.request.form['identificador'], lat=flask.request.form['latitud'], lon=flask.request.form['longitud']).__dict__
	response = requests.post(url, data=json.dumps(movil_dict), headers=headers)
	return redirect('/ubicacion/obtener-ubicaciones')


@app.route('/ubicacion/obtener-ubicacion/', methods=['GET', 'POST'])
def obtener_ubicacion():
	if flask.request.method == 'GET':
		return render_template('ubicacion/obtener_ubicacion.html', search_id = 1)
	url = "http://localhost:8080/movil/rest/ubicacion/Longitud/"+flask.request.form['longitud']+'/Latitud/'+\
					flask.request.form['latitud']+'/distancia/'+flask.request.form['distancia']
	ubicacion_query = []
	response = requests.get(url).json()
	for u in response:
		ubicacion_query.append(Ubicacion(date=u['fecha-hora'], id=u['identificador'], tipo=u['tipo']))
	return render_template('ubicacion/obtener_ubicacion.html', ubicaciones = ubicacion_query)


@app.route('/ubicacion/obtener-ubicaciones', methods=['GET'])
def obtener_ubicaciones():
	url = "http://localhost:8080/movil/rest/ubicacion/" 
	response = requests.get(url).json()
	ubicacion_query = []
	for u in response:
		ubicacion_query.append(Ubicacion(date=u['fecha_hora'], id=u['id_movil'], lat=u['latitud'], lon=u['longitud']))
	return render_template('/ubicacion/obtener_ubicaciones.html', ubicaciones=ubicacion_query)


@app.route('/ubicacion/borrar-ubicacion', methods=['GET', 'POST'])
def borrar_ubicacion():
	if flask.request.method == 'GET':
		return render_template('ubicacion/borrar_ubicacion.html')
	url = "http://localhost:8080/movil/rest/ubicacion/id/"+flask.request.form['id']
	response = requests.delete(url)
	return redirect('/ubicacion/obtener-ubicaciones')