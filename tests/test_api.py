import unittest
import json
from app import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home(self):
        """Test the home page returns HTML"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<!DOCTYPE html>', response.data)
        self.assertIn(b'Entity Recognition System', response.data)

    def test_extract_endpoint(self):
        """Test the extraction API endpoint"""
        payload = {"text": "Apple is looking at buying U.K. startup for $1 billion"}
        response = self.app.post('/api/extract', 
                                 data=json.dumps(payload),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertIn("entities", data)
        self.assertIn("total_entities", data)
        self.assertTrue(len(data['entities']) > 0)
        
        # Check structure of first entity
        entity = data['entities'][0]
        self.assertIn("text", entity)
        self.assertIn("label", entity)
        self.assertIn("start", entity)
        self.assertIn("end", entity)

    def test_extract_no_text(self):
        """Test error handling when no text provided"""
        response = self.app.post('/api/extract', 
                                 data=json.dumps({}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
