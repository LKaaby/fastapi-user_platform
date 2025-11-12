# test_direct.py
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(__file__))

try:
    # Test the import chain
    from src.core.config import settings
    print("✅ SUCCESS: Imported settings from config")
    print(f"Settings class: {type(settings)}")
    print(f"DATABASE_URL present: {hasattr(settings, 'DATABASE_URL')}")
except ImportError as e:
    print(f"❌ IMPORT ERROR: {e}")
    print(f"Python path: {sys.path}")