# Simple Makefile

# Run Python server
run-python:
	cd backend && python3 main.py

# Run NPM server
run-npm:
	cd frontend && npm run serve

# Start both Python and NPM servers
up: run-python run-npm

.PHONY: run-python run-npm up
