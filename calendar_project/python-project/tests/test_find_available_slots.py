import unittest
import tempfile
import os
from datetime import timedelta
from io_comp import read_csv, person_availability, find_available_slots


class TestFindAvailableSlots(unittest.TestCase):
    
    def test_alice_jack_60min_meeting(self):
        """Test finding available slots for Alice and Jack with 60 minute meeting"""
        person_list = ['Alice', 'Jack']
        event_duration = timedelta(minutes=60)
        
        result = find_available_slots(person_list, event_duration)
        
        expected = [
            "Starting Time of available slots: 07:00",
            "Starting Time of available slots: 09:40 - 12:00",
            "Starting Time of available slots: 14:00 - 15:00",
            "Starting Time of available slots: 17:00 - 18:00"
        ]
        
        self.assertEqual(result, expected)
    
    def test_alice_jack_30min_meeting(self):
        """Test finding available slots for Alice and Jack with 30 minute meeting"""
        person_list = ['Alice', 'Jack']
        event_duration = timedelta(minutes=30)
        
        result = find_available_slots(person_list, event_duration)
        
        # Should have more slots available with shorter duration
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        # First slot should still start at 07:00
        self.assertIn("07:00", result[0])
    
    def test_all_three_people_60min(self):
        """Test finding available slots for Alice, Jack, and Bob with 60 minute meeting"""
        person_list = ['Alice', 'Jack', 'Bob']
        event_duration = timedelta(minutes=60)
        
        result = find_available_slots(person_list, event_duration)
        
        # With Bob included, there should be fewer available slots
        self.assertIsInstance(result, list)
        # Should have at least the early morning slot
        self.assertTrue(any("07:00" in slot for slot in result))
    
    def test_single_person_alice(self):
        """Test finding available slots for Alice only"""
        person_list = ['Alice']
        event_duration = timedelta(minutes=60)
        
        result = find_available_slots(person_list, event_duration)
        
        # Alice should have more availability than when combined with others
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
    
    def test_bob_only_60min(self):
        """Test finding available slots for Bob only with 60 minute meeting"""
        person_list = ['Bob']
        event_duration = timedelta(minutes=60)
        
        result = find_available_slots(person_list, event_duration)
        
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
    
    def test_short_duration_15min(self):
        """Test with very short meeting duration (15 minutes)"""
        person_list = ['Alice', 'Jack']
        event_duration = timedelta(minutes=15)
        
        result = find_available_slots(person_list, event_duration)
        
        # Should have many more slots with 15 minute duration
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
    
    def test_long_duration_120min(self):
        """Test with long meeting duration (120 minutes)"""
        person_list = ['Alice', 'Jack']
        event_duration = timedelta(minutes=120)
        
        result = find_available_slots(person_list, event_duration)
        
        # Should have fewer slots with 120 minute duration
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0, "Should have at least one available slot")
        # Check that 09:40 appears in at least one slot (since 09:40-12:00 is 140 min, enough for 120 min meeting)
        matching_slots = [s for s in result if "09:40" in s]
        self.assertGreater(len(matching_slots), 0, "Should have slot starting at 09:40")


if __name__ == '__main__':
    unittest.main()