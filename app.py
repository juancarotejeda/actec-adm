
import mysql.connector,funciones,os
from flask import Flask, render_template,flash, request, redirect, url_for
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key=os.getenv("APP_KEY")

DB_HOST =os.getenv('DB_HOST')
DB_USERNAME =os.getenv("DB_USERNAME")
DB_PASSWORD =os.getenv("DB_PASSWORD")
DB_NAME =os.getenv("DB_NAME")

# Connect to the database
connection =mysql.connector.connect(
    host=DB_HOST,
    user=DB_USERNAME,
    password=DB_PASSWORD,
    database=DB_NAME,
    autocommit=True
)

@app.route("/")
def login():  
    cur = connection.cursor() 
    resultado=funciones.listado_miembro(cur)  
    cur.close()                   
    return render_template('login.html',parada_adm=resultado)

@app.route("/new_data", methods=["GUET","POST"])
def new_data(): 
   msg = ''
   resultado=[]
   if request.method == 'POST':    
    funcion = request.form['funcion']
    codigo = request.form['codigo']
    password = request.form['clave']    
    cur = connection.cursor()       
    resultado=funciones.administracion(cur,codigo)
    if resultado != []:    
        if password == resultado:                                           
           if funcion[0:3] =='GER': 
              valor=0,0,0,0,0,0,0,0
              selector_paradas=funciones.listado_paradas(cur)            
              return render_template('direccion.html',selector_paradas=selector_paradas,valor=valor) 
           elif funcion[0:3] =='PUB':  
              return render_template('digitadores.html')
           elif funcion[0:3] =='DIG': 
              selector_paradas=funciones.listado_paradas(cur)              
              return render_template('digitadores.html',selector_paradas=selector_paradas)   
    else: 
        msg= 'no podemos confirmar su informacion!'
        flash(msg)
        return redirect(url_for('login'))
    
@app.route('/selector_data',methods=['GUET','POST'])
def selector_data(): 
    if request.method == 'POST':    
        parada = request.form['paradax']
        cur = connection.cursor()    
        fecha = datetime.strftime(datetime.now(),"%Y %m %d - %H:%M:%S")
        informacion=funciones.info_parada(cur,parada)
        cabecera=funciones.info_cabecera(cur,parada)
        miembros=funciones.lista_miembros(cur,parada)
        diario=funciones.diario_general(cur,parada)
        selector_paradas=funciones.listado_paradas(cur) 
        cuotas_hist=funciones.prestamo_aport(cur,parada)  
        print(cuotas_hist)  
        return render_template('direccion.html',fecha=fecha,informacion=informacion,cabecera=cabecera,miembros=miembros,valor=diario,cuotas_hist=cuotas_hist,selector_paradas=selector_paradas)
    

@app.route("/data_cuotas", methods=["GET","POST"])
def data_cuotas():
    my_list=[]
    if request.method == 'POST': 
        parada=request.form['parada']     
        hoy = request.form['time']
        cant=request.form['numero']
        valor_cuota=request.form['valor']
        for i in range(int(cant)): 
            my_list +=(request.form.getlist('item')[i],
                    request.form.getlist('select')[i],
                    request.form.getlist('nombre')[i],
                    request.form.getlist('cedula')[i])  
        string=funciones.dividir_lista(my_list,4) 
        cur = connection.cursor()
        funciones.crear_p(cur,parada,string,valor_cuota,hoy)  
        cur.close()                                                        
        return redirect(url_for('data_confirmacion'))   
 



@app.route('/crear_nueva_p',methods=['GUEST','POST']) 
def crear_nueva_p():
    if request.method == 'POST':
       cur = connection.cursor()
       parada=request.form['nombre']
       direccion=request.form['direccion']
       municipio=request.form['municipio']
       provincia=request.form['provincia']
       zona=request.form['zona']
       cuota=request.form['cuota']
       pago=request.form['pago']
       banco=request.form['banco']
       num_cuenta=request.form['cuenta']
       funciones.generar_pp(cur,parada,direccion,municipio,provincia,zona,cuota,pago,banco,num_cuenta)
       return render_template('digitadores.html')



                                                   
@app.route('/edit_parada',methods=['GUEST','POST']) 
def edit_parada(): 
    if request.method == 'POST':               
       parada=request.form['e-parada']
       cur = connection.cursor()
       data=funciones.info_parada(cur,parada)
       cur.close()      
       return render_template('digitadores.html',data=data,parada=parada) 
 
@app.route('/actualizar_p',methods=['GUEST','POST']) 
def actualizar_p():
    if request.method == 'POST':
       cur = connection.cursor()
       parada=request.form['parada']
       direccion=request.form['direccion']
       municipio=request.form['municipio']
       provincia=request.form['provincia']
       zona=request.form['zona']
       cuota=request.form['cuota']
       pago=request.form['pago']
       banco=request.form['banco']
       num_cuenta=request.form['num_cuenta']
       funciones.actualizar_pp(cur,parada,direccion,municipio,provincia,zona,cuota,pago,banco,num_cuenta)   
       cur.close()
       return render_template('digitadores.html')                      
                           
@app.route('/n_miembro',methods=['GUEST','POST']) 
def n_miembro(): 
    if request.method == 'POST':
       cur = connection.cursor()
       parada=request.form['E-parada']
       nombre=request.form['nombre']
       cedula=request.form['cedula']
       telefono=request.form['telefono']
       funcion=request.form['funcion']
       funciones.insertar_Asociado(cur,parada,nombre,cedula,telefono,funcion)
       cur.close()
       return render_template('digitadores.html')

@app.route('/select_p',methods=['GUEST','POST']) 
def select_p(): 
    if request.method == 'POST':
       cur = connection.cursor()
       parada=request.form['parada']
       list_miembros=funciones.nombres_miembro(cur,parada)
       cur.close()
       return render_template('digitadores.html',parada=parada,list_miembros=list_miembros)
                           
                           
@app.route('/select_miembro',methods=['GUEST','POST']) 
def select_miembro(): 
    if request.method == 'POST':
       cur = connection.cursor()
       parada=request.form['parada']
       miembro=request.form['miembros']
       datos_miembro=funciones.dat_miembros(cur,parada,miembro)
    return render_template('digitadores.html',datos_miembro=datos_miembro,parada=parada ) 
 
@app.route('/redit_miembro',methods=['GUEST','POST']) 
def redit_miembro(): 
    if request.method == 'POST':
       cur = connection.cursor()
       parada=request.form['parada']
       identificador=request.form['identificador']
       nombre=request.form['nombre']
       cedula=request.form['cedula']
       telefono=request.form['telefono']
       funcion=request.form['funcion']
       funciones.actualizar_asoc(cur,parada,nombre,cedula,telefono,funcion,identificador)
       cur.close()
       return render_template('digitadores.html')


if __name__ == "__main__":
    app.run(debug=True,port=5600,host='0.0.0.0')