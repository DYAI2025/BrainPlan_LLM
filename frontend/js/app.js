// app.js - Frontend-Logik für den Brainstorming Assistant

// Funktion zum Senden der Brainstorming-Anfrage an die API
async function submitBrainstorm(idea, context, focus, files) {
    // Anzeige des Ladezustands
    const mainContent = document.querySelector('main');
    mainContent.innerHTML = '<div class="loading">Brainstorming läuft... Bitte warten Sie einen Moment.</div>';

    // Dateien verarbeiten (in einer echten Implementierung würden diese
    // entweder direkt hochgeladen oder als Text extrahiert)
    let fileContent = '';
    if (files && files.length > 0) {
        for (let i = 0; i < files.length; i++) {
            const file = files[i];
            // In einer echten Implementierung würden Dateien entweder
            // direkt zum Backend hochgeladen oder als Textinhalt verarbeitet
            fileContent += `\n\nInhalt aus ${file.name} wurde analysiert`;
        }
    }

    const fullContext = context + fileContent;

    try {
        // API-Aufruf an Backend (in einer echten Implementierung)
        // Hier verwenden wir einen Mock-Endpunkt für die Demonstration
        const response = await fetch('https://brainstorm-backend.example.com/api/brainstorm', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                idea: idea,
                context: fullContext,
                focus: focus,
                round_info: 'Erste Iteration'
            })
        });

        if (!response.ok) {
            throw new Error(`API Error: ${response.statusText}`);
        }

        const result = await response.json();
        return result;
    } catch (error) {
        console.error('Fehler beim Brainstorming:', error);
        
        // Anzeige des Fehlers
        mainContent.innerHTML = `
            <div class="error">
                <h2>Fehler beim Verarbeiten der Anfrage</h2>
                <p>${error.message}</p>
                <p>Bitte überprüfen Sie, ob das Backend ordnungsgemäß läuft und die API-URL korrekt ist.</p>
                <a href="index.html" class="btn">Zurück zum Formular</a>
            </div>
        `;
        throw error;
    }
}

// Hilfsfunktion zum Lesen von Dateien als Text
function readFileAsText(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = reject;
        reader.readAsText(file);
    });
}

// Funktion zum Anzeigen der Ergebnisse
function displayResult(result, idea) {
    // In einer echten Implementierung würden die Ergebnisdaten
    // in die entsprechenden HTML-Elemente eingefügt
    document.getElementById('original-idea-text').textContent = idea;
    document.getElementById('problem-statement').textContent = result.problem_statement || 'Wird generiert...';
    document.getElementById('goals-kpis').textContent = result.goals_kpis || 'Wird generiert...';
    document.getElementById('functional-requirements').innerHTML = formatRequirements(result.functional_requirements) || '<p>Wird generiert...</p>';
    document.getElementById('nonfunctional-requirements').innerHTML = formatRequirements(result.nonfunctional_requirements) || '<p>Wird generiert...</p>';
    document.getElementById('risks-assumptions').textContent = result.risks_assumptions || 'Wird generiert...';
    document.getElementById('implementation-potential').textContent = result.implementation_potential || 'Wird generiert...';
    document.getElementById('task-list').innerHTML = formatList(result.task_list) || '<p>Wird generiert...</p>';
    document.getElementById('test-ideas').innerHTML = formatList(result.test_ideas) || '<p>Wird generiert...</p>';
    document.getElementById('prompt-planner').textContent = result.followup_prompts?.prompt_planner || 'Wird generiert...';
    document.getElementById('prompt-architect').textContent = result.followup_prompts?.prompt_architect || 'Wird generiert...';
    document.getElementById('prompt-dev').textContent = result.followup_prompts?.prompt_dev || 'Wird generiert...';
    
    // Verstecke das Formular und zeige die Ergebnisseite
    document.querySelector('form').style.display = 'none';
    
    // Scrollen zum Anfang der Ergebnisse
    window.scrollTo(0, 0);
}

// Hilfsfunktionen zur Formatierung der Ergebnisse
function formatRequirements(reqText) {
    if (!reqText) return '<p>Keine Anforderungen vorhanden</p>';
    
    const reqLines = reqText.split('\n').filter(line => line.trim() !== '');
    let html = '<ul class="requirements-list">';
    
    reqLines.forEach(line => {
        if (line.trim()) {
            const isFR = line.includes('FR-');
            const isNFR = line.includes('NFR-');
            
            if (isFR || isNFR) {
                const [label, ...rest] = line.split(':');
                html += `<li><span class="${isFR ? 'fr' : 'nfr'}">${label}:</span> ${rest.join(':')}</li>`;
            } else {
                html += `<li>${line}</li>`;
            }
        }
    });
    
    html += '</ul>';
    return html;
}

function formatList(listText) {
    if (!listText) return '<p>Keine Einträge vorhanden</p>';
    
    const lines = listText.split('\n').filter(line => line.trim() !== '');
    let html = '<ul class="tasks-list">';
    
    lines.forEach(line => {
        if (line.trim()) {
            html += `<li>${line}</li>`;
        }
    });
    
    html += '</ul>';
    return html;
}

// Event-Listener für das Formular
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('brainstormForm');
    
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const idea = document.getElementById('idea').value.trim();
            const context = document.getElementById('context').value.trim();
            const focus = document.getElementById('focus').value;
            const filesInput = document.getElementById('files');
            const files = filesInput.files;
            
            if (!idea) {
                alert('Bitte geben Sie eine Idee ein');
                return;
            }
            
            try {
                // In einer echten Implementierung würde hier die API
                // tatsächlich aufgerufen, aber für die Demonstration
                // verwenden wir Mock-Daten
                const mockResult = {
                    problem_statement: `Zusammenfassung der Idee: ${idea}\n\nKontext: ${context}`,
                    goals_kpis: `Ziele und KPIs für: ${idea}\n\n- Ziel 1: Beschreibung\n- Ziel 2: Beschreibung\n- KPI 1: Metrik\n- KPI 2: Metrik`,
                    functional_requirements: `FR-1 (H): Das System SOLLTE eine intuitive Benutzeroberfläche bieten\nFR-2 (M): Das System MUSS in der Lage sein, Benutzerdaten zu speichern`,
                    nonfunctional_requirements: `NFR-1 (H): Das System MUSS innerhalb von 2 Sekunden auf Benutzereingaben reagieren\nNFR-2 (M): Das System SOLLTE eine Verfügbarkeit von 99.9% bieten`,
                    risks_assumptions: `RISIKO-1: Technische Umsetzbarkeit könnte komplexer sein als ursprünglich angenommen - Gegenmaßnahme: Prototypisierung\nANNAHME-1: Benutzer haben Zugang zu Internet - Wird für die Umsetzung vorausgesetzt`,
                    implementation_potential: `Komponenten:\n- Frontend-Modul\n- Backend-Service\n- Datenbank\n\nPhasen:\n- Phase 1: Prototyp\n- Phase 2: MVP\n- Phase 3: Produktion`,
                    task_list: `T1: Technologie-Research (FR-1, FR-2)\nT2: UI/UX-Design (FR-1)\nT3: Backend-Entwicklung (FR-2)`,
                    test_ideas: `TS-1: Unit-Test (Unit) - Testet die Hauptlogik\nTS-2: Integrationstest (Integration) - Testet die API-Schnittstellen\nTS-3: E2E-Test (E2E) - Testet den kompletten Workflow`,
                    followup_prompts: {
                        prompt_planner: `Erstelle einen detaillierten Entwicklungsplan für: ${idea}. Kontext: ${context}`,
                        prompt_architect: `Entwirf die Systemarchitektur für: ${idea}. Gegeben ist folgender Kontext: ${context}`,
                        prompt_dev: `Erstelle eine Entwicklungsstrategie und erste Implementierungsschritte für: ${idea}. Kontext: ${context}`
                    }
                };
                
                // Simuliere API-Verzögerung
                await new Promise(resolve => setTimeout(resolve, 1500));
                
                // Zeige die Ergebnisse an
                displayResult(mockResult, idea);
                
                // Optional: In einer echten Implementierung würde hier die echte API aufgerufen:
                /*
                const result = await submitBrainstorm(idea, context, focus, files);
                displayResult(result, idea);
                */
            } catch (error) {
                console.error('Fehler:', error);
                // Fehlerbehandlung wird bereits in submitBrainstorm durchgeführt
            }
        });
    }
});