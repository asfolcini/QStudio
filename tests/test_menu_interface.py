#!/usr/bin/env python3
"""
Integration test for menu interface functionality
"""

import sys
import os
import unittest
from unittest.mock import patch

# Add parent directory to path for proper imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestMenuInterface(unittest.TestCase):
    
    def test_menu_imports(self):
        """Test that menu interface can be imported"""
        try:
            import menu_interface
            print("✓ Menu interface imports successfully")
        except Exception as e:
            self.fail(f"Menu interface import failed: {e}")
    
    def test_menu_functions_exist(self):
        """Test that key menu functions exist"""
        try:
            import menu_interface
            
            # Test main menu functions
            functions = [
                'handle_data_management',
                'handle_financial_analysis', 
                'handle_visualization',
                'handle_strategy_analysis',
                'handle_utilities',
                'run_menu_interface'
            ]
            
            for func in functions:
                self.assertTrue(hasattr(menu_interface, func), f"Function {func} not found")
            
            print("✓ All main menu functions exist")
        except Exception as e:
            self.fail(f"Menu functions test failed: {e}")
    
    def test_data_management_submenu_options(self):
        """Test that Data Management submenu has expected options"""
        try:
            import menu_interface
            
            # Test that the basic structure exists
            # We can't easily test the exact menu options without running it,
            # but we can verify the structure
            self.assertTrue(hasattr(menu_interface, 'handle_data_management'))
            
            print("✓ Data Management submenu structure exists")
        except Exception as e:
            self.fail(f"Data Management submenu test failed: {e}")
    
    def test_symbol_management_functions(self):
        """Test that symbol management functions exist"""
        try:
            import menu_interface
            
            # Test symbol management functions
            functions = [
                'handle_add_symbol',
                'handle_remove_symbol'
            ]
            
            for func in functions:
                self.assertTrue(hasattr(menu_interface, func), f"Function {func} not found")
            
            print("✓ Symbol management functions exist")
        except Exception as e:
            self.fail(f"Symbol management functions test failed: {e}")
    
    def test_core_modules_import(self):
        """Test that core modules can be imported"""
        try:
            from core import Datahub
            import core.config as cfg
            print("✓ Core modules import successfully")
        except Exception as e:
            self.fail(f"Core modules import failed: {e}")

if __name__ == '__main__':
    print("Running QStudio Menu Interface Test Suite...")
    print("=" * 50)
    
    # Run all tests
    unittest.main(verbosity=2)