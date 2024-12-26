
# Helios - minimalist web framework for Python

Helios is a lightweight Python web routing framework designed to provide a simple way to handle HTTP routing. Built on top of WSGI (Web Server Gateway Interface), it offers a clean and intuitive approach to route requests in your Python web applications.

> **Note:** Helios is a basic routing library designed primarily for learning and experimentation. It is not intended for use in production environments.

## Features

- **WSGI compatibility**: Runs on any WSGI-compatible server such as Gunicorn, uWSGI, or the built-in Python WSGI server.
- **Simple routing**: Define routes easily and map them to Python functions.
- **Dynamic URL parameters**: Extract variables from the URL path.
- **Method support**: Handle different HTTP methods (GET, POST, etc.).

## Installation

To use Helios in your project, you can install it directly via GitHub or manually by cloning the repository.

### Using Git

```bash
git clone https://github.com/subrotokumar/helios.git
cd helios
pip install .
```

Alternatively, if Helios is hosted on PyPI, you can install it via pip:

```bash
pip install helios
```

## Usage

### Basic Example

Here’s a simple example of how to set up Helios with basic routing.

```python
from helios import Helios, Request, Response

# Create an app instance
app = Helios()

# Define a route
@app.get('/')
def home(req: Request, res: Response):
    return 'Hello, World!'

@app.post('/hello/{name}')
def greet(req: Request, res: Response, name: str):
    res.send(f'Hello, {name}!')

if __name__ == '__main__':
    app.run()
```

### Running the App with a WSGI Server

Helios is designed to run on any WSGI-compatible server. For example, using Gunicorn:

1. Save your application in a file (e.g., `app.py`).
2. Run the application with Gunicorn:

```bash
gunicorn app:app
```

In the above example, `app` refers to the Helios application instance, and `app.py` is the Python file containing your app.

### Handling HTTP Methods

You can specify the HTTP methods that your routes should handle:

```python
@app.get('/hello1/{name}')
def greet1(req, res, name):
    res.send(f'Hello, {name}!')

@app.post('/hello2/{name}')
def greet2(req, res, name):
    res.send(f'Hello, {name}!')
```

## Supported HTTP Methods

Helios currently supports the following HTTP methods:

- `GET`
- `POST`
- `PUT`
- `DELETE`

You can specify the methods for each route using the `methods` argument in the route decorator.

## Limitations

- **Not production-ready**: Helios is intended for educational and learning purposes. It is not optimized for high performance or scalability.
- **Minimal functionality**: This library provides basic routing and HTTP request handling but lacks advanced features such as middleware support, templating, and database integration.
- **No built-in templating**: Helios does not include a templating engine as of right now. [**Comming Soon**]

## Contributing

Helios is open-source and welcomes contributions! If you find any bugs or want to improve the library, feel free to fork the repository and submit a pull request.

### Contribution Guidelines:

- Fork the repository.
- Create a new branch for your changes.
- Write tests for new features or bug fixes.
- Submit a pull request with a description of your changes.

## License

Helios is licensed under the MIT License. See the LICENSE file for more details.