# Developer Information

**Fuyad Hassan** - ID: 232-134-043  
**Guljar Hosen** - ID: 232-134-010

---

# Entity Recognition System

A powerful Named Entity Recognition (NER) system built with Flask and spaCy. It extracts and visualizes entities like Persons, Organizations, Dates, and more from text using a stunning, dynamic web interface with animated backgrounds, smooth transitions, and interactive elements.

## ✨ Features

- **Real-time Extraction**: Instantly identifies entities in text with advanced spaCy NLP models.
- **Dynamic Visual Interface**: Animated rainbow header, floating particles, and smooth transitions.
- **Interactive Animations**: Typewriter effects, bounce-in statistics, and hover animations.
- **Color-coded Visualization**: Beautiful entity highlighting with custom color schemes.
- **Responsive Design**: Modern UI with backdrop blur effects and gradient backgrounds.
- **JSON API**: RESTful endpoints for seamless integration.
- **Dockerized**: Easy deployment with Docker Compose.
- **Progress Feedback**: Animated loading indicators during text analysis.

## 🚀 Quick Start (Local)

1. **Install Dependencies**:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # On Windows
    # or
    source venv/bin/activate  # On macOS/Linux
    pip install -r requirements.txt
    python -m spacy download en_core_web_lg
    ```

2. **Run the Application**:
    ```bash
    python app.py
    ```

3. **Access**: Open [http://localhost:5000](http://localhost:5000)

## 🐳 Docker Deployment

1. **Build and Run**:
    ```bash
    docker-compose -f deployment/docker-compose.yml up --build -d
    ```

2. **Access**: Open [http://localhost:5000](http://localhost:5000)

## 💻 Command Line Usage

### Prerequisites
Make sure you have:
- Python 3.7+ installed
- Virtual environment set up with dependencies installed
- spaCy language model downloaded

### Step-by-Step Commands

1. **Navigate to the project directory**:
    ```bash
    cd "path/to/Named Entity Recognition"
    ```

2. **Activate the virtual environment**:
    ```bash
    # On Windows
    source .venv/Scripts/activate
    
    # On macOS/Linux
    source venv/bin/activate
    ```
    

3. **Start the Flask application**:
    ```bash
    python app.py
    ```

### Alternative: Direct execution
If you prefer not to activate the virtual environment:
```bash
# Windows
"C:/path/to/project/.venv/Scripts/python.exe" app.py

# macOS/Linux
/path/to/project/venv/bin/python app.py
```

### Expected Output
Once running, you should see:
```
============================================================
ENTITY RECOGNITION SYSTEM API
============================================================

Server running at: http://0.0.0.0:5000

Endpoints:
  POST /api/extract - Extract entities from text
  POST /api/batch - Batch entity extraction
  GET  /health - Health check

Press CTRL+C to stop
```

### Stopping the Application
- Press `Ctrl+C` in the terminal to stop the server
- The application runs in debug mode with auto-restart on code changes

### Troubleshooting
- **Import errors**: Ensure dependencies are installed with `pip install -r requirements.txt`
- **spaCy model missing**: Run `python -m spacy download en_core_web_lg`
- **Port already in use**: Change the port in `app.py` or kill the process using port 5000

## 🎨 UI Highlights

- **Animated Header**: Rainbow gradient background that continuously shifts colors
- **Particle Effects**: Floating background particles for ambient animation
- **Smooth Transitions**: Fade-in, slide-in, and bounce effects throughout the interface
- **Interactive Elements**: Ripple effects on buttons and scaling animations on hover
- **Progress Visualization**: Animated progress bar during entity extraction
- **Typewriter Animation**: Dynamic text reveal for the main title

## 📡 API Usage

**Endpoint**: `POST /api/extract`

**Body**:
```json
{
    "text": "Elon Musk bought Twitter for $44 billion."
}
```

**Response**:
```json
{
    "total_entities": 3,
    "entities": [
        {
            "text": "Elon Musk",
            "label": "PERSON",
            "start": 0,
            "end": 9
        },
        {
            "text": "Twitter",
            "label": "ORG",
            "start": 16,
            "end": 23
        },
        {
            "text": "$44 billion",
            "label": "MONEY",
            "start": 29,
            "end": 40
        }
    ],
    "entities_by_type": {
        "PERSON": ["Elon Musk"],
        "ORG": ["Twitter"],
        "MONEY": ["$44 billion"]
    },
    "people": ["Elon Musk"],
    "organizations": ["Twitter"],
    "highlighted_html": "<span class=\"entity-mark entity-PERSON\">Elon Musk</span> bought <span class=\"entity-mark entity-ORG\">Twitter</span> for <span class=\"entity-mark entity-MONEY\">$44 billion</span>."
}
```

## 📂 Repository

GitHub: [https://github.com/Fuyad22/Text_Entity.git](https://github.com/Fuyad22/Text_Entity.git)
