import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from random import choice

# Set up Firebase credentials
cred = credentials.Certificate("to/serviceAccountKey.json")
firebase_admin.initialize_app(cred,{"databaseURL": "https://carrier-hcn1-default-rtdb.firebaseio.com"}  )
ref = db.reference('/')

class Firebase:
    def add_item(self,nxxnsx:int,queries:dict):
        queries.update({"total":1})
        item_ref = ref.child("carriers").child(str(nxxnsx)).child("ocn")
        item_ref.set(queries)

    def add_query(self,nxxnsx:int,query:str):
        item_ref = ref.child("carriers").child(str(nxxnsx)).child("ocn")
        print(item_ref.get())
        if self.check_existance(nxxnsx,query) : query = {query: item_ref.get()[query] + 1}
        else : query = {query:1}
        total = item_ref.get()["total"] + 1
        item_ref.update(query)
        item_ref.update({"total":total})
    
    def check_existance(self,nxxnsx:int,queryItem = None) -> bool:
        item_ref = ref.child("carriers").child(str(nxxnsx))
        if queryItem is None : return item_ref.get() is not None
        else: return queryItem in list(item_ref.get().keys())

    def insert_query(self,nxxnsx:int,query:str):
        if self.check_existance(nxxnsx): self.add_query(nxxnsx,query)
        else : self.add_item(nxxnsx,{query:1})

    def get_carrier(self,nxxnsx:int):
        probabilties_range = 3
        reference = ref.child("carriers").child(str(nxxnsx)).child("ocn")
        items:dict = reference.get()
        if items is None : return "None"
        total = items.pop("total")
        max_percentage = max(items.values()) * 100 / total
        print(max_percentage)
        return choice([i for i, value in items.items() if value * 100/total >= max(items.values()) - probabilties_range])
    