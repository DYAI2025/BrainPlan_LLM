// app.js - Frontend-Logik für den Brainstorming Assistant

// Konfiguration: Backend-URL (kann überschrieben werden)
// Setzen Sie BACKEND_URL als Umgebungsvariable oder passen Sie die URL hier an
const BACKEND_URL = window.BACKEND_URL || 'http://localhost:5000';
const USE_MOCK_DATA = window.USE_MOCK_DATA !== undefined ? window.USE_MOCK_DATA : true;

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
        // API-Aufruf an Backend
        const apiUrl = `${BACKEND_URL}/api/brainstorm`;
        const response = await fetch(apiUrl, {
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
                <p><strong>Backend-URL:</strong> ${BACKEND_URL}</p>
                <p><em>Tipp: Starten Sie das Backend mit "python brainstorming_ui.py" im Hauptverzeichnis.</em></p>
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
    document.getElementById('problem-statement').innerHTML = formatParagraphs(result.problem_statement) || '<p>Wird generiert...</p>';
    document.getElementById('goals-kpis').innerHTML = formatParagraphs(result.goals_kpis) || '<p>Wird generiert...';
    document.getElementById('functional-requirements').innerHTML = formatRequirements(result.functional_requirements) || '<p>Wird generiert...</p>';
    document.getElementById('nonfunctional-requirements').innerHTML = formatRequirements(result.nonfunctional_requirements) || '<p>Wird generiert...</p>';
    document.getElementById('risks-assumptions').innerHTML = formatParagraphs(result.risks_assumptions) || '<p>Wird generiert...';
    document.getElementById('implementation-potential').innerHTML = formatParagraphs(result.implementation_potential) || '<p>Wird generiert...';
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
    let html = '<div class="requirements-container">';

    reqLines.forEach(line => {
        if (line.trim()) {
            const isFR = line.includes('FR-');
            const isNFR = line.includes('NFR-');

            if (isFR || isNFR) {
                const [label, ...rest] = line.split(':');
                html += `<div class="requirement-item"><span class="${isFR ? 'fr' : 'nfr'}">${label}:</span> ${rest.join(':')}</div>`;
            } else {
                html += `<div class="requirement-item">${line}</div>`;
            }
        }
    });

    html += '</div>';
    return html;
}

function formatList(listText) {
    if (!listText) return '<p>Keine Einträge vorhanden</p>';

    const lines = listText.split('\n').filter(line => line.trim() !== '');
    let html = '<div class="list-container">';

    lines.forEach(line => {
        if (line.trim()) {
            html += `<div class="list-item">${line}</div>`;
        }
    });

    html += '</div>';
    return html;
}

function formatParagraphs(text) {
    if (!text) return '';

    // Trenne den Text in Absätze anhand von \n\n oder doppelten Zeilenumbrüchen
    const paragraphs = text.split(/\n\s*\n/);

    let html = '';
    paragraphs.forEach(paragraph => {
        if (paragraph.trim()) {
            // Entferne führende Leerzeichen und Zeilenumbrüche
            paragraph = paragraph.trim();

            // Ersetze einzelne Zeilenumbrüche durch Leerzeichen (außer bei speziellen Fällen)
            let lines = paragraph.split('\n');
            let processedParagraph = '';
            for (let i = 0; i < lines.length; i++) {
                if (lines[i].trim().startsWith('- ') || lines[i].trim().startsWith('* ') ||
                    lines[i].trim().startsWith('FR-') || lines[i].trim().startsWith('NFR-') ||
                    lines[i].trim().startsWith('RISIKO-') || lines[i].trim().startsWith('ANNAHME-') ||
                    lines[i].trim().startsWith('T') || lines[i].trim().startsWith('TS-')) {
                    // Behalte Listenpunkte und spezielle Kennungen bei
                    if (processedParagraph) processedParagraph += '<br>' + lines[i];
                    else processedParagraph = lines[i];
                } else {
                    // Normale Zeilen zusammenführen
                    if (processedParagraph) processedParagraph += ' ' + lines[i];
                    else processedParagraph = lines[i];
                }
            }

            html += `<p>${processedParagraph}</p>`;
        }
    });

    return html;
}

// Funktion zum Leeren des Formulars
function clearForm() {
    document.getElementById('idea').value = '';
    document.getElementById('context').value = '';
    document.getElementById('focus').value = 'allgemein';
    document.getElementById('files').value = '';
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
                let result;

                // Verwende Mock-Daten wenn konfiguriert, ansonsten echte API
                if (USE_MOCK_DATA) {
                    console.log('Verwende Mock-Daten für Demo-Zwecke');
                    await new Promise(resolve => setTimeout(resolve, 1500)); // Simuliere API-Verzögerung
                    result = generateMockResult(idea, context);
                } else {
                    console.log('Rufe Backend-API auf:', BACKEND_URL);
                    result = await submitBrainstorm(idea, context, focus, files);
                }

                // Zeige die Ergebnisse an
                displayResult(result, idea);

            } catch (error) {
                console.error('Fehler:', error);
                // Fehlerbehandlung wird bereits in submitBrainstorm durchgeführt
            }
        });
    }

    // Event-Listener für den Clear-Button
    const clearBtn = document.getElementById('clearBtn');
    if (clearBtn) {
        clearBtn.addEventListener('click', function() {
            if (confirm('Sind Sie sicher, dass Sie das Formular leeren möchten? Alle eingegebenen Daten gehen verloren.')) {
                clearForm();
            }
        });
    }
});

// Hilfsfunktion zum Generieren von Mock-Daten für Demo-Zwecke
function generateMockResult(idea, context) {
    return {
        problem_statement: `### Situation\n${idea}\n\n### Hintergrund\n${context}\n\n### Ziel\nEntwicklung einer Lösung zur Umsetzung der beschriebenen Anforderungen`,
        goals_kpis: `## Hauptziele\n\n- Effiziente Umsetzung der Kernfunktionalitäten\n- Benutzerfreundliche Interaktion mit der Anwendung\n\n## KPIs\n\n- Benutzerakzeptanzrate > 80%\n- Antwortzeit < 2 Sekunden\n- Systemverfügbarkeit > 99.5%`,
        functional_requirements: `### Must-Have Anforderungen\n\nFR-1 (H): Das System SOLLTE eine intuitive Benutzeroberfläche bieten, um eine einfache Bedienung sicherzustellen\n\nFR-2 (H): Das System MUSS in der Lage sein, Benutzerdaten sicher zu speichern und zu verwalten\n\n### Should-Have Anforderungen\n\nFR-3 (S): Das System SOLLTE eine Suchfunktion bereitstellen\n\nFR-4 (S): Das System SOLLTE Benachrichtigungen bei wichtigen Ereignissen senden\n\n### Could-Have Anforderungen\n\nFR-5 (C): Das System KÖNNTE eine Offline-Funktionalität bieten\n\nFR-6 (C): Das System KÖNNTE eine Sprachsteuerung unterstützen`,
        nonfunctional_requirements: `### Performance-Anforderungen\n\nNFR-1 (H): Das System MUSS innerhalb von 2 Sekunden auf Benutzereingaben reagieren\n\nNFR-2 (M): Das System SOLLTE eine Last von bis zu 1000 gleichzeitigen Benutzern verarbeiten können\n\n### Sicherheitsanforderungen\n\nNFR-3 (H): Der Datenschutz MUSS gemäß DSGVO gewährleistet sein\n\nNFR-4 (M): Zugriffe AUF sensible Daten MÜSSEN authentifiziert sein\n\n### Verfügbarkeitsanforderungen\n\nNFR-5 (H): Das System SOLLTE eine Verfügbarkeit von 99.9% bieten`,
        risks_assumptions: `## Risiken\n\n- RISIKO-1: Die technische Umsetzbarkeit mancher Anforderungen könnte komplexer sein als ursprünglich eingeschätzt\n  - Gegenmaßnahme: Durchführung von Proof-of-Concept-Tests vor der Hauptentwicklung\n\n- RISIKO-2: Ein Mangel an qualifizierten Entwicklern könnte das Projekt verzögern\n  - Gegenmaßnahme: Frühzeitige Rekrutierung und Schulung von Personal\n\n## Annahmen\n\n- ANNAHME-1: Der Benutzer hat regelmäßigen Zugang zu einer Internetverbindung\n\n- ANNAHME-2: Die notwendigen externen Schnittstellen (z.B. Zahlungsdienste) sind stabil verfügbar`,
        implementation_potential: `## Architekturansatz\n\n- Modulare Architektur mit klaren Schnittstellen\n- Nutzung von Microservices für Skalierbarkeit\n\n## Technologieempfehlungen\n\n- Backend: Node.js/Express oder Python/Django\n- Frontend: React oder Vue.js\n- Datenbank: PostgreSQL oder MongoDB\n\n## Phasenplanung\n\n- Phase 1: Prototypentwicklung (2 Wochen)\n- Phase 2: MVP-Implementierung (6 Wochen)\n- Phase 3: Erweiterte Funktionen und Tests (4 Wochen)\n- Phase 4: Bereitstellung und Einführung (2 Wochen)`,
        task_list: `### Phase 1: Projektvorbereitung\n\nT1.1: Anforderungsanalyse (2 Tage)\nT1.2: Technologieentscheidung (1 Tag)\nT1.3: Projektplanung (1 Tag)\n\n### Phase 2: Architektur und Design\n\nT2.1: Systemarchitektur festlegen (2 Tage)\nT2.2: Datenbankschema entwerfen (2 Tage)\nT2.3: UI/UX-Design erstellen (3 Tage)\n\n### Phase 3: Implementierung\n\nT3.1: Backend-Basis implementieren (5 Tage)\nT3.2: Frontend-Basis implementieren (4 Tage)\nT3.3: API-Integration durchführen (3 Tage)`,
        test_ideas: `### Unit-Tests\n\nTS-1: Test der Geschäftslogik (Unit) - Stellt sicher, dass Algorithmen korrekt funktionieren\n\nTS-2: Test der Datenbankschicht (Unit) - Verifiziert korrekte Speicherung und Abruf von Daten\n\n### Integrationstests\n\nTS-3: API-Endpunkte testen (Integration) - Überprüft korrekte Kommunikation zwischen Frontend und Backend\n\nTS-4: Authentifizierung testen (Integration) - Stellt sichere Benutzerauthentifizierung sicher\n\n### E2E-Tests\n\nTS-5: Benutzerworkflow testen (E2E) - Überprüft vollständige Benutzerabläufe\n\nTS-6: Belastungstest (E2E) - Validiert Systemverhalten unter Last`,
        followup_prompts: {
            prompt_planner: `Erstelle einen detaillierten Entwicklungsplan für: ${idea}. Kontext: ${context}. Bitte strukturiere den Plan in Phasen mit klaren Meilensteinen, Zeitplänen und Ressourcenbedarf.`,
            prompt_architect: `Entwirf die Systemarchitektur für: ${idea}. Gegeben ist folgender Kontext: ${context}. Bitte berücksichtige Skalierbarkeit, Sicherheit und Wartbarkeit in der Architektur.`,
            prompt_dev: `Erstelle eine Entwicklungsstrategie und erste Implementierungsschritte für: ${idea}. Kontext: ${context}. Bitte empfehle spezifische Technologien und Frameworks sowie eine geeignete Vorgehensweise.`
        }
    };
}