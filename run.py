"""
Quick start script for NOVA AI Personal Assistant
"""
import os
import sys

def main():
    print("=" * 60)
    print("NOVA - AI Personal Assistant")
    print("=" * 60)
    print()
    
    # Check Python version
    if sys.version_info < (3, 11):
        print("⚠️  Warning: Python 3.11 or higher is recommended")
        print(f"   Current version: {sys.version}")
        print()
    
    # Check if .env exists
    if not os.path.exists('.env'):
        print("📝 Creating .env file from template...")
        if os.path.exists('.env.example'):
            with open('.env.example', 'r') as src, open('.env', 'w') as dst:
                dst.write(src.read())
            print("✅ .env file created")
        else:
            print("⚠️  .env.example not found")
        print()
    
    print("🚀 Starting NOVA...")
    print()
    print("📍 Server will be available at: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    print()
    print("=" * 60)
    print()
    
    # Import and run the app
    try:
        from app import app
        port = int(os.getenv('PORT', 5000))
        debug = os.getenv('FLASK_DEBUG', 'True') == 'True'
        app.run(host='0.0.0.0', port=port, debug=debug)
    except ImportError as e:
        print(f"❌ Error: {e}")
        print()
        print("Please install required packages:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    except KeyboardInterrupt:
        print()
        print("👋 Shutting down NOVA...")
        print("Goodbye!")
        sys.exit(0)

if __name__ == '__main__':
    main()
