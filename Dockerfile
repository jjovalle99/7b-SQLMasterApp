FROM python:3.11.6
RUN useradd -m sqlmaster
USER sqlmaster
ENV HOME=/home/sqlmaster \
    PATH=/home/sqlmaster/.local/bin:$PATH \
    POETRY_VIRTUALENVS_IN_PROJECT=true
WORKDIR /app
COPY --chown=sqlmaster ./ ./
RUN pip install --upgrade poetry --no-cache-dir && \
    poetry install --only main --with deploy_model --no-root --no-cache --no-interaction \
    --no-ansi --no-cache
EXPOSE 7860
CMD ["poetry", "run", "streamlit", "run", "app.py", "--server.port", "7860"]