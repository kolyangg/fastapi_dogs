from enum import Enum
from fastapi import FastAPI, Path, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get('/')
def root():
    return 'Hello'

@app.post('/post')
def get_post() -> Timestamp:
    max_id = max(item.id for item in post_db)
    new_timestamp = Timestamp(id = max_id + 1, timestamp=int(datetime.now().strftime('%Y%m%d%H%M%S')))
    post_db.append(new_timestamp)
    return new_timestamp

@app.get('/dog', response_model=list[Dog]) # Need to do list[Dog] to return several items
def get_dogs(kind: DogType = None): # None means parameter is optional
    if not kind:
        return [dict(dogs_db[i]) for i in dogs_db.keys()]
    else:
        return [dict(dogs_db[i]) for i in dogs_db.keys() if dict(dogs_db[i])['kind'] == kind]
        
@app.post('/dog', summary='Create Dog')
def create_dog(dog: Dog) -> Dog:
    for i in dogs_db.keys():
        if dict(dogs_db[i])['pk'] == dog.pk:
            raise HTTPException(status_code=409, detail='The specified PK already exists.')
    
    dogs_db[dog.pk] = dog
    return dog

@app.get('/dog/{pk}', summary='Get Dog by Pk')
def get_dog_by_pk(pk: int) -> Dog:
    # Check if this Pk is not in dogs_db and raise Exception
    keep = False
    for i in dogs_db.keys(): 
        if dict(dogs_db[i])['pk'] == pk:
            keep = True
    if keep == False:
        raise HTTPException(status_code=404, detail='The specified PK value not found.')
    
    return dogs_db[pk]

@app.patch('/dog/{pk}', summary='Update Dog') # TO CHECK!!!
def get_dog_by_pk(pk: int, dog: Dog) -> Dog:
    # Check if this Pk is not in dogs_db and raise Exception
    keep = False
    for i in dogs_db.keys(): 
        if dict(dogs_db[i])['pk'] == pk:
            keep = True
    if keep == False:
        raise HTTPException(status_code=404, detail='The specified PK value not found.')
    
    # Check if this Pk != Dog.pk and raise Exception
    if pk != dog.pk:
        raise HTTPException(status_code=404, detail='The specified PK values do not match.')

    dogs_db[dog.pk] = dog
    
    return dogs_db[pk]
