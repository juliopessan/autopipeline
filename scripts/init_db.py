#!/usr/bin/env python
"""Initialize database with tables and sample data"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'apps', 'backend'))

from database import Base, engine, SessionLocal, init_db
from models import User, Program, Experiment, Metric
from datetime import datetime
import hashlib

def hash_password(password: str) -> str:
    """Simple password hashing (use bcrypt in production)"""
    return hashlib.sha256(password.encode()).hexdigest()

def init_database():
    """Initialize database with tables and sample data"""
    print("🗄️  Initializing database...")
    
    # Create tables
    init_db()
    print("✅ Tables created")
    
    # Create sample users
    db = SessionLocal()
    
    # Check if admin exists
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin:
        admin = User(
            username="admin",
            email="admin@company.com",
            full_name="Admin User",
            password_hash=hash_password("admin123"),
            is_active=True,
            is_admin=True
        )
        db.add(admin)
        print("✅ Created admin user")
    
    # Check if test user exists
    user = db.query(User).filter(User.username == "user").first()
    if not user:
        user = User(
            username="user",
            email="user@company.com",
            full_name="Test User",
            password_hash=hash_password("user123"),
            is_active=True,
            is_admin=False
        )
        db.add(user)
        print("✅ Created test user")
    
    # Create sample program
    program = db.query(Program).filter(Program.name == "Optimization Run 1").first()
    if not program and admin:
        program = Program(
            user_id=admin.id,
            name="Optimization Run 1",
            description="First optimization program",
            optimization_goal="maximize",
            metric_name="throughput",
            baseline_value=1.0,
            target_value=1.5,
            max_iterations=100,
            status="active"
        )
        db.add(program)
        db.flush()
        print("✅ Created sample program")
        
        # Create sample experiment
        experiment = Experiment(
            program_id=program.id,
            created_by=admin.id,
            parameters={"param1": 0.5, "param2": 0.8},
            results={"success": True, "score": 1.1},
            status="completed",
            cost=0.25,
            duration_seconds=120
        )
        db.add(experiment)
        db.flush()
        print("✅ Created sample experiment")
        
        # Create sample metrics
        metric = Metric(
            experiment_id=experiment.id,
            metric_name="throughput",
            value=1.1
        )
        db.add(metric)
        print("✅ Created sample metrics")
    
    db.commit()
    db.close()
    
    print("\n✅ Database initialization complete!")
    print("\nDefault credentials:")
    print("  Admin: admin / admin123")
    print("  User:  user / user123")
    print("\nDatabase URL: sqlite:///./autopipeline.db (local) or PostgreSQL")

if __name__ == "__main__":
    try:
        init_database()
    except Exception as e:
        print(f"\n❌ Error initializing database: {e}")
        sys.exit(1)
