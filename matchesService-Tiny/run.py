import uvicorn
if __name__=='__main__':
 uvicorn.run('matches_app.main:app',host='0.0.0.0',port=8003,reload=True)
