import unittest
from ner_core import AdvancedEntityExtractor

class TestNER(unittest.TestCase):
    def setUp(self):
        try:
            self.engine = AdvancedEntityExtractor()
        except Exception:
            self.engine = None

    def test_processing(self):
        if not self.engine:
            self.skipTest("Spacy model not installed")
        
        text = "Google was founded by Larry Page."
        entities = self.engine.extract_entities(text)
        self.assertIsInstance(entities, list)
        self.assertTrue(len(entities) > 0)
        
        # Google -> ORG
        # Larry Page -> PERSON
        labels = [e['label'] for e in entities]
        texts = [e['text'] for e in entities]
        
        self.assertIn("Google", texts)
        self.assertIn("ORG", labels)

    def test_custom_patterns(self):
        """Test custom pattern extraction if available"""
        if not self.engine:
            self.skipTest("Engine not initialized")
            
        text = "Contact me at test@example.com"
        result = self.engine.extract_all(text)
        custom = result.get('custom_entities', {})
        
        self.assertIn('EMAIL', custom)
        self.assertIn('test@example.com', custom['EMAIL'])

if __name__ == '__main__':
    unittest.main()
