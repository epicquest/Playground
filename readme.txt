
### Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt   # for dev purposes, syntax analysis
```

### Run the application
```bash
# Set testing environment for mock service
export TESTING=1

# Start the FastAPI server
python -m app.main
# Or using uvicorn

```

### Run tests
```bash
# Unit tests
pytest tests/test_unit.py -v

# Integration tests
pytest tests/test_integration.py -v

# All tests
pytest -v

# Robot Framework tests (requires running server)
robot tests/robot_tests.robot
```

### Run Prefect flow
```bash
python -m app.flows
```

## Key Features Demonstrated

1. **FastAPI**: RESTful API with automatic OpenAPI docs
2. **Pydantic**: Data validation and serialization
3. **Asyncio/Aiohttp**: Async HTTP requests
4. **Unit Tests**: Mocking external dependencies
5. **Integration Tests**: Full API testing
6. **Robot Framework**: BDD-style acceptance tests
7. **Prefect**: Workflow orchestration (basic example)
8. **Dependency Injection**: Service layer abstraction
9. **Error Handling**: Proper exception handling
10. **Type Hints**: Full type annotation


#LINT-FORMAT

# Lint code
ruff check app/
#ruff --fix app/
pylint app/
mypy app/
# all together, serial flow
ruff app/ && pylint app/ && mypy app/

# Format code
black app/

Tool	Purpose	              Fast & Modern?	     Notes
ruff	Linting, formatting	  ✅ Super fast	         Replaces flake8, isort, more
pylint	Deep static analysis  ❌ Slower	             Very thorough, opinionated
black	Auto-formatting	      ✅	                 Works great with ruff
mypy	Static type checking  ✅	                 Use if you use type hints


https://playground-rukf.onrender.com/