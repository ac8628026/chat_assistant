### chat_assistant backend 

## hosted on aws using nginx 
##  Test in browser with backend URL : https://chat-assistant-backend.kgpian.site/docs

## ⚙️ Setup Instructions for local pc

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/chat_assistant_backend.git
cd chat_assistant_backend

##create an venv 
python3 -m venv venv
source venv/bin/activate

## install dep
pip install -r requirements.txt
uvicorn main:app --reload
