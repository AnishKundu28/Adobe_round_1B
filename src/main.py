# src/main.py

from pathlib import Path
from intelligence_system import DocumentIntelligenceSystem

def main():
    # Define base paths within the Docker container
    base_dir = Path('/app')
    input_dir = base_dir / 'input'
    output_dir = base_dir / 'output'

    # Initialize and run the system
    system = DocumentIntelligenceSystem()
    system.analyze(input_dir, output_dir)

if __name__ == "__main__":
    main()