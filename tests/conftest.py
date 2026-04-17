import pytest
import os

os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["SECRET_KEY"] = "test-secret"
os.environ["GROQ_API_KEY"] = "test-key"
os.environ["MAIL_USERNAME"] = ""
os.environ["MAIL_PASSWORD"] = ""