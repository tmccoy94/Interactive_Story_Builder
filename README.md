# Interactive Story Builder

An interactive web application that generates and plays branching stories using AI. Users can select a theme, generate a story, and explore different story paths.

## Features

- Generate unique stories based on user-provided themes
- Interactive story navigation with choices and multiple endings
- FastAPI backend with SQLite database
- React frontend with modern UI
- API proxying for local development
- Easy deployment and environment configuration

## Technologies Used

- **Frontend:** React, Vite, Axios, React Router
- **Backend:** FastAPI, SQLAlchemy, Pydantic
- **Database:** SQLite (development), configurable for production
- **AI Integration:** OpenAI API (or similar LLM)

## Getting Started

### Prerequisites

- Node.js (v18+ recommended)
- Python (3.12+ recommended)
- [pip](https://pip.pypa.io/en/stable/installation/)
- [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html) (optional, but recommended)

### Installation

#### 1. Clone the repository

```sh
git clone https://github.com/yourusername/interactive-story-builder.git
cd interactive-story-builder
```

#### 2. Set up the backend (you could also use uv)

```sh
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

- Edit `.env` to set your `DATABASE_URL`, `OPEN_API_KEY`, and allowed origins.

#### 3. Set up the frontend

```sh
cd ../frontend
npm install
```

- Edit `.env` to set `VITE_DEBUG=true` for local development.

### Running Locally

#### 1. Start the backend

```sh
cd backend
uvicorn main:app --reload
```

#### 2. Start the frontend

```sh
cd frontend
npm run dev
```

- Visit [http://localhost:5173](http://localhost:5173) in your browser.

### Deployment

- Configure your backend for production (e.g., use PostgreSQL, set `DEBUG=False`).
- Build the frontend for production:
  ```sh
  npm run build
  ```
- Serve the frontend build with your preferred static file server.
- Use a process manager (e.g., Gunicorn, Uvicorn with workers) for the backend.

## Environment Variables

**Backend (.env):**
```
DATABASE_URL=sqlite:///./database.db
API_PREFIX=/api
DEBUG=True
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
OPEN_API_KEY=your-openai-key
```

**Frontend (.env):**
```
VITE_DEBUG=true
```

## API Endpoints

- `POST /api/stories/create` — Create a new story job (provide theme)
- `GET /api/stories/{id}/complete` — Get the complete story tree

## Folder Structure

```
interactive-story-builder/
├── backend/
│   ├── main.py
│   ├── routers/
│   ├── models/
│   ├── schemas/
│   ├── core/
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── App.jsx
│   │   └── index.jsx
│   ├── public/
│   └── .env
└── README.md
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a pull request

## License

This project is licensed under the MIT License.

## Acknowledgements

- [OpenAI](https://openai.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://react.dev/)
- [Vite](https://vitejs.dev/)

---

**For questions or support, open an issue or contact the maintainer.**
