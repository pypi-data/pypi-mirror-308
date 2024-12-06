# flask-make

`flask-make` is a Python package that helps you quickly set up a new Flask project with a predefined directory structure. This CLI tool creates the app folder, a virtual environment, installs Flask, and generates an organized directory structure for you, including templates, static files, and configuration files.

## Features
- **Automated Project Setup**: Sets up a new Flask app with a standard directory structure.
- **Virtual Environment Creation**: Automatically creates and activates a virtual environment in the project directory.
- **Dependency Installation**: Installs Flask and generates a `requirements.txt` file with installed dependencies.
- **Structured Template**: Comes with organized folders for static files, templates, configuration, and the main app file, ready for development.

## Installation

To install `flask-make`, simply use pip:

```bash
pip install flask-make
```

## Usage

Once installed, you can create a new Flask app by running the `flask-make` command in your terminal:

```bash
flask-make <app-name>
```

Replace `<app-name>` with the desired name of your new Flask project folder.

### Example
```bash
flask-make my_flask_app
```

This will:
1. Create a folder named `my_flask_app`.
2. Set up a virtual environment within `my_flask_app/venv`.
3. Install Flask in the virtual environment.
4. Generate a `requirements.txt` file listing installed packages.
5. Create a structured directory layout:
    ```
    my_flask_app/
    ├── app.py
    ├── config.py
    ├── requirements.txt
    ├── static/
    │   ├── css/
    │   ├── js/
    │   └── img/
    ├── templates/
    │   └── index.html
    └── venv/
    ```

6. Display instructions to activate the virtual environment.

### Activating the Virtual Environment

After creating the project, activate the virtual environment:

#### On Windows
```bash
cd my_flask_app
venv\Scripts\activate
```

#### On macOS/Linux
```bash
cd my_flask_app
source venv/bin/activate
```

## License
This project is licensed under the MIT License.
