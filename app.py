from flask import Flask, render_template, url_for, request, redirect, flash
import mysql.connector
from datetime import datetime
import os


app = Flask(__name__)
app.secret_key= 'secret'

#Definimos las Config 

config = {
  'user': 'bfbaad988df285',
  'password': 'bae95327',
  'host': 'us-cdbr-east-03.cleardb.com',
  'database': 'heroku_25e4199725f9d55', 
  'use_pure': 'False',
  'ssl_cipher': 'ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-AES256-SHA:DH-DSS-AES256-GCM-SHA384:DHE-DSS-AES256-GCM-SHA384:DH-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-SHA256:DHE-DSS-AES256-SHA256:DH-RSA-AES256-SHA256:DH-DSS-AES256-SHA256:DHE-RSA-AES256-SHA:DHE-DSS-AES256-SHA:DH-RSA-AES256-SHA:DH-DSS-AES256-SHA:DHE-RSA-CAMELLIA256-SHA:DHE-DSS-CAMELLIA256-SHA:DH-RSA-CAMELLIA256-SHA:DH-DSS-CAMELLIA256-SHA:ECDH-RSA-AES256-GCM-SHA384:ECDH-ECDSA-AES256-GCM-SHA384:ECDH-RSA-AES256-SHA384:ECDH-ECDSA-AES256-SHA384:ECDH-RSA-AES256-SHA:ECDH-ECDSA-AES256-SHA:AES256-GCM-SHA384:AES256-SHA256:AES256-SHA:CAMELLIA256-SHA:PSK-AES256-CBC-SHA:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES128-SHA:DH-DSS-AES128-GCM-SHA256:DHE-DSS-AES128-GCM-SHA256:DH-RSA-AES128-GCM-SHA256:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES128-SHA256:DHE-DSS-AES128-'
}



@app.route('/')
def inicio():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute('select * from trabajo')
    data = cursor.fetchall()
    cursor.close()
    return render_template('index.html', trabajos = data)

@app.route('/index')
def index():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute('select * from trabajo')
    data = cursor.fetchall()
    cursor.close()
    return render_template('index.html', trabajos = data)

@app.route('/nuevo')
def nuevo():
    return render_template('nuevo.html')

@app.route('/reportes')
def reportes():
    return render_template('reportes.html')

@app.route('/nuevo_trabajo', methods=['POST'])
def nuevo_trabajo():
    if request.method == 'POST':
        artista = request.form['artista']
        trabajo_real = request.form['trabajo_realizado']
        precio = request.form['precio']
        fecha = datetime.now()
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        cursor.execute('INSERT INTO trabajo (artista, trabajo_realizado, precio, fecha) VALUES (%s, %s, %s,%s)',
        (artista, trabajo_real, precio, fecha))
        cursor.close()
        flash('Trabajo Cargado Correctamente')
        return redirect(url_for('index'))


@app.route('/borrar/<string:id>')
def borrar_trabajo(id):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor() 
    cursor.execute('delete from trabajo where idtrabajo = {0}'.format(id))
    cursor.close()
    flash('Se borro el trabajo correctamente')
    return redirect(url_for('index'))

@app.route('/editar/<id>')
def pedir_trabajo(id):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute('select * from trabajo where idtrabajo = {0}'.format(id))
    data = cursor.fetchall()
    cursor.close()
    return render_template('edit-trabajo.html', trabajo_sel = data[0])

@app.route('/update/<string:id>', methods=['POST'])
def actualizar_trabajo(id):
    if request.method == 'POST':
        artista = request.form['artista']
        trabajo_real = request.form['trabajo_realizado']
        precio = request.form['precio']
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        cursor.execute("""
        update trabajo 
        set artista = %s,
            trabajo_realizado = %s,
            precio = %s
        where idtrabajo = %s""", (artista, trabajo_real, precio, id))
        cursor.close()
        flash('Se actualizo el trabajo correctamente')
        return redirect(url_for('index'))

    
@app.route('/nuevo_reporte', methods=['POST'])
def nuevo_report():
    if request.method == 'POST':
        variable_x = request.form['variable_x']
        mode = request.form['mode']
        variable_y = request.form['variable_y']
        fecha_in = request.form['fecha_in']
        fecha_fi = request.form['fecha_fi']
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        if (mode!='0') & (variable_x!='0') & (variable_y!='0') & (fecha_in != '') & (fecha_fi != ''):
            if mode == 'sum':
                cursor.execute('SELECT {}, SUM({}) FROM trabajo WHERE fecha > %s AND fecha < %s GROUP BY {}'.format(variable_x, variable_y,variable_x),
                (fecha_in, fecha_fi))
                data = cursor.fetchall()
                etiquetas = []
                datos = []
                for dato in data:
                    etiquetas.append(dato[0])
                    datos.append(int(dato[1]))
                cursor.close()
                return render_template('grafico.html', etiquetas = etiquetas, datos = datos)
                
            else:
                cursor.execute('SELECT {}, COUNT({}) FROM trabajo WHERE fecha > %s AND fecha < %s GROUP BY {}'.format(variable_x, variable_y,variable_x),
                (fecha_in, fecha_fi))
                data = cursor.fetchall()
                etiquetas = []
                datos = []
                for dato in data:
                    etiquetas.append(dato[0])
                    datos.append(int(dato[1]))
                cursor.close()
                return render_template('grafico.html', etiquetas = etiquetas, datos = datos)
                
        else:
            flash('Te olvidaste de seleccionar algun campo')
            cursor.close()
            return redirect(url_for('reportes'))



