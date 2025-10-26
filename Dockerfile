# ---------- build stage ----------
FROM python:3.11-slim AS builder
WORKDIR /app

# Install system deps for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libpq-dev

COPY pyproject.toml poetry.lock* /app/
# If using requirements.txt, COPY requirements.txt /app/ and skip poetry steps
RUN pip install --upgrade pip
# Example using requirements.txt:
# COPY requirements.txt /app/
# RUN pip wheel --wheel-dir=/wheels -r requirements.txt

# If you have requirements.txt:
COPY requirements.txt /app/
RUN pip install --prefix=/install -r requirements.txt

# Copy project sources
COPY . /app

# ---------- final stage ----------
FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1

# Create a non-root user
RUN useradd --create-home appuser
WORKDIR /home/appuser

# Copy installed packages and app
COPY --from=builder /install /usr/local
COPY --from=builder /app /home/appuser/app
RUN chown -R appuser:appuser /home/appuser

USER appuser
WORKDIR /home/appuser/app

# Collect static, run migrations (optional at container start) — keep ENTRYPOINT CMD minimal
EXPOSE 8000

# Use an entrypoint script in production to run migrations, collectstatic, then start gunicorn
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
