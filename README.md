# ECA SICI - Demo de monitorización IA CCTV

Demo local con frontend React y backend Python para mostrar el concepto de monitorización centralizada de instalaciones CCTV.

## Arranque rápido

```bash
cd backend && python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

En otra terminal: `npm install && npm run dev` y abrir `http://localhost:5173`.

La demo utiliza datos mock. La capa `backend/app/services/data_provider.py` está preparada para sustituirse por conectores reales.
