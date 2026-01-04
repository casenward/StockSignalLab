clean:
	@echo "Cleaning Python cache files..."
	@powershell -Command "Get-ChildItem -Recurse -Directory -Filter __pycache__ | Remove-Item -Recurse -Force"
	@powershell -Command "Get-ChildItem -Recurse -File -Filter *.pyc | Remove-Item -Force"
	@echo "Clean complete."