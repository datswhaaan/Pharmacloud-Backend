# Pharmacloud Backend

## Quick Start

### 1. Clone Repository
```bash
git clone <repo-url>
cd pharmacloud-backend
```

### 2. Install Dependencies
```bash
poetry install
```

### 3. Setup Environment Variables
Copy `.env.example` to `.env`

```bash
cp .env.example .env
```

Windows:

```bash
copy .env.example .env
```

Then update the environment variables as needed.

### 4. Run Application
```bash
uvicorn src.app.main:app --reload
```

or

```bash
make run
```

**API Docs:** http://localhost:8000/docs

## Docker
```bash
docker build -t pharmacloud-backend .
docker run -p 8000:8000 pharmacloud-backend
```