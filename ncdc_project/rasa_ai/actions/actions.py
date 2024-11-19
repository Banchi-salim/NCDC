from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionDiseaseInfo(Action):
    def name(self) -> Text:
        return "action_disease_info"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        disease = tracker.get_slot("disease")
        if disease:
            # Replace with actual disease data or API integration
            dispatcher.utter_message(text=f"The symptoms of {disease} include fever, headache, and fatigue.")
        else:
            dispatcher.utter_message(text="Please specify the disease you'd like to know about.")
        return []

class ActionProtectiveMeasures(Action):
    def name(self) -> Text:
        return "action_protective_measures"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        disease = tracker.get_slot("disease")
        if disease:
            dispatcher.utter_message(text=f"The protective measures for {disease} include using protective gear and maintaining hygiene.")
        else:
            dispatcher.utter_message(text="Please specify the disease for which you need protective measures.")
        return []

class ActionOutbreakAlerts(Action):
    def name(self) -> Text:
        return "action_outbreak_alerts"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Example: Replace with real outbreak data or API integration
        dispatcher.utter_message(text="Currently, there are no active outbreaks in your area. Stay tuned for updates.")
        return []
