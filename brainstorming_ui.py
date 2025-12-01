from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
import tempfile
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Importiere den Skill
from brainstorming_skill.src.skill import execute_brainstorm_skill

app = Flask(__name__)
app.secret_key = 'dein-geheimer-schluessel-hier'  # Sollte in einer echten Anwendung aus einer Umgebungsvariable geladen werden

# Lade Umgebungsvariablen
load_dotenv('/home/dyai/Dokumente/DYAI_home/DEV/GIT_repos/Brainstorm_LLM/brainstorming_skill/.env')

# Konfiguriere Upload-Verzeichnis
UPLOAD_FOLDER = '/tmp/brainstorm_uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Erlaubte Dateitypen
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx', 'md', 'csv', 'json'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/brainstorm', methods=['POST'])
def brainstorm():
    try:
        # Hole die Benutzereingaben
        idea = request.form.get('idea', '').strip()
        context = request.form.get('context', '').strip()
        focus = request.form.get('focus', 'allgemein')
        
        # Dateien verarbeiten, falls vorhanden
        uploaded_context = ""
        if 'files' in request.files:
            files = request.files.getlist('files')
            for file in files:
                if file and file.filename != '' and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    
                    # Lese den Inhalt der Datei
                    content = read_file_content(filepath)
                    uploaded_context += f"\n\nInhalt aus {filename}:\n{content}"
                    
                    # Lösche die Datei nach der Verarbeitung
                    os.remove(filepath)
        
        # Kombiniere den Benutzerkontext mit dem aus den Dateien
        full_context = context + uploaded_context if context else uploaded_context
        
        if not idea:
            flash('Bitte geben Sie eine Idee ein', 'error')
            return redirect(url_for('index'))
        
        # Erstelle die Input-Daten für den Skill
        inputs = {
            "idea": idea,
            "context": full_context,
            "focus": focus,
            "round_info": "Erste Iteration"
        }
        
        # Führe den Skill aus
        result = execute_brainstorm_skill(inputs, use_mock=False)
        
        # Zeige das Ergebnis an
        return render_template('result.html', result=result, idea=idea)
        
    except Exception as e:
        flash(f'Fehler bei der Verarbeitung: {str(e)}', 'error')
        app.logger.error(f'Fehler bei der Verarbeitung: {str(e)}')
        return redirect(url_for('index'))

def read_file_content(filepath):
    """Liest den Inhalt einer Datei basierend auf ihrem Typ"""
    ext = os.path.splitext(filepath)[1].lower()
    
    try:
        if ext == '.txt':
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        elif ext == '.pdf':
            import PyPDF2
            with open(filepath, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text
        elif ext == '.md':
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        elif ext == '.json':
            import json
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return json.dumps(data, ensure_ascii=False, indent=2)
        else:
            # Als Textdatei behandeln
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
    except Exception as e:
        return f"Fehler beim Lesen der Datei {os.path.basename(filepath)}: {str(e)}"

@app.route('/api/brainstorm', methods=['POST'])
def brainstorm_api():
    """API-Endpunkt für Brainstorming-Anfragen"""
    try:
        data = request.get_json()
        
        idea = data.get('idea', '').strip()
        context = data.get('context', '').strip()
        focus = data.get('focus', 'allgemein')
        round_info = data.get('round_info', 'Erste Iteration')
        
        if not idea:
            return jsonify({'error': 'Idee ist erforderlich'}), 400
        
        inputs = {
            "idea": idea,
            "context": context,
            "focus": focus,
            "round_info": round_info
        }
        
        result = execute_brainstorm_skill(inputs, use_mock=False)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Stelle sicher, dass das Upload-Verzeichnis existiert
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Starte den Server
    print("Starte den Brainstorming UI Server...")
    print("Öffne http://localhost:5000 in deinem Browser")
    app.run(debug=True, host='0.0.0.0', port=5000)