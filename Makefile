# Simple Makefile

# Install NPM packages
install-npm:
	cd frontend && npm install

# Run Python server
run-python:
	cd backend && python3 main.py

# Run NPM server
run-vue:
	cd frontend && npm run serve

# Start both Python and NPM servers
up: install-npm run-python run-npm

.PHONY: install-npm run-python run-npm up
