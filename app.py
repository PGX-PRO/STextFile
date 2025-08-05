from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
from urllib.parse import quote, unquote
import requests
from io import BytesIO

app = Flask(__name__)

headers = {
 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def acortar_url(link):
 try:
  response = requests.post('https://acut0x-qa7e.onrender.com', data={'url': link}, headers={'Content-Type': 'application/x-www-form-urlencoded'})
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
 files = {'files[]': (file_storage.filename, file_data, 'text/plain')}
 data = {'expiry': '30'}
 r = requests.post(url, files=files, data=data, headers=headers)
 return r.json()

@app.route('/')
def index():
 success = request.args.get('success') == 'true'
 file_url = request.args.get('file_url')
 active_tab = request.args.get('active_tab', 'text')
 if file_url:
  file_url = unquote(file_url)
 return render_template('index.html', success=success, file_url=file_url, active_tab=active_tab)

@app.route('/upload', methods=['POST'])
def upload_file():
 import base64

 if 'archivo' not in request.files:
  return render_template('index.html', error='No se seleccionó ningún archivo', active_tab='file')
 file = request.files['archivo']
 if file.filename == '':
  return render_template('index.html', error='No se seleccionó ningún archivo', active_tab='file')

 result = upload(file)
 if result.get('success'):
  url = result['files'][0]['url']
  final = acortar_url(url)
  return render_template('index.html', success=True, file_url=final, active_tab='file')

 try:
  print("El archivo original falló, reintentando subida con el archivo codificado a base64 y con cambio de nombre")

  file.stream.seek(0)
  file_bytes = file.stream.read()
  base64_bytes = base64.b64encode(file_bytes)

  base64_stream = BytesIO(base64_bytes)
  base64_stream.seek(0)

  from werkzeug.datastructures import FileStorage
  base64_file = FileStorage(stream=base64_stream, filename="archivo_base64.txt", content_type="text/plain")

  result2 = upload(base64_file)
  print("Respuesta del segundo intento (base64):", result2)

  if result2.get('success'):
   url = result2['files'][0]['url']
   url = f"https://decode-jfw1.onrender.com/base64/?link={url}"
   final = acortar_url(url)
   return render_template('index.html', success=True, file_url=final, active_tab='file')
  else:
   return render_template('index.html', error='Error al subir el archivo en base64', active_tab='file')
 except Exception as e:
  print("Error al procesar archivo como base64:", e)
  return render_template('index.html', error='Error al procesar archivo como base64', active_tab='file')

@app.route('/upload_text', methods=['POST'])
def upload_text_file():
 if 'archivo' not in request.files:
  return jsonify({'success': False, 'error': 'No se pudo crear el archivo de texto'})
 file = request.files['archivo']
 if file.filename == '':
  return jsonify({'success': False, 'error': 'No se pudo crear el archivo de texto'})
 if file:
  result = upload(file)
  if result.get('success'):
   url = result['files'][0]['url']
   if file.filename == "texto_base64.txt":
    link = f"https://decode-jfw1.onrender.com/base64/?link={url}"
   else:
    link = url
   final_url = acortar_url(link)
   return jsonify({'success': True, 'files': [{'url': final_url}]})
  else:
   return jsonify({'success': False, 'error': 'Error al subir el archivo de texto'})

if __name__ == '__main__':
 app.run(host='0.0.0.0', port=10000)
