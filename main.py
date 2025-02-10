from flask import Flask, render_template, request
from experta import *

app = Flask(__name__)


class Sintoma(Fact):
    """ Representa un síntoma médico reportado por el usuario. """
    pass


class DiagnosticoMedico(KnowledgeEngine):

    @Rule(Sintoma(fiebre=True), Sintoma(tos=True), Sintoma(dolor_cuerpo=True))
    def diagnosticar_gripe(self):
        print('hola')
        self.diagnostico = "Gripe 🤒"
        self.recomendaciones = "Descanso, líquidos y analgésicos."

    @Rule(Sintoma(fiebre=True), Sintoma(tos=True), Sintoma(dificultad_respirar=True), Sintoma(dolor_pecho=True))
    def diagnosticar_neumonia(self):
        self.diagnostico = "Neumonía 🏥"
        self.recomendaciones = "Consulta a un médico urgentemente."

    @Rule(Sintoma(fiebre=True), Sintoma(tos=True), Sintoma(dificultad_respirar=True), Sintoma(perdida_olfato=True), Sintoma(perdida_gusto=True))
    def diagnosticar_covid(self):
        self.diagnostico = "COVID-19 🦠"
        self.recomendaciones = "Aíslate y busca atención médica si los síntomas empeoran."

    @Rule(Sintoma(estornudos=True), Sintoma(picazon_ojos=True), Sintoma(congestion_nasal=True), Sintoma(fiebre=False))
    def diagnosticar_alergia(self):
        self.diagnostico = "Alergia 🤧"
        self.recomendaciones = "Usa antihistamínicos y evita los alérgenos."

    @Rule(Sintoma(dolor_cabeza=True), Sintoma(nauseas=True), Sintoma(sensibilidad_luz=True))
    def diagnosticar_migrana(self):
        self.diagnostico = "Migraña ⚡"
        self.recomendaciones = "Descansa en un lugar oscuro y evita el estrés."


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/diagnosticar', methods=['POST'])
def diagnosticar():
    # Obtener lista de síntomas desde el formulario
    sintomas_seleccionados = request.form.getlist("sintomas")
    sintomas_dict = {sintoma: True for sintoma in sintomas_seleccionados}

    motor = DiagnosticoMedico()
    motor.reset()

    for sintoma, presente in sintomas_dict.items():
        print(sintoma, presente)
        motor.declare(Sintoma(**{sintoma: presente}))

    motor.diagnostico = "No se pudo determinar un diagnóstico."
    motor.recomendaciones = "Consulta a un médico para una evaluación más precisa."
    motor.run()

    return render_template("index.html", diagnostico=motor.diagnostico, recomendaciones=motor.recomendaciones)
