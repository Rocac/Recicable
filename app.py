from flask import Flask, render_template, request
import pickle
from skfuzzy import control as ctrl

# Cargar el modelo fuzzy desde el archivo .pkl
with open("modelo_fuzzy.pkl", "rb") as archivo:
    clasificacion_ctrl = pickle.load(archivo)

app = Flask(__name__)

# Función para ejecutar el modelo
def clasificar_residuo(peso_val, suciedad_val, material_val):
    sim = ctrl.ControlSystemSimulation(clasificacion_ctrl)
    sim.input['peso'] = peso_val
    sim.input['suciedad'] = suciedad_val
    sim.input['material'] = material_val
    sim.compute()

    resultado = sim.output['clasificacion']
    if resultado < 0.5:
        return "ORGÁNICO"
    elif resultado < 1.5:
        return "RECICLABLE"
    else:
        return "NO RECICLABLE"

# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta que procesa el formulario
@app.route('/clasificar', methods=['POST'])
def clasificar():
    peso = float(request.form['peso'])
    suciedad = float(request.form['suciedad'])
    material = int(request.form['material'])

    resultado = clasificar_residuo(peso, suciedad, material)
    return render_template('index.html', resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)
