📝 DocPlus v2.0 - AI Document Processor

DocPlus este o platformă inteligentă de procesare a documentelor care utilizează rețele neurale avansate (PaddleOCR) pentru a extrage text din PDF-uri și imagini în timp real. Interfața este optimizată pentru productivitate, oferind un workflow fluid de tip "Drag & Drop".
🚀 Funcționalități Cheie

    AI OCR Processing: Extracție precisă a textului folosind modele de Deep Learning.

    Global Drag & Drop: Încarcă documente instant de oriunde din pagină.

    Modern Workspace: Vizualizare tip listă cu statusuri în timp real și progress bar inteligent.

    Interfață Adaptivă: Suport complet pentru Dark Mode și Light Mode cu efecte de Glassmorphism.

    Arhitectură Dockerizată: Deploy rapid și consistență între mediile de dezvoltare.

🛠️ Stack Tehnologic

    Frontend: Vue 3, Vite, TypeScript, Tailwind CSS, Lucide Icons.

    Backend: FastAPI (Python), PaddleOCR, rețele neurale.

    Infrastructură: Docker, Docker Compose.

🐳 Rulare cu Docker (Metoda Recomandată)

Cea mai simplă metodă de a rula întreaga suită (Frontend + Backend + AI) este folosind Docker Compose.
1. Pre-cerințe

    Docker Desktop instalat.

    Docker Compose activat.

2. Lansarea aplicației

Din rădăcina proiectului, rulează comanda:
Bash

docker-compose up --build

3. Accesare

După finalizarea build-ului, aplicația va fi disponibilă la următoarele adrese:

    Frontend: http://localhost:5173

    Backend API: http://localhost:8000

    API Documentation: http://localhost:8000/docs (Swagger UI)

💻 Instalare Manuală (Dezvoltare)

Dacă dorești să rulezi serviciile separat pentru dezvoltare:
Frontend
Bash

cd frontend
npm install
npm run dev

Backend

Notă: Necesită Python 3.9+ și bibliotecile PaddleOCR.
Bash

cd backend
pip install -r requirements.txt
uvicorn main:app --reload

📂 Structura Proiectului
Plaintext

docplus/
├── frontend/               # Codul Vue 3 + Vite
│   ├── src/
│   │   ├── components/     # Componente UI (BackgroundGrid, etc.)
│   │   └── views/          # Dashboard.vue, Login.vue
├── backend/                # API-ul FastAPI (Python)
│   ├── app/
│   │   ├── ocr_engine.py   # Logica PaddleOCR
│   │   └── routes/         # Endpoint-uri upload/analyze
├── docker-compose.yml      # Configurația de orchestră
└── README.md               # Această documentație

⚙️ Configurare (Variabile de mediu)

Creează un fișier .env în folderul backend pentru a configura setările de securitate:
Code snippet

JWT_SECRET=cheia_ta_secreta_aici
DATABASE_URL=sqlite:///./sql_app.db
ALLOWED_ORIGINS=["http://localhost:5173"]

🔒 Securitate și Autentificare

    JWT (JSON Web Tokens): Toate cererile către API necesită un token valid obținut la Login.

    CORS: Configurat pentru a permite accesul doar de la originile securizate definite.

🤝 Contribuție

    Fă un Fork proiectului.

    Creează un Feature Branch (git checkout -b feature/AmazingFeature).

    Dă Commit modificărilor tale (git commit -m 'Add some AmazingFeature').

    Dă Push către branch (git push origin feature/AmazingFeature).

    Deschide un Pull Request.

⭐ Dacă îți place acest proiect, nu uita să-i dai un star!