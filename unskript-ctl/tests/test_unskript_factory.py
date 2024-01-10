import sys
import os 
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

try:
    from unskript_ctl_factory import ChecksFactory, ScriptsFactory, NotificationFactory, ConfigParserFactory
except Exception as e: 
    print(f"ERROR: {e}")

class TestChecksFactory(unittest.TestCase):
    def test_checks_factory_run(self):
        factory1 = ChecksFactory()
        factory2 = ChecksFactory()
        # Test Singleton behavior 
        self.assertIs(factory1, factory2)
        
        factory1.run()

class TestScriptsFactory(unittest.TestCase):
    def test_scripts_factory_run(self):
        factory1 = ScriptsFactory()
        factory2 = ScriptsFactory()
        # Test Singleton behavior 
        self.assertIs(factory1, factory2)

        factory1.run()

class TestReportsFactory(unittest.TestCase):
    def test_reports_factory_run(self):
        factory1 = NotificationFactory()
        factory2 = NotificationFactory()
        # Test Singleton behavior
        self.assertIs(factory1, factory2)

        factory1.notify()

class TestConfigParserFactory(unittest.TestCase):
    def test_reports_factory_run(self):
        factory1 = ConfigParserFactory()
        factory2 = ConfigParserFactory()
        # Test Singleton behavior
        self.assertIs(factory1, factory2)

        g = factory1.get_global()
        assert isinstance(g, dict) is True
        n = factory1.get_notification()
        assert isinstance(n, dict) is True
        cp = factory1.get_checks_params()
        assert isinstance(cp, dict) is True
        c = factory1.get_checks()
        assert isinstance(c, list) is True
        j = factory1.get_jobs()
        assert isinstance(j, dict) is True
        s = factory1.get_schedule()
        assert isinstance(s, dict) is True

if __name__ == '__main__':    
    unittest.main()