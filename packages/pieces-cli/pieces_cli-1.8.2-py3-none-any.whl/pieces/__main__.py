# To be able to use 
# python -m pieces [command] [args]
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from pieces.app import main
if __name__ == '__main__':
    main()
