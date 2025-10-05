# Writer Buddy

A minimal, literary writing application inspired by timeless web aesthetics. Write, edit, and review your work in a distraction-free environment.

## Features

### Three Writing Modes

**✍️ Writing Mode**
- Disappearing text feature - older words fade as you type
- Adjustable notes pane for research and references  
- Serif typography for a literary feel
- Minimal, distraction-free interface

**✏️ Edit Mode**
- 37+ writing rules to improve your prose
- Remove weak words: very, really, just, that, etc.
- Check for passive voice, repeated words, long sentences
- Highlight -ly adverbs and vague language
- Custom rule creation

**📖 Review Mode**
- Beautiful markdown rendering
- Text-to-speech with adjustable speed
- Clean reading view

### Organization
- Tag-based organization
- Real-time search
- Chronological document list

### Export
- Markdown (.md)
- Plain text (.txt)
- PDF

## Quick Start

```bash
# Install dependencies and set up database
just install

# Run development server
just dev

# Visit http://localhost:8000
```

## Manual Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Load preset rules
python manage.py create_preset_rules
python manage.py add_writing_rules
python manage.py add_advanced_rules

# Run server
python manage.py runserver
```

## Design Philosophy

Writer Buddy embraces a minimal, literary aesthetic:
- Serif fonts (Crimson Text, EB Garamond)
- Cream background, muted colors
- No rounded corners or heavy shadows
- Generous whitespace
- Simple, understated interactions

Inspired by the personal web and sites like [simonsarris.com](https://simonsarris.com/).

## Tech Stack

- **Backend:** Django 4.2
- **Frontend:** HTMX + Alpine.js + Tailwind CSS
- **Database:** SQLite
- **Export:** WeasyPrint (PDF), Markdown
- **TTS:** Web Speech API

## Writing Rules

Writer Buddy includes 37 preset rules based on classic writing advice:

**Word Removal**
- Qualifiers: very, really, just, quite, rather, literally, actually, etc.
- Weak words: that, then, start/begin, suddenly
- Redundant: completely, totally, extremely

**Style Checks**
- Passive voice detection
- -ly adverbs
- Repeated words
- Long sentences (30+ words)
- Vague language: thing/something, interesting, nice

**Clichés**
- "in order to" → use "to"
- "there is/are" → rewrite stronger
- "it is/was" → rewrite stronger

## Justfile Commands

```bash
just install    # Install and set up project
just dev        # Run development server
just migrate    # Run database migrations
just lint       # Check Python code
just superuser  # Create admin user
just clean      # Remove cache files
just reset-db   # Reset database (careful!)
```

## Contributing

This is a personal project, but suggestions and feedback are welcome!

## License

MIT

---

*Write simply. Write clearly. Write well.*
