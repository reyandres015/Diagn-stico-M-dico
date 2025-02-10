from flask import Flask, render_template, request
from experta import *

app = Flask(__name__)


class Sintoma(Fact):
    """ Representa un síntoma médico reportado por el usuario. """
    pass


class DiagnosticoMedico(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.diagnosticos_probables = {}

    def actualizar_probabilidad(self, enfermedad, peso):
        if enfermedad in self.diagnosticos_probables:
            self.diagnosticos_probables[enfermedad] += peso
        else:
            self.diagnosticos_probables[enfermedad] = peso

    @Rule(Sintoma(fiebre=True))
    def sintoma_fiebre(self):
        self.actualizar_probabilidad("Gripe 🤒", 1)
        self.actualizar_probabilidad("Neumonía 🏥", 1)
        self.actualizar_probabilidad("COVID-19 🦠", 1)

    @Rule(Sintoma(tos=True))
    def sintoma_tos(self):
        self.actualizar_probabilidad("Gripe 🤒", 1)
        self.actualizar_probabilidad("Neumonía 🏥", 1)
        self.actualizar_probabilidad("COVID-19 🦠", 1)

    @Rule(Sintoma(dolor_garganta=True))
    def sintoma_dolor_garganta(self):
        self.actualizar_probabilidad("Gripe 🤒", 5)
        self.actualizar_probabilidad("COVID-19 🦠", 1)

    @Rule(Sintoma(dificultad_respirar=True))
    def sintoma_dificultad_respirar(self):
        self.actualizar_probabilidad("Gripe 🤒", 2)
        self.actualizar_probabilidad("Neumonía 🏥", 5)
        self.actualizar_probabilidad("COVID-19 🦠", 5)

    @Rule(Sintoma(dolor_pecho=True))
    def sintoma_dolor_pecho(self):
        self.actualizar_probabilidad("Neumonía 🏥", 5)

    @Rule(Sintoma(perdida_olfato=True))
    def sintoma_perdida_olfato(self):
        self.actualizar_probabilidad("COVID-19 🦠", 5)

    @Rule(Sintoma(perdida_gusto=True))
    def sintoma_perdida_gusto(self):
        self.actualizar_probabilidad("COVID-19 🦠", 5)

    @Rule(Sintoma(estornudos=True))
    def sintoma_estornudos(self):
        self.actualizar_probabilidad("Alergia 🤧", 5)

    @Rule(Sintoma(congestion_nasal=True))
    def sintoma_congestion_nasal(self):
        self.actualizar_probabilidad("Alergia 🤧", 1)
        self.actualizar_probabilidad("Gripe 🤒", 2)
        self.actualizar_probabilidad("COVID-19 🦠", 1)

    @Rule(Sintoma(dolor_cabeza=True))
    def sintoma_dolor_cabeza(self):
        self.actualizar_probabilidad("Migraña ⚡", 5)

    @Rule(Sintoma(nauseas=True))
    def sintoma_nauseas(self):
        self.actualizar_probabilidad("Migraña ⚡", 5)

    @Rule(Sintoma(sensibilidad_luz=True))
    def sintoma_sensibilidad_luz(self):
        self.actualizar_probabilidad("Migraña ⚡", 5)

    def obtener_diagnostico(self):
        if not self.diagnosticos_probables:
            self.diagnostico = "No se pudo determinar un diagnóstico con los síntomas proporcionados."


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/diagnosticar', methods=['POST'])
def diagnosticar():
    sintomas_seleccionados = request.form.getlist("sintomas")
    sintomas_dict = {sintoma: True for sintoma in sintomas_seleccionados}

    motor = DiagnosticoMedico()
    motor.reset()

    for sintoma, presente in sintomas_dict.items():
        motor.declare(Sintoma(**{sintoma: presente}))

    motor.run()
    motor.obtener_diagnostico()
    # ordenar los diagnósticos por probabilidad
    motor.diagnosticos_probables = dict(
        sorted(motor.diagnosticos_probables.items(), key=lambda item: item[1], reverse=True))

    return render_template(
        "index.html",
        diagnosticosProbables=motor.diagnosticos_probables,
        totalPuntos=sum(motor.diagnosticos_probables.values()),
    )
