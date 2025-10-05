# Writer Buddy - Justfile

# Install dependencies
install:
    python3 -m venv venv
    . venv/bin/activate && pip install --upgrade pip
    . venv/bin/activate && pip install -r requirements.txt
    . venv/bin/activate && python manage.py migrate
    . venv/bin/activate && python manage.py create_preset_rules
    . venv/bin/activate && python manage.py add_writing_rules
    . venv/bin/activate && python manage.py add_advanced_rules
    @echo "✓ Installation complete!"

# Run development server
dev:
    . venv/bin/activate && python manage.py runserver

# Run development server with Channels (ASGI)
dev-async:
    . venv/bin/activate && daphne -b 0.0.0.0 -p 8000 config.asgi:application

# Run migrations
migrate:
    . venv/bin/activate && python manage.py makemigrations
    . venv/bin/activate && python manage.py migrate

# Lint Python code
lint:
    @echo "Checking Python code..."
    . venv/bin/activate && python -m py_compile documents/*.py rules/*.py config/*.py || true
    @echo "✓ Lint complete"

# Format code (if you add black later)
format:
    @echo "No formatter installed. Install black with: pip install black"

# Create superuser
superuser:
    . venv/bin/activate && python manage.py createsuperuser

# Clean up
clean:
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete 2>/dev/null || true
    @echo "✓ Cleaned up Python cache files"

# Reset database (CAREFUL!)
reset-db:
    rm -f db.sqlite3
    . venv/bin/activate && python manage.py migrate
    @echo "⚠️  Database reset complete"

# Show all available commands
help:
    @just --list
