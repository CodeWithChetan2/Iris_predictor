from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Annotated
import pickle
import numpy as np

import uvicorn

app=FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates=Jinja2Templates(directory='templates')


@app.get('/')
def home():
    return "Welcome"    
 
@app.get('/home',response_class=HTMLResponse)
def home(request:Request):
    return  templates.TemplateResponse('index.html', context={'request': request})

@app.post('/predict_iris',response_class=HTMLResponse)
async def predict(request:Request):
    form_data=await request.form()
    sepal_length=float(form_data.get('sepal_length'))
    sepal_width=float(form_data.get('sepal_width'))
    petal_length=float(form_data.get("petal_length"))
    petal_width=float(form_data.get('petal_width'))
    model=pickle.load(open("clf.pkl",'rb'))
    result=model.predict([[sepal_length,sepal_width,petal_length,petal_width]])[0]
    return templates.TemplateResponse("index.html",context={'request':request,'result':result})
    
if __name__=='__main__':
    uvicorn.run(app,port=500)
    


