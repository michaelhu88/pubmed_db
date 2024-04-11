from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/search_pubmed')
def search_pubmed():
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        'db': 'pubmed',
        'term': 'breast cancer AND 2008[pdat] AND Science[journal]',
        'usehistory': 'y',
        'retmode': 'json'
    }
    response = requests.get(url, params=params)
    if response.ok:
        data = response.json()
        print(data)
        pmids = data.get("esearchresult", {}).get("idlist", [])
        return jsonify(pmids)
    else:
        return jsonify({"error": "Request failed"}), 500

# New endpoint to fetch citation information for a list of PMIDs
@app.route('/fetch_citations', methods=['GET'])
def fetch_citations():
    pmids = requests.args.get('pmids')  # PMIDs are expected as a comma-separated query parameter
    if not pmids:
        return jsonify({"error": "No PMIDs provided"}), 400
    
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        'db': 'pubmed',
        'id': pmids,
        'retmode': 'xml',  # Requesting XML format for the citation information
    }
    response = requests.get(url, params=params)
    if response.ok:
        # Returning the XML response directly for demonstration
        # In practice, consider parsing this XML to extract and return structured data
        return response.content, 200, {'Content-Type': 'application/xml'}
    else:
        return jsonify({"error": "Failed to fetch citations"}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)

