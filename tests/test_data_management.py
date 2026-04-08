#!/usr/bin/env python3
"""
Comprehensive test suite for QStudio Data Management functionality
Tests the first part of data management (excluding purge)
"""

import sys
import os
import unittest
from unittest.mock import patch, mock_open

# Add parent directory to path for proper imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestDataManagement(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_symbol = "AAPL"
        self.test_symbols_file = "config/symbols"
        
    def test_imports_work(self):
        """Test that all required modules can be imported"""
        try:
            from core.Datahub import Datahub
            import core.config as cfg
            import menu_interface
            print("✓ All imports successful")
        except Exception as e:
            self.fail(f"Import failed: {e}")
    
    def test_datahub_initialization(self):
        """Test Datahub initialization"""
        try:
            from core.Datahub import Datahub
            dh = Datahub(loadfromconfig=False)
            self.assertIsInstance(dh, Datahub)
            print("✓ Datahub initialization successful")
        except Exception as e:
            self.fail(f"Datahub initialization failed: {e}")
    
    def test_symbol_management_functions_exist(self):
        """Test that symbol management functions exist in menu_interface"""
        try:
            import menu_interface
            functions = ['handle_add_symbol', 'handle_remove_symbol']
            for func in functions:
                self.assertTrue(hasattr(menu_interface, func), f"Function {func} not found")
            print("✓ Symbol management functions exist")
        except Exception as e:
            self.fail(f"Symbol management functions test failed: {e}")
    
    def test_menu_interface_structure(self):
        """Test that menu interface has expected structure"""
        try:
            import menu_interface
            # Test that main menu functions exist
            main_functions = ['handle_data_management', 'handle_financial_analysis']
            for func in main_functions:
                self.assertTrue(hasattr(menu_interface, func), f"Function {func} not found")
            print("✓ Menu interface structure correct")
        except Exception as e:
            self.fail(f"Menu interface structure test failed: {e}")
    
    def test_configuration_access(self):
        """Test that configuration can be accessed"""
        try:
            import core.config as cfg
            self.assertIsNotNone(cfg.DATA_REPOSITORY)
            self.assertIsNotNone(cfg.SYMBOLS_FILEPATH)
            print("✓ Configuration access successful")
        except Exception as e:
            self.fail(f"Configuration access failed: {e}")
    
    def test_datahub_symbol_operations(self):
        """Test basic Datahub symbol operations"""
        try:
            from core.Datahub import Datahub
            dh = Datahub(loadfromconfig=False)
            
            # Test setting symbols
            dh.set_symbols(self.test_symbol)
            symbols = dh.get_symbols()
            self.assertIn(self.test_symbol, symbols)
            
            # Test adding symbol
            dh.add_symbol("GOOGL")
            symbols = dh.get_symbols()
            self.assertIn("GOOGL", symbols)
            
            print("✓ Datahub symbol operations successful")
        except Exception as e:
            self.fail(f"Datahub symbol operations failed: {e}")

    def test_datahub_methods_exist(self):
        """Test that essential Datahub methods exist"""
        try:
            from core.Datahub import Datahub
            dh = Datahub(loadfromconfig=False)
            
            methods = ['get_symbols', 'set_symbols', 'add_symbol', 'load_data', 'download_data', 'update_data']
            for method in methods:
                self.assertTrue(hasattr(dh, method), f"Method {method} not found")
            
            print("✓ Datahub methods exist")
        except Exception as e:
            self.fail(f"Datahub methods test failed: {e}")

if __name__ == '__main__':
    print("Running QStudio Data Management Test Suite...")
    print("=" * 50)
    
    # Run all tests
    unittest.main(verbosity=2)