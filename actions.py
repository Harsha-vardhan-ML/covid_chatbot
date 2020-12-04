# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
from typing import Any, Text, Dict, List
from rasa_sdk import  Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import requests

class Actioncovid(Action): #custom action for getting the number of covid cases in an state
    
    def name(self) -> Text:
         return "action_covid"

    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: DomainDict) -> List[Dict[Text, Any]]:
        #use the below api to get the json format of the reports of covid cases
         response = requests.get("https://api.covid19india.org/data.json").json()
         name = tracker.get_slot('NAME') #get the slot values
         state = tracker.get_slot('STATE')
         #print(state.title())
         message = "please enter correct state name" #if you enter a wrong state name, display this message
         for i in response["statewise"]: #check for the state wise covid cases
            if i['state'] == state.title(): #find the user entered state details
                #print(i['state'])
                message = "Hey "+name+"! "+"number of cases in "+state+":: "+"active cases: "+i['active']+" confirmed cases: "+i['confirmed']+" recovered cases: "+i['recovered']
                #print(message)
         dispatcher.utter_message(message) #report back to user

         return []

#custom action for validating the slot in form:
# if we want we can use this to check whether user entered correct state name
# and if it is wrong ask again to enter the state name
'''class Validate_form_covid(FormValidationAction):
    def name(self) -> Text:
        return "validate_form_coivd"

    @staticmethod
    def names_db() -> List[Text]:
        
        """Database of supported cuisines"""
        response = requests.get("https://api.covid19india.org/data.json").json()
        state_names=[]
        for i in response['statewise']:
            state_names.append(i['state'])

        return state_names
    def validate_STATE(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""

        if slot_value.title() in self.names_db():
            # validation succeeded, set the value of the "cuisine" slot to value
            return {"STATE": slot_value}
        else:
            # validation failed, set this slot to None so that the
            # user will be asked for the slot again
           # message = "please enter correct state name"
            
            return {"STATE": None}'''









