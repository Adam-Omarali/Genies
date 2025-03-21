# -------- Stage 1: Build Frontend --------
FROM node:20-alpine AS frontend-builder


WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build  # this outputs to /app/frontend/out

# -------- Stage 2: Build Backend --------
FROM python:3.11-slim

# Install Python dependencies
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY backend/ ./backend/

# Copy built frontend from previous stage
COPY --from=frontend-builder /app/frontend/out ./frontend/out

# Serve the frontend via FastAPI
# backend/main.py should mount StaticFiles from ./frontend/out

EXPOSE 8000
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
