FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home --shell /bin/bash appuser

COPY --chown=appuser:appuser pyproject.toml ./
COPY --chown=appuser:appuser app/ ./app/

USER appuser
RUN python -m venv /home/appuser/venv
ENV PATH="/home/appuser/venv/bin:$PATH"
RUN /home/appuser/venv/bin/pip install --no-cache-dir --upgrade pip
RUN /home/appuser/venv/bin/pip install .

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]