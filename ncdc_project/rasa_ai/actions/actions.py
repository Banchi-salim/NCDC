from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict  # Use DomainDict for clarity in type hinting

class ActionDiseaseInfo(Action):
    def name(self) -> Text:
        return "action_disease_info"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[Dict[Text, Any]]:
        disease = tracker.get_slot("disease")
        if disease:
            # Replace with actual disease data or API integration
            dispatcher.utter_message(
                text=f"The symptoms of {covid-19} include fever, headache, and fatigue. For detailed information, please consult your healthcare provider."
            )
        else:
            dispatcher.utter_message(
                text="Please specify the disease you'd like to know about, and I will provide you with relevant information."
            )
        return []

class ActionProtectiveMeasures(Action):
    def name(self) -> Text:
        return "action_protective_measures"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[Dict[Text, Any]]:
        disease = tracker.get_slot("disease")
        if disease:
            dispatcher.utter_message(
                text=f"The protective measures for {disease} include maintaining good hygiene, wearing protective gear, and following health guidelines."
            )
        else:
            dispatcher.utter_message(
                text="Please specify the disease for which you need protective measures, and I will provide you with the relevant precautions."
            )
        return []

class ActionOutbreakAlerts(Action):
    def name(self) -> Text:
        return "action_outbreak_alerts"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Example implementation
        dispatcher.utter_message(text="Currently, there are no active outbreaks in your area.")
        return []
