#!/usr/bin/env python3
from app import create_app, db
import models

app = create_app()
with app.app_context():
    db.create_all()
    print("Database tables created successfully!")