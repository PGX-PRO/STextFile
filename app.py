from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
import requests
from io import BytesIO

app = Flask(__name__)

def acortar_url(link):
 try:
  response = requests.post('https://acut0x-qa7e.onrender.com',data={'url': link},headers={'Content-Type': 'application/x-www-form-urlencoded'})
  response.raise_for_status()
  soup = BeautifulSoup(response.text, 'html.parser')
  enlace_acortado = soup.find('a', class_='acortada')['href']
  return enlace_acortado
 except Exception as e:
  print(f"Error al acortar URL: {e}")
  return link

def upload(file_storage):
 url = "https://qu.ax/upload.php"
 headers = {
 "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Mobile Safari/537.36",
 "Referer": "https://qu.ax/"
 }
 file_data = BytesIO()
 file_storage.save(file_data)
 file_data.seek(0)
 files = {'files[]': (file_storage.filename, file_data)}
 data = {'expiry': '30'}
 r = requests.post(url, files=files, data=data, headers=headers)
 return r.json()

@app.route('/')
def index():
 success = request.args.get('success') == 'true'
 file_url = request.args.get('file_url')
 active_tab = request.args.get('active_tab', 'text')
 if file_url:
  file_url = acortar_url(file_url)
 return render_template('index.html',success=success,file_url=file_url,active_tab=active_tab)

@app.route('/upload', methods=['POST'])
def upload_file():
 if 'archivo' not in request.files:
  return render_template('index.html',error='No se seleccionó ningún archivo',active_tab='file')
 file = request.files['archivo']
 if file.filename == '':
  return render_template('index.html',error='No se seleccionó ningún archivo',active_tab='file')
 if file:
  result = upload(file)
  if result.get('success'):
   url_original = result['files'][0]['url']
   url_acortada = acortar_url(url_original)
   return render_template('index.html', success=True,file_url=url_acortada,active_tab='file')
  else:
   return render_template('index.html',error='Error al subir el archivo',active_tab='file')

@app.route('/upload_text', methods=['POST'])
def upload_text_file():
 if 'archivo' not in request.files:
  return jsonify({
  'success': False,
  'error': 'No se pudo crear el archivo de texto'
  })
 file = request.files['archivo']
 if file.filename == '':
  return jsonify({'success': False,'error': 'No se pudo crear el archivo de texto'})
 if file:
  result = upload(file)
  if result.get('success'):
   for file_info in result['files']:
    file_info['url'] = acortar_url(file_info['url'])
   return jsonify({'success': True,'files': result['files']})
  else:
   return jsonify({'success': False,'error': 'Error al subir el archivo de texto'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
