from flask import Flask, render_template, request, redirect, url_for, session, flash
import pymysql

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Cambiar a una clave más segura

# Configuración de la base de datos
db_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',  # Cambiar si tienes un usuario diferente
    'password': '',  # Cambiar si tienes una contraseña configurada
    'database': 'bd_seguridad',
    'cursorclass': pymysql.cursors.DictCursor
}

# Conexión a la base de datos
def connect_to_db():
    return pymysql.connect(**db_config)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/quienes-somos')
def quienes_somos():
    return render_template('quienes_somos.html')

@app.route('/acerca-de')
def acerca_de():
    return render_template('acerca_de.html')

@app.route('/menu')
def menu():
    if 'usuario' in session:
        return render_template('opciones.html')
    #   return render_template('equipos.html')
    flash('Debes iniciar sesión para acceder a estas opciones', 'warning')
    return redirect(url_for('inicio_sesion'))
    
    
# Ruta para la página de contacto
@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        # Recuperar los datos enviados por el formulario
        nombre = request.form['nombre']
        email = request.form['email']
        mensaje = request.form['mensaje']

        # Validación básica (puedes personalizarla)
        if not nombre or not email or not mensaje:
            flash('Todos los campos son obligatorios.', 'danger')
        else:
            flash('Mensaje enviado correctamente. ¡Gracias por contactarnos!', 'success')

        # Redirigir de vuelta a la página de contacto
        return redirect(url_for('contacto'))

    # Mostrar el formulario cuando sea GET
    return render_template('contacto.html')



@app.route('/inicio-sesion', methods=['GET', 'POST'])
def inicio_sesion():
    if request.method == 'POST':
        clave = request.form['clave']
        try:
            connection = connect_to_db()
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM usuarios WHERE clave = %s", (clave,))
                usuario = cursor.fetchone()
                if usuario:
                    session['usuario'] = usuario['clave']
                    flash('Inicio de sesión exitoso', 'success')
                    return redirect(url_for('opciones'))
                else:
                    flash('Clave incorrecta', 'danger')
        finally:
            connection.close()
    return render_template('inicio_sesion.html')

@app.route('/opciones')
def opciones():
    if 'usuario' in session:
        return render_template('opciones.html')
    flash('Debes iniciar sesión para acceder a estas opciones', 'warning')
    return redirect(url_for('inicio_sesion'))

@app.route('/pagina1')
def pagina1():
    if 'usuario' in session:
        return render_template('equipos.html')
    return redirect(url_for('inicio_sesion'))


@app.route('/pagina2')
def pagina2():
    if 'usuario' in session:
        return render_template('pagina2.html')
    return redirect(url_for('inicio_sesion'))

@app.route('/pagina3')
def pagina3():
    if 'usuario' in session:
        return render_template('pagina3.html')
    return redirect(url_for('inicio_sesion'))

@app.route('/pagina4')
def pagina4():
    if 'usuario' in session:
        return render_template('pagina4.html')
    return redirect(url_for('inicio_sesion'))

@app.route('/pagina5')
def pagina5():
    if 'usuario' in session:
        return render_template('pagina5.html')
    return redirect(url_for('inicio_sesion'))

@app.route('/cerrar-sesion')
def cerrar_sesion():
    session.pop('usuario', None)
    flash('Sesión cerrada exitosamente', 'info')
    return redirect(url_for('home'))

    
### AGREGADO
    
#    from flask import Flask, render_template, request, redirect, url_for,
#import mysql.connector

#app = Flask(__name__)
#app.secret_key = 'clave_secreta_segura'

# Configuración de conexión a MySQL
#db_config = {
#    'host': 'localhost',
#    'user': 'root',  # Cambia por tu usuario de MySQL
#    'password': '',  # Cambia por tu contraseña
#    'database': 'bd_seguirdad'
#}

# Página principal para gestión de equipos
@app.route('/equipos', methods=['GET', 'POST'])
def equipos():

 # Agregado mio
   connection = connect_to_db()
   with connection.cursor() as cursor:


#mmuo
 #   cursor.execute("SELECT * FROM equipos")
 #   equipos = cursor.fetchall()
 #    connection.commit()
 #


    if request.method == 'POST':
        # Capturar datos del formulario
        nombre_equipo = request.form['nombre_equipo']
        tipo_equipo = request.form['tipo_equipo']
        marca = request.form['marca']
        modelo = request.form['modelo']
        numero_serie = request.form['numero_serie']
        fecha_compra = request.form['fecha_compra']

        try:
            # Insertar nuevo equipo
            query = """
            INSERT INTO equipos (nombre_equipo, tipo_equipo, marca, modelo, numero_serie, fecha_compra)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (nombre_equipo, tipo_equipo, marca, modelo, numero_serie, fecha_compra))
            connection.commit()
            flash('Equipo agregado correctamente.', 'success')
        except pymysql.connector.Error as err:
            flash(f'Error al agregar el equipo: {err}', 'danger')

    # Recuperar todos los equipos
    cursor.execute("SELECT * FROM equipos")
    equipos = cursor.fetchall()
    
    connection.close()
    return render_template('equipos.html', equipos=equipos)

# Ruta para eliminar un equipo
@app.route('/equipos/eliminar/<int:id>')
def eliminar_equipo(id):
    connection =pymysql.connect(**db_config) 
    cursor = connection.cursor()

    try:
        cursor.execute("DELETE FROM equipos WHERE id = %s", (id,))
        connection.commit()
        flash('Equipo eliminado correctamente.', 'info')
    except pymysql.connect.Error as err:
        flash(f'Error al eliminar el equipo: {err}', 'danger')

    connection.close()
    return redirect(url_for('equipos'))

# Ruta para editar un equipo
@app.route('/equipos/editar/<int:id>', methods=['GET', 'POST'])
def editar_equipo(id):
    connection =pymysql.connect(**db_config) 
    cursor = connection.cursor()

    if request.method == 'POST':
        # Actualizar datos
        nombre_equipo = request.form['nombre_equipo']
        tipo_equipo = request.form['tipo_equipo']
        marca = request.form['marca']
        modelo = request.form['modelo']
        numero_serie = request.form['numero_serie']
        fecha_compra = request.form['fecha_compra']

        try:
            query = """
            UPDATE equipos
            SET nombre_equipo = %s, tipo_equipo = %s, marca = %s, modelo = %s,
                numero_serie = %s, fecha_compra = %s
            WHERE id = %s
            """
            cursor.execute(query, (nombre_equipo, tipo_equipo, marca, modelo, numero_serie, fecha_compra, id))
            connection.commit()
            flash('Equipo actualizado correctamente.', 'success')
        except pymysql.connector.Error as err:
            flash(f'Error al actualizar el equipo: {err}', 'danger')

        connection.close()
        return redirect(url_for('equipos'))

    # Obtener los datos actuales del equipo
    cursor.execute("SELECT * FROM equipos WHERE id = %s", (id,))
    equipo = cursor.fetchone()

    connection.close()
    return render_template('editar_equipo.html', equipo=equipo)

if __name__ == '__main__':
    app.run(debug=True)
