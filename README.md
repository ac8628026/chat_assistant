### chat_assistant backend 

## hosted on aws using nginx 
##  Test in browser with backend URL : https://chat-assistant-backend.kgpian.site/docs

## ⚙️ Setup Instructions for local pc

### 1. Clone the Repository

```bash
git clone https://github.com/ac8628026/chat_assistant.git
cd chat_assistant

##create an venv 
python3 -m venv venv
source venv/bin/activate

## install dep
pip install -r requirements.txt

##create .env 
touch .env
GOOGLE_API_KEY = google_api_key


##run server
uvicorn main:app --reload
