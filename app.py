from flask import Flask, render_template, url_for, request, redirect, flash
import mysql.connector
from datetime import date
import os


app = Flask(__name__)
app.secret_key= 'secret'

#Definimos las Config 

config = {
  'user': 'bfbaad988df285',
  'password': 'bae95327',
  'host': 'us-cdbr-east-03.cleardb.com',
  'database': 'heroku_25e4199725f9d55',
  'port': '3306', 
  'ssl_ca': 'ssl/cleardb-ca.pem', 
  'ssl_cert': 'ssl/bfbaad988df285-cert.pem', 
  'ssl_key': 'ssl/bfbaad988df285-key.pem'
  #'client_flags': [ClientFlag.SSL],
}




#init MySQL
cnx = mysql.connector.connect(**config)

@app.route('/')
def inicio():
    cursor = cnx.cursor()
    cursor.execute('select * from trabajo')
    data = cursor.fetchall()
    cursor.close()
    return render_template('index.html', trabajos = data)

@app.route('/index')
def index():
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
        fecha = date.today() # Cambiar a formato
        cursor = cnx.cursor()
        cursor.execute('INSERT INTO trabajo (artista, trabajo_realizado, precio, fecha) VALUES (%s, %s, %s,%s)',
        (artista, trabajo_real, precio, fecha))
        cursor.close()
        flash('Trabajo Cargado Correctamente')
        return redirect(url_for('index'))


@app.route('/borrar/<string:id>')
def borrar_trabajo(id):
    cursor = cnx.cursor() 
    cursor.execute('delete from trabajo where idtrabajo = {0}'.format(id))
    cursor.close()
    flash('Se borro el trabajo correctamente')
    return redirect(url_for('index'))

@app.route('/editar/<id>')
def pedir_trabajo(id):
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


if __name__ == '__main__':
    app.run()
        

