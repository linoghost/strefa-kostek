#!/usr/bin/env python
"""
Script do uruchomienia testów Selenium dla PrestaShopa
Użycie: python run_tests.py
"""

import subprocess
import sys
import os

def run_tests():
    """Uruchom testy"""
    print("\n" + "="*60)
    print("SELENIUM TESTS - PrestaShop")
    print("="*60 + "\n")
    
    test_dir = os.path.join(os.path.dirname(__file__), "selenium")
    
    # Uruchom wszystkie testy
    cmd = [
        sys.executable, "-m", "pytest",
        test_dir,
        "-v",
        "-s",
        "--tb=short"
    ]
    
    print(f"Uruchamianie: {' '.join(cmd)}\n")
    
    result = subprocess.run(cmd)
    
    return result.returncode

if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)
