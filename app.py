from flask import Flask, jsonify, session, redirect, url_for, request
from flask_cors import CORS  # Permite que React acceda a Flask desde otro dominio
import serial
import time

app = Flask(__name__)
app.secret_key = "una_clave_secreta"

CORS(app)  # Habilita CORS para todas las rutas

def comunicacion_balanza():
    
    try:
        with serial.Serial(
            port="/dev/ttyUSB0",  # Cambia si el puerto es diferente
            baudrate=9600,        
            bytesize=serial.EIGHTBITS,  
            parity=serial.PARITY_NONE,  
            stopbits=serial.STOPBITS_ONE,  
            timeout=1  
        ) as dispositivo:
            dispositivo.write(b'\x05')  # Enviar ENQ (0x05)
            time.sleep(1)  # Pequeña espera para la respuesta
            respuesta = dispositivo.read(100)
            
            if respuesta and respuesta[0] == 0x02:  
                try:
                    datos = respuesta[1:-2]  
                    peso = int(datos.decode('utf-8'))  
                    print(peso)
                    return peso
                    
                except ValueError:
                    return None
        
    except serial.SerialException:
        return None

@app.route("/peso", methods=["GET"])
def obtener_peso():
    peso = comunicacion_balanza()
    peso_prueba = 1500
    return jsonify({"peso": peso_prueba if peso_prueba is not None else "En espera..."})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
