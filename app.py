from pathlib import Path
import runpy


# Streamlit Cloud starts from repository root, so run the prototype app in-place.
runpy.run_path(str(Path(__file__).parent / "carepredict_prototype" / "app.py"), run_name="__main__")