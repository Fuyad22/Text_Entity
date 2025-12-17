"""
Named Entity Recognition Web Application
Real-time entity extraction with beautiful web interface
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import spacy
import json
from collections import defaultdict, Counter
import re

app = Flask(__name__)
CORS(app)

# Load spaCy model
import sys
import subprocess

# Load spaCy model
try:
    nlp = spacy.load('en_core_web_lg')
except OSError:
    print("Downloading language model 'en_core_web_lg'...")
    subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_lg"])
    nlp = spacy.load('en_core_web_lg')

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Entity Recognition System</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(45deg, #1a1a2e, #16213e, #0f3460, #1a1a2e);
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
            min-height: 100vh;
            padding: 20px;
            overflow-x: hidden;
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        .particles {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: -1;
        }
        
        .particle {
            position: absolute;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 50%;
            animation: float 20s linear infinite;
        }
        
        @keyframes float {
            0% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
            10% { opacity: 1; }
            90% { opacity: 1; }
            100% { transform: translateY(-100vh) rotate(360deg); opacity: 0; }
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
            animation: slideIn 1s ease-out;
        }
        
        @keyframes slideIn {
            from { transform: translateY(50px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 20%, #f093fb 40%, #f5576c 60%, #4facfe 80%, #00f2fe 100%);
            background-size: 400% 400%;
            color: white;
            padding: 40px;
            text-align: center;
            position: relative;
            overflow: hidden;
            animation: headerRainbow 10s ease-in-out infinite;
        }
        
        @keyframes headerRainbow {
            0% { background-position: 0% 50%; }
            25% { background-position: 100% 50%; }
            50% { background-position: 100% 0%; }
            75% { background-position: 0% 100%; }
            100% { background-position: 0% 50%; }
        }
        
        .header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: pulse 4s ease-in-out infinite;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            position: relative;
            z-index: 1;
            animation: typeWriter 3s steps(40, end);
            overflow: hidden;
            white-space: nowrap;
            border-right: 3px solid white;
        }
        
        @keyframes typeWriter {
            from { width: 0; }
            to { width: 100%; }
        }
        
        .header p {
            position: relative;
            z-index: 1;
            opacity: 0;
            animation: fadeIn 1s 3s forwards;
        }
        
        @keyframes fadeIn {
            to { opacity: 1; }
        }
        
        .content {
            padding: 40px;
        }
        
        .input-section {
            margin-bottom: 30px;
            animation: fadeInUp 1s 0.5s both;
        }
        
        @keyframes fadeInUp {
            from { transform: translateY(30px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        
        label {
            display: block;
            font-size: 1.1em;
            font-weight: 600;
            margin-bottom: 10px;
            color: #333;
            animation: fadeIn 1s 0.7s both;
        }
        
        textarea {
            width: 100%;
            min-height: 150px;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 1em;
            font-family: inherit;
            resize: vertical;
            transition: all 0.3s ease;
            animation: fadeIn 1s 0.9s both;
        }
        
        textarea:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
            transform: scale(1.02);
        }
        
        .button-group {
            display: flex;
            gap: 15px;
            margin-top: 20px;
            animation: fadeIn 1s 1.1s both;
        }
        
        button {
            flex: 1;
            padding: 15px;
            font-size: 1.1em;
            font-weight: 600;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        
        button::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 50%;
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }
        
        button:hover::before {
            width: 300px;
            height: 300px;
        }
        
        .btn-extract {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .btn-extract:hover {
            transform: translateY(-3px) scale(1.05);
            box-shadow: 0 15px 30px rgba(102, 126, 234, 0.4);
        }
        
        .btn-clear {
            background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%);
            color: #666;
        }
        
        .btn-clear:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }
        
        .results {
            display: none;
            margin-top: 30px;
            animation: fadeInUp 0.8s ease-out;
        }
        
        .entity-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            transition: transform 0.3s ease;
            animation: bounceIn 0.6s ease-out;
        }
        
        .stat-card:nth-child(1) { animation-delay: 0.1s; }
        .stat-card:nth-child(2) { animation-delay: 0.2s; }
        .stat-card:nth-child(3) { animation-delay: 0.3s; }
        .stat-card:nth-child(4) { animation-delay: 0.4s; }
        
        @keyframes bounceIn {
            0% { transform: scale(0.3); opacity: 0; }
            50% { transform: scale(1.05); }
            70% { transform: scale(0.9); }
            100% { transform: scale(1); opacity: 1; }
        }
        
        .stat-card:hover {
            transform: translateY(-5px) scale(1.05);
        }
        
        .stat-number {
            font-size: 2.5em;
            font-weight: 700;
            animation: countUp 2s ease-out;
        }
        
        @keyframes countUp {
            from { transform: translateY(20px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        
        .stat-label {
            font-size: 0.9em;
            opacity: 0.9;
            margin-top: 5px;
        }
        
        .highlighted-text {
            background: white;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            padding: 25px;
            margin-bottom: 30px;
            line-height: 2;
            font-size: 1.1em;
            animation: slideInLeft 0.8s ease-out;
        }
        
        @keyframes slideInLeft {
            from { transform: translateX(-50px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        .entity-mark {
            padding: 2px 8px;
            border-radius: 5px;
            font-weight: 600;
            white-space: nowrap;
            display: inline-block;
            margin: 2px;
            transition: transform 0.2s ease;
        }
        
        .entity-mark:hover {
            transform: scale(1.1);
        }
        
        .entity-PERSON { background: #aa9cfc; color: white; }
        .entity-ORG { background: #7aecec; color: #333; }
        .entity-GPE { background: #feca74; color: #333; }
        .entity-LOC { background: #ff9561; color: white; }
        .entity-DATE { background: #bfe1d9; color: #333; }
        .entity-MONEY { background: #e4e7d2; color: #333; }
        .entity-PRODUCT { background: #ffeb80; color: #333; }
        .entity-EVENT { background: #ff6b6b; color: white; }
        
        .entity-lists {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }
        
        .entity-list {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            animation: fadeInUp 0.8s ease-out;
            transition: transform 0.3s ease;
        }
        
        .entity-list:hover {
            transform: translateY(-5px);
        }
        
        .entity-list h3 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.2em;
        }
        
        .entity-item {
            background: white;
            padding: 10px;
            margin: 8px 0;
            border-radius: 5px;
            border-left: 3px solid #667eea;
            transition: all 0.3s ease;
            animation: slideInRight 0.6s ease-out;
        }
        
        .entity-item:nth-child(1) { animation-delay: 0.1s; }
        .entity-item:nth-child(2) { animation-delay: 0.2s; }
        .entity-item:nth-child(3) { animation-delay: 0.3s; }
        
        @keyframes slideInRight {
            from { transform: translateX(50px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        .entity-item:hover {
            transform: translateX(10px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .legend {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            animation: fadeIn 1s ease-out;
        }
        
        .legend h3 {
            margin-bottom: 15px;
            color: #333;
        }
        
        .legend-items {
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
        }
        
        .legend-item {
            display: flex;
            align-items: center;
            gap: 8px;
            transition: transform 0.2s ease;
        }
        
        .legend-item:hover {
            transform: scale(1.05);
        }
        
        .legend-color {
            width: 30px;
            height: 20px;
            border-radius: 5px;
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
            animation: fadeIn 0.5s ease-out;
        }
        
        .progress-bar {
            width: 100%;
            height: 8px;
            background: #e0e0e0;
            border-radius: 4px;
            overflow: hidden;
            margin: 20px 0;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            width: 0%;
            animation: progress 2s ease-in-out infinite;
        }
        
        @keyframes progress {
            0% { width: 0%; }
            50% { width: 70%; }
            100% { width: 100%; }
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .examples {
            margin-top: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
            animation: fadeInUp 1s 1.5s both;
        }
        
        .example-btn {
            display: block;
            width: 100%;
            text-align: left;
            padding: 12px 15px;
            margin: 8px 0;
            background: white;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .example-btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.1), transparent);
            transition: left 0.5s;
        }
        
        .example-btn:hover::before {
            left: 100%;
        }
        
        .example-btn:hover {
            border-color: #667eea;
            transform: translateX(10px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.2);
        }
    </style>
</head>
<body>
    <div class="particles" id="particles"></div>
    <div class="container">
        <div class="header">
            <h1>🔍 Entity Recognition System</h1>
            <p>AI-Powered Named Entity Extraction & Analysis</p>
        </div>
        
        <div class="content">
            <div class="input-section">
                <label for="inputText">Enter Text for Analysis:</label>
                <textarea id="inputText" placeholder="Paste or type any text here to extract entities (people, organizations, locations, dates, etc.)..."></textarea>
                
                <div class="button-group">
                    <button class="btn-extract" onclick="extractEntities()">🔍 Extract Entities</button>
                    <button class="btn-clear" onclick="clearAll()">🗑️ Clear</button>
                </div>
            </div>
            
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <div class="progress-bar">
                    <div class="progress-fill"></div>
                </div>
                <p style="margin-top: 15px; color: #666;">Analyzing text...</p>
            </div>
            
            <div class="results" id="results">
                <div class="entity-stats" id="stats"></div>
                
                <div class="legend">
                    <h3>📊 Entity Types Legend</h3>
                    <div class="legend-items">
                        <div class="legend-item">
                            <div class="legend-color" style="background: #aa9cfc;"></div>
                            <span>PERSON - People names</span>
                        </div>
                        <div class="legend-item">
                            <div class="legend-color" style="background: #7aecec;"></div>
                            <span>ORG - Organizations</span>
                        </div>
                        <div class="legend-item">
                            <div class="legend-color" style="background: #feca74;"></div>
                            <span>GPE - Countries/Cities</span>
                        </div>
                        <div class="legend-item">
                            <div class="legend-color" style="background: #ff9561;"></div>
                            <span>LOC - Locations</span>
                        </div>
                        <div class="legend-item">
                            <div class="legend-color" style="background: #bfe1d9;"></div>
                            <span>DATE - Dates/Times</span>
                        </div>
                        <div class="legend-item">
                            <div class="legend-color" style="background: #e4e7d2;"></div>
                            <span>MONEY - Monetary values</span>
                        </div>
                    </div>
                </div>
                
                <h3 style="margin-bottom: 15px; color: #333;">📝 Highlighted Text</h3>
                <div class="highlighted-text" id="highlightedText"></div>
                
                <h3 style="margin-bottom: 15px; color: #333;">📋 Extracted Entities</h3>
                <div class="entity-lists" id="entityLists"></div>
            </div>
            
            <div class="examples">
                <h3>📌 Try These Examples:</h3>
                <button class="example-btn" onclick="loadExample(0)">
                    Example 1: Business news article
                </button>
                <button class="example-btn" onclick="loadExample(1)">
                    Example 2: Historical event
                </button>
                <button class="example-btn" onclick="loadExample(2)">
                    Example 3: Contact information
                </button>
            </div>
        </div>
    </div>
    
    <script>
        // Create floating particles
        function createParticles() {
            const particlesContainer = document.getElementById('particles');
            for (let i = 0; i < 50; i++) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                particle.style.left = Math.random() * 100 + '%';
                particle.style.width = Math.random() * 6 + 2 + 'px';
                particle.style.height = particle.style.width;
                particle.style.animationDelay = Math.random() * 20 + 's';
                particle.style.animationDuration = (Math.random() * 10 + 10) + 's';
                particlesContainer.appendChild(particle);
            }
        }
        
        createParticles();
        
        const examples = [
            "Apple Inc. was founded by Steve Jobs in Cupertino, California on April 1, 1976. The company is now valued at over $2.5 trillion. Tim Cook became CEO in 2011.",
            "World War II ended on September 2, 1945 when Japan formally surrendered to the Allied forces. The war had begun on September 1, 1939 in Europe.",
            "Contact John Smith at john.smith@company.com or call (555) 123-4567. Our office is located at 123 Main Street, New York, NY 10001."
        ];
        
        function loadExample(index) {
            document.getElementById('inputText').value = examples[index];
        }
        
        function clearAll() {
            document.getElementById('inputText').value = '';
            document.getElementById('results').style.display = 'none';
        }
        
        async function extractEntities() {
            const text = document.getElementById('inputText').value.trim();
            
            if (!text) {
                alert('Please enter some text to analyze!');
                return;
            }
            
            const loading = document.getElementById('loading');
            const results = document.getElementById('results');
            
            loading.style.display = 'block';
            results.style.display = 'none';
            
            try {
                const response = await fetch('/api/extract', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: text })
                });
                
                const data = await response.json();
                displayResults(data);
            } catch (error) {
                alert('Error analyzing text. Please try again.');
                console.error(error);
            } finally {
                loading.style.display = 'none';
            }
        }
        
        function displayResults(data) {
            // Display stats
            const stats = document.getElementById('stats');
            stats.innerHTML = `
                <div class="stat-card">
                    <div class="stat-number">${data.total_entities}</div>
                    <div class="stat-label">Total Entities</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${Object.keys(data.entities_by_type).length}</div>
                    <div class="stat-label">Entity Types</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${data.people.length}</div>
                    <div class="stat-label">People</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${data.organizations.length}</div>
                    <div class="stat-label">Organizations</div>
                </div>
            `;
            
            // Display highlighted text
            document.getElementById('highlightedText').innerHTML = data.highlighted_html;
            
            // Display entity lists
            const entityLists = document.getElementById('entityLists');
            let listsHtml = '';
            
            for (const [type, entities] of Object.entries(data.entities_by_type)) {
                if (entities.length > 0) {
                    listsHtml += `
                        <div class="entity-list">
                            <h3>${type} (${entities.length})</h3>
                            ${entities.map(e => `<div class="entity-item">${e}</div>`).join('')}
                        </div>
                    `;
                }
            }
            
            entityLists.innerHTML = listsHtml;
            
            document.getElementById('results').style.display = 'block';
        }
    </script>
</body>
</html>
"""

# API Routes
@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/extract', methods=['POST'])
def extract_entities():
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Process with spaCy
        doc = nlp(text)
        
        # Extract entities
        entities = []
        entities_by_type = defaultdict(list)
        
        for ent in doc.ents:
            entities.append({
                'text': ent.text,
                'label': ent.label_,
                'start': ent.start_char,
                'end': ent.end_char
            })
            entities_by_type[ent.label_].append(ent.text)
        
        # Remove duplicates
        for key in entities_by_type:
            entities_by_type[key] = list(set(entities_by_type[key]))
        
        # Get specific types
        people = [ent.text for ent in doc.ents if ent.label_ == 'PERSON']
        organizations = [ent.text for ent in doc.ents if ent.label_ == 'ORG']
        locations = [ent.text for ent in doc.ents if ent.label_ in ['GPE', 'LOC']]
        dates = [ent.text for ent in doc.ents if ent.label_ == 'DATE']
        
        # Create highlighted HTML
        highlighted_html = create_highlighted_text(text, doc)
        
        return jsonify({
            'total_entities': len(entities),
            'entities': entities,
            'entities_by_type': dict(entities_by_type),
            'people': list(set(people)),
            'organizations': list(set(organizations)),
            'locations': list(set(locations)),
            'dates': list(set(dates)),
            'highlighted_html': highlighted_html
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/batch', methods=['POST'])
def batch_extract():
    try:
        data = request.get_json()
        texts = data.get('texts', [])
        
        if not texts:
            return jsonify({'error': 'No texts provided'}), 400
        
        results = []
        for text in texts:
            doc = nlp(text)
            entities = [{'text': ent.text, 'label': ent.label_} for ent in doc.ents]
            results.append({'text': text[:100] + '...', 'entities': entities})
        
        return jsonify({'results': results})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def create_highlighted_text(text, doc):
    """Create HTML with highlighted entities"""
    html_parts = []
    last_end = 0
    
    for ent in doc.ents:
        # Add text before entity
        html_parts.append(text[last_end:ent.start_char])
        
        # Add highlighted entity
        html_parts.append(
            f'<span class="entity-mark entity-{ent.label_}">'
            f'{ent.text} <small>[{ent.label_}]</small></span>'
        )
        
        last_end = ent.end_char
    
    # Add remaining text
    html_parts.append(text[last_end:])
    
    return ''.join(html_parts)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'model': 'en_core_web_lg'})

if __name__ == '__main__':
    print("="*60)
    print("ENTITY RECOGNITION SYSTEM API")
    print("="*60)
    print("\nServer running at: http://0.0.0.0:5000")
    print("\nEndpoints:")
    print("  POST /api/extract - Extract entities from text")
    print("  POST /api/batch - Batch entity extraction")
    print("  GET  /health - Health check")
    print("\nPress CTRL+C to stop\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)