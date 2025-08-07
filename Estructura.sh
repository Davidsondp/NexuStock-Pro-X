nexustock_pro_x/
├── .env
├── .gitignore
├── README.md
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py
│   │   │   │   ├── products.py
│   │   │   │   ├── movements.py
│   │   │   │   ├── users.py
│   │   │   │   ├── reports.py
│   │   │   │   ├── ai.py
│   │   │   │   └── currency.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── product.py
│   │   │   ├── movement.py
│   │   │   └── user.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── inventory.py
│   │   │   ├── ia.py
│   │   │   ├── currency.py
│   │   │   └── voice.py
│   │   ├── static/
│   │   │   └── locales/
│   │   │       ├── es.json
│   │   │       ├── en.json
│   │   │       ├── fr.json
│   │   │       └── ht.json
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── database.py
│   │       └── security.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── public/
│   │   ├── index.html
│   │   └── assets/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ScannerQR.js
│   │   │   ├── VoiceControl.js
│   │   │   ├── ProductPreview.svelte
│   │   │   └── DashboardCharts.js
│   │   ├── stores/
│   │   │   ├── auth.js
│   │   │   └── inventory.js
│   │   ├── utils/
│   │   │   ├── api.js
│   │   │   └── i18n.js
│   │   └── main.js
│   ├── package.json
│   └── vite.config.js
├── scripts/
│   ├── deploy.sh
│   ├── database/
│   │   └── migrations/
│   └── ai/
│       └── train_model.py
└── tests/
    ├── unit/
    ├── integration/
    └── e2e/