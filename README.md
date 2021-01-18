pip3 install -r requirements.txt

uvicorn app.main:app --host 0.0.0.0 --port 9000

docker build -t taskfastapiimage . 
docker run -d --name taskfastapicontainer -p 9000:9000 taskfastapiimage