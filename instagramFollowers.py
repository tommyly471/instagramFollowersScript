import json
import unittest
from unittest.mock import patch, mock_open

# Your main functions
def load_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def extract_followers_following(data):
    followers = set()
    following = set()
    
    for follower in data.get('followers', []):
        followers.add(follower['string_list_data'][0]['value'])
    
    for followee in data.get('following', []):
        following.add(followee['string_list_data'][0]['value'])
    
    return followers, following

def compare_followers_following(followers, following):
    not_following_back = following - followers
    not_followed_back = followers - following
    
    return not_following_back, not_followed_back

def main():
    # Load your data
    followers_data_path = 'path_to_your_followers.json'
    following_data_path = 'path_to_your_following.json'

    followers_data = load_data(followers_data_path)
    following_data = load_data(following_data_path)

    # Extract followers and following
    followers, following = extract_followers_following({
        'followers': followers_data,
        'following': following_data
    })

    # Compare followers and following
    not_following_back, not_followed_back = compare_followers_following(followers, following)

    # Print the results
    print("People you follow who don't follow you back:")
    for user in not_following_back:
        print(user)

    print("\nPeople who follow you but you don't follow back:")
    for user in not_followed_back:
        print(user)

# Unit tests
class TestSocialMedia(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps([
        {"string_list_data": [{"value": "user1"}]},
        {"string_list_data": [{"value": "user2"}]}
    ]))
    def test_load_data_followers(self, mock_file):
        expected_data = [
            {"string_list_data": [{"value": "user1"}]},
            {"string_list_data": [{"value": "user2"}]}
        ]
        data = load_data('path_to_your_followers.json')
        self.assertEqual(data, expected_data)
    
    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps([
        {"string_list_data": [{"value": "user3"}]},
        {"string_list_data": [{"value": "user4"}]}
    ]))
    def test_load_data_following(self, mock_file):
        expected_data = [
            {"string_list_data": [{"value": "user3"}]},
            {"string_list_data": [{"value": "user4"}]}
        ]
        data = load_data('path_to_your_following.json')
        self.assertEqual(data, expected_data)

    def test_extract_followers_following(self):
        data = {
            "followers": [{"string_list_data": [{"value": "user1"}]}, {"string_list_data": [{"value": "user2"}]}],
            "following": [{"string_list_data": [{"value": "user2"}]}, {"string_list_data": [{"value": "user3"}]}]
        }
        followers, following = extract_followers_following(data)
        self.assertEqual(followers, {"user1", "user2"})
        self.assertEqual(following, {"user2", "user3"})
    
    def test_compare_followers_following(self):
        followers = {"user1", "user2"}
        following = {"user2", "user3"}
        not_following_back, not_followed_back = compare_followers_following(followers, following)
        self.assertEqual(not_following_back, {"user3"})
        self.assertEqual(not_followed_back, {"user1"})

if __name__ == "__main__":
    main()
    unittest.main(argv=[''], verbosity=2, exit=False)
