# Flask Database Migration Guide

This guide explains how to manage database migrations in your Flask application using Flask-Migrate and Alembic.

## 🚀 Quick Start

### 1. Activate Virtual Environment
```bash
source .venv/bin/activate
```

### 2. Check Migration Status
```bash
flask db current
```

## 📋 Migration Commands

### 🔍 Check Status
```bash
# Show current migration revision
flask db current

# Show migration history
flask db history

# Show detailed info about current revision
flask db show

# List all available commands
flask db --help
```

### 📝 Create New Migrations
```bash
# Create a new migration after model changes
flask db migrate -m "Description of changes"

# Example:
flask db migrate -m "Add new user fields"
```

### ⬆️ Apply Migrations
```bash
# Apply all pending migrations
flask db upgrade

# Apply to specific revision
flask db upgrade <revision_id>

# Apply one migration at a time
flask db upgrade +1
```

### ⬇️ Rollback Migrations
```bash
# Rollback one migration
flask db downgrade -1

# Rollback to specific revision
flask db downgrade <revision_id>

# Rollback all migrations
flask db downgrade base
```

### 🏷️ Mark Migrations
```bash
# Mark current database as being at specific revision
flask db stamp <revision_id>

# Mark as being at the latest revision
flask db stamp head
```

## 🏗️ Migration Workflow

### 1. Make Model Changes
Edit your models in `app/models.py`:
```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    # Add new fields here
    email = db.Column(db.String(120), unique=True, nullable=False)
```

### 2. Generate Migration
```bash
flask db migrate -m "Add email field to User model"
```

### 3. Review Migration
Check the generated migration file in `migrations/versions/`

### 4. Apply Migration
```bash
flask db upgrade
```

### 5. Verify
```bash
flask db current
```

## 🔧 Common Scenarios

### Existing Database
If you have an existing database with tables:
```bash
# Mark as being at the latest migration
flask db stamp head
```

### Reset Database
To start fresh:
```bash
# Remove all tables
flask db downgrade base

# Recreate from scratch
flask db upgrade
```

### Check for Pending Migrations
```bash
# See what migrations are pending
flask db show

# Compare current vs head
flask db current
flask db heads
```

## 📁 Migration Files

### Location
- **Migrations directory**: `migrations/`
- **Migration files**: `migrations/versions/`
- **Configuration**: `migrations/alembic.ini`

### Migration File Structure
```python
"""Add email field to User model

Revision ID: abc123def456
Revises: previous_revision_id
Create Date: 2024-01-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    # Add new column
    op.add_column('user', sa.Column('email', sa.String(120), nullable=True))

def downgrade():
    # Remove column
    op.drop_column('user', 'email')
```

## 🐛 Troubleshooting

### "Table already exists" Error
```bash
# Mark migration as applied
flask db stamp head
```

### "No such table" Error
```bash
# Check if tables exist
flask db current

# Create tables if needed
flask db upgrade
```

### Migration Conflicts
```bash
# Check migration history
flask db history

# Reset if needed
flask db stamp base
flask db upgrade
```

## 📊 Current Status

Your application is currently at:
- **Revision**: `e5a2fa2da5b8`
- **Description**: `initial`
- **Status**: ✅ Up to date

## 🎯 Best Practices

1. **Always backup** your database before migrations
2. **Test migrations** in development first
3. **Use descriptive messages** when creating migrations
4. **Review generated code** before applying
5. **Keep migrations small** and focused
6. **Never edit** existing migration files

## 🚨 Production Notes

- **Never run migrations directly** on production
- **Always backup** before migrations
- **Test rollback procedures**
- **Monitor migration logs**
- **Use maintenance windows**

## 📚 Additional Resources

- [Flask-Migrate Documentation](https://flask-migrate.readthedocs.io/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

---

**Need Help?** Check the troubleshooting section or run `flask db --help` for all available commands. 