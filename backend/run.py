"""
SmartCook AI Backend - Main Entry Point
启动 Flask 应用
"""
import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    print("[START] SmartCook AI Backend is starting...")
    print("[INFO] API address: http://localhost:5000")
    print("[INFO] Health check: http://localhost:5000/health")
    print("[INFO] API documentation: Please check DEPLOY.md")
    print("-" * 50)

    # Use environment variables for configuration
    debug_mode = os.getenv('FLASK_DEBUG', 'False') == 'True'
    port = int(os.getenv('FLASK_PORT', 5000))

    if debug_mode:
        print("[WARNING] Debug mode is enabled")

    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug_mode
    )
