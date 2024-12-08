import random
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionProvideDiseaseInfo(Action):
    def name(self) -> Text:
        return "action_provide_disease_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        disease = next(tracker.get_latest_entity_values("disease"), None)

        disease_info = {
            "COVID-19": "COVID-19 is a highly contagious respiratory disease caused by the SARS-CoV-2 virus. It can spread through respiratory droplets and close contact.",
            "Influenza": "Influenza is a viral infection that attacks the respiratory system. It's typically seasonal and can cause mild to severe symptoms.",
            "Hepatitis": "Hepatitis is an inflammation of the liver, often caused by viral infections. There are different types (A, B, C) with varying transmission methods.",
            "HIV": "HIV (Human Immunodeficiency Virus) attacks the body's immune system. It can be managed with antiretroviral therapy but currently has no cure.",
            # Add more diseases here
        }

        if disease and disease.upper() in disease_info:
            dispatcher.utter_message(disease_info[disease.upper()])
        else:
            dispatcher.utter_message(
                "I have information on various diseases. Please specify which one you're interested in.")

        return []


class ActionSymptomInfo(Action):
    def name(self) -> Text:
        return "action_symptoms_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        disease = next(tracker.get_latest_entity_values("disease"), None)

        symptoms = {
            "COVID-19": "Common symptoms include fever, dry cough, fatigue, loss of taste/smell.",
            "Influenza": "Symptoms include sudden high fever, chills, muscle aches, headache, and respiratory issues.",
            "Hepatitis": "Symptoms may include yellowing of skin, dark urine, extreme fatigue, nausea, and abdominal pain.",
            # Add more symptoms
        }

        if disease and disease.upper() in symptoms:
            dispatcher.utter_message(symptoms[disease.upper()])
        else:
            dispatcher.utter_message("Symptoms vary by disease. Please specify which disease you want to know about.")

        return []


class ActionPreventionAdvice(Action):
    def name(self) -> Text:
        return "action_prevention_advice"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        general_prevention = [
            "Wash hands frequently with soap and water",
            "Use alcohol-based hand sanitizers",
            "Maintain social distancing",
            "Wear masks in crowded places",
            "Get vaccinated",
            "Avoid touching face with unwashed hands",
            "Maintain a healthy diet and exercise",
            "Get adequate sleep",
        ]

        dispatcher.utter_message("Here are some general prevention tips:\n" +
                                 "\n".join(f"- {tip}" for tip in general_prevention))

        return []


class ActionEmergencyAssessment(Action):
    def name(self) -> Text:
        return "action_emergency_assessment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        emergency_signs = [
            "Difficulty breathing",
            "Persistent chest pain or pressure",
            "Confusion or inability to wake",
            "Bluish lips or face",
            "High fever that doesn't respond to medication"
        ]

        dispatcher.utter_message(
            "If you're experiencing any of these emergency signs, seek immediate medical attention:\n" +
            "\n".join(f"- {sign}" for sign in emergency_signs))

        return []

# Add more custom actions as needed