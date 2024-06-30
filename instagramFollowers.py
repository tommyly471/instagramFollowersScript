import json

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

if __name__ == "__main__":
    main()
