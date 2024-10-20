from src.config.settings import create_app

# Main driver function
if __name__ == '__main__':
    app = create_app()
    app.run()