from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "pub_a40e4946712447c38670f69e0fdb967d"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_news', methods=['GET'])
def get_news():
    city = request.args.get('city', '')
    
    if not city:
        return jsonify({"status": "error", "message": "City parameter is missing"}), 400
        
    url = f"https://newsdata.io/api/1/news?apikey={API_KEY}&q={city}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        print("--- API DATA RECEIVED ---")
        
        if response.status_code == 200 and data.get("status") == "success":
            raw_results = data.get("results", [])
            articles = []
            
            for item in raw_results:
                articles.append({
                    "title": item.get("title"),
                    "url": item.get("link"),
                    "urlToImage": item.get("image_url"),
                    "description": item.get("description") or item.get("content") or "No description available.",
                    "publishedAt": item.get("pubDate", "Recent"),
                    "source": {
                        "name": item.get("source_id", "Live News")
                    }
                })
            
            return jsonify({"status": "success", "articles": articles[:10]})
        else:
            print("API Error Response:", data)
            return jsonify({"status": "error", "message": "API status failed"}), 400
            
    except Exception as e:
        print("Exception occurred:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
