# Skewer

Skewer is a basic Teradata table viewer built with Flask and Bootstrap. It provides a simple web interface to browse Teradata tables and view record details.

## Setup

### Prerequisites

- Python 3.13+
- `uv` package manager

### Installation

1. Clone the repository:

```bash
git clone https://github.com/mortie23/skewer.git
cd skewer
```

2. Install dependencies:

```bash
uv sync
```

### Configuration

Skewer requires a configuration file located in your home directory to connect to Teradata.

1. Create a file named `.skewer.toml` in your user home directory (e.g., `C:\Users\YourName\.skewer.toml` on Windows or `~/.skewer.toml` on Linux/macOS).
2. Add your Teradata credentials:

```toml
host = "your_teradata_host"
user = "your_username"
password = "your_password"
# Optional:
logmech = "TD2" 
```

**Note**: Ensure the keys match exactly as shown above (`host`, `user`, `password`).

### Running the Application

To start the development server:

```bash
uv run skewer
```

Open your browser and navigate to `http://127.0.0.1:5000`.

## Features

- **Connection Check**: Verifies database connection on the home page.
- **Table Viewer**: Browse database tables.
- **Table Sample**: View paginated sample data from tables.
- **Record Detail**: Lookup and view individual records with detail.

## Deployment

### Posit Connect

To deploy to Posit Connect using `rsconnect-python`, ensure you have the `dev` dependencies installed or add `rsconnect-python` to your environment.

Run the following command:

```sh
uv run rsconnect deploy flask -s <CONNECT_SERVER_URL> -k <API_KEY> -t "Skewer" ./ wsgi.py
```