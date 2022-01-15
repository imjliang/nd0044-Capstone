@echo off
set DATABASE_URL=postgresql://postgres:0613@localhost:5432/fsndcapstone
python test_app.py
echo "test local app completed!"