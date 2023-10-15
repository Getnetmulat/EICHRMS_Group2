"""Application entry point."""
from App import app

if __name__ == "__main__":
    app.run(host='localhost', debug='False', port=int("80"))
