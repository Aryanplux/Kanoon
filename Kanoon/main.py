import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from translator.ui import select_language

if __name__ == "__main__":
    select_language()