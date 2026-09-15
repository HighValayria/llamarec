@echo off
set "PY=C:\Users\33967\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
"%PY%" "%~dp0sync.py" status %*
