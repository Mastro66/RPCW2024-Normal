import csv
import json

# Função para formatar strings como URIs
def format_uri(value):
    return value.strip().replace(' ', '_').replace(',', '').replace('(', '').replace(')', '')

# Início do conteúdo TTL
ttl = """@prefix : <http://www.example.org/disease-ontology#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

:Ontology a owl:Ontology .

# Classes
:Disease a owl:Class .
:Symptom a owl:Class .
:Treatment a owl:Class .
:Patient a owl:Class .

# Properties
:hasSymptom a owl:ObjectProperty ;
    rdfs:domain :Disease ;
    rdfs:range :Symptom .

:hasTreatment a owl:ObjectProperty ;
    rdfs:domain :Disease ;
    rdfs:range :Treatment .

:exhibitsSymptom a owl:ObjectProperty ;
    rdfs:domain :Patient ;
    rdfs:range :Symptom .

:hasDescription a owl:DatatypeProperty ;
    rdfs:domain :Disease ;
    rdfs:range xsd:string .
"""

# Carregar o arquivo Disease_Syntoms.csv e criar instâncias de Disease e Symptom
with open('Disease_Syntoms.csv', newline='', encoding='utf-8') as csvfile:
    disease_symptoms = csv.DictReader(csvfile)
    for row in disease_symptoms:
        disease = format_uri(row['Disease'].strip())
        ttl += f"\n###  http://www.example.org/disease-ontology#{disease}\n"
        ttl += f":{disease} rdf:type :Disease .\n"
        
        for i in range(1, 18):  # Supondo que há até 17 sintomas por doença
            symptom_key = f'Symptom_{i}'
            symptom = row[symptom_key].strip()
            if symptom:
                symptom = format_uri(symptom)
                ttl += f":{symptom} rdf:type :Symptom .\n"
                ttl += f":{disease} :hasSymptom :{symptom} .\n"

# Carregar o arquivo Disease_Description.csv e associar descrições às instâncias de Disease
with open('Disease_Description.csv', newline='', encoding='utf-8') as csvfile:
    disease_descriptions = csv.DictReader(csvfile)
    for row in disease_descriptions:
        disease = format_uri(row['Disease'].strip())
        description = row['Description'].strip()
        ttl += f"\n:{disease} :hasDescription \"{description}\"^^xsd:string .\n"

# Salvar a ontologia como med_doencas.ttl
with open('med_doencas.ttl', 'w', encoding='utf-8') as output_file:
    output_file.write(ttl)

# Continuar adicionando os tratamentos ao TTL
with open('Disease_Treatment.csv', newline='', encoding='utf-8') as csvfile:
    disease_treatments = csv.DictReader(csvfile)
    for row in disease_treatments:
        disease = format_uri(row['Disease'].strip())
        for i in range(1, 5):  # Supondo que há até 4 precauções por doença
            treatment_key = f'Precaution_{i}'
            treatment = row[treatment_key].strip()
            if treatment:
                treatment = format_uri(treatment)
                ttl += f"\n:{treatment} rdf:type :Treatment .\n"
                ttl += f":{disease} :hasTreatment :{treatment} .\n"

# Salvar a ontologia como med_tratamentos.ttl
with open('med_tratamentos.ttl', 'w', encoding='utf-8') as output_file:
    output_file.write(ttl)

# Carregar o arquivo JSON com sintomas dos pacientes e criar instâncias de pacientes
with open('pg54470.json', encoding='utf-8') as jsonfile:
    patients = json.load(jsonfile)
    for patient in patients:
        patient_name = format_uri(patient["nome"])
        symptoms = patient["sintomas"]
        ttl += f"\n###  http://www.example.org/disease-ontology#{patient_name}\n"
        ttl += f":{patient_name} rdf:type :Patient ;\n"
        ttl += f'    :name "{patient["nome"]}"^^xsd:string ;\n'
        for symptom in symptoms:
            symptom = format_uri(symptom)
            ttl += f"    :exhibitsSymptom :{symptom} ;\n"
        ttl = ttl.rstrip(' ;\n') + " .\n"  # Remover o último ponto e vírgula e adicionar ponto final

# Salvar a ontologia como med_doentes.ttl
with open('med_doentes.ttl', 'w', encoding='utf-8') as output_file:
    output_file.write(ttl)

print("Ontologias criadas e salvas com sucesso.")
