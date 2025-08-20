from flask import Flask, render_template
from bs4 import BeautifulSoup as bs
import requests as req
import base64
import json 

app = Flask(__name__)
url = "https://xn--72cz0evbxczc.com/"

def ENC(string):
	string_bytes = string.encode("ascii")
	base64_bytes = base64.b64encode(string_bytes)
	base64_hasil = base64_bytes.decode("ascii")
	return base64_hasil
	
def DEC(string):
	base64_bytes = string.encode("ascii")
	string_bytes = base64.b64decode(base64_bytes)
	decode_hasil = string_bytes.decode("ascii")
	return decode_hasil
	
@app.route("/")
def main():
	jek = []
	raw = req.get(url).text
	sup = bs(raw,'html.parser').find_all("a",{"class":"post-video"})
	
	for item in sup:
		links = item.get("href")
		title = item.get("title")
		thumb = item.find("img").get("src")
		
		jek.append(f'<img src="{thumb}" style="width:100%;padding-botom:1%;"/> {links} <br/><br/> ')
	return render_template('index.html', items=jek,title="momok")

@app.route('/page/<string:nomor>')
def page(nomor):
	dat = []
	raw = req.get(f"{url}page/{nomor}/").text
	sup = bs(raw,'html.parser').find("div",{"class":"latest-videos"}).find_all("a",{"class":"post-video"})
	
	for item in sup:
		links = item.get("href")
		title = item.get("title")
		thumb = item.find("img").get("src")
		#translated = GoogleTranslator(source='auto', target='en').translate(title)
		dat.append({"thumb":thumb,"target":ENC(links),"judul":title})
		
	return render_template('homepage.html',items=dat,nomor=int(nomor))

@app.route('/view/<string:link>')
def view(link):
	raw = req.get(DEC(link)).text
	src = bs(raw,'html.parser').find('iframe').get("src")
	if "/play/" not in src:
		res = bs(req.get(src).text,'html.parser').find_all("script")[5].text.strip()
		uid = res.split('const uid = "')[1].split('";')[0]
		tss = res.split('timestamp = "')[1].split('";')[0]
		tok = res.split('token = "')[1].split('";')[0]
		dat = req.post("https://mixapi.masteplayers.com/api/player-data",data={"uid":uid,"timestamp":tss,"token":tok}).json()['playlistIframe'][0]
	else:
		dat = src
		
	return render_template('view.html',link=dat)

if __name__ == "__main__":
    app.run()
