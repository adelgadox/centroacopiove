import os

# Minimal env vars required by app.config.Settings before any import.
# These are never used for real operations in unit tests.
os.environ.setdefault("DATABASE_URL", "postgresql://test:test@localhost/test")
os.environ.setdefault("SECRET_KEY", "test-secret-key-for-unit-tests-only-32-chars")
os.environ.setdefault("FRONTEND_URL", "http://localhost:3000")
