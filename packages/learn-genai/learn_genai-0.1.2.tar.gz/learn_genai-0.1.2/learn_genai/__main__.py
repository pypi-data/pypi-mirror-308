import sys
from pathlib import Path
import streamlit.web.cli as stcli

# Add the project root directory to sys.path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def main():
    from learn_genai.main import main as app_main
    sys.argv = ["streamlit", "run", str(Path(__file__).parent / "main.py")] + sys.argv[1:]
    sys.exit(stcli.main())

if __name__ == "__main__":
    main()
