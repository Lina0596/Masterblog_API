from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


def validate_post_data(data):
    """
    Validates if title or content data is in a post request.
    Returns True if the data is in the request and False if not.
    """
    if "title" not in data or "content" not in data:
        return False
    return True


def find_post_by_id(post_id):
    """
    Checks if the given id in a get request matches
    with the id of a post in the database.
    Returns the post with the matching id or None
    if there is no matching post.
    """
    for i in range(len(POSTS)):
        if post_id == POSTS[i]["id"]:
            post_index = i
            return post_index
    return None

print(find_post_by_id(2))


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """
    Gets all posts and returns it as json.
    The sort parameter sorts the posts by title or by content.
    The direction parameter sorts the posts in ascending or descending order.
    Returns an error message if the given parameters are invalid.
    """
    sort = request.args.get("sort")
    direction = request.args.get("direction")
    if sort == "" and direction == "" or not sort and not direction:
        POSTS.sort(key=lambda post: post["id"])
        return jsonify(POSTS)
    elif sort == "title" and direction == "asc":
        POSTS.sort(key= lambda post: post["title"])
        return jsonify(POSTS)
    elif sort == "title" and direction == "desc":
        POSTS.sort(key= lambda post: post["title"], reverse=True)
        return jsonify(POSTS)
    elif sort == "content" and direction == "asc":
        POSTS.sort(key= lambda post: post["content"])
        return jsonify(POSTS)
    elif sort == "content" and direction == "desc":
        POSTS.sort(key=lambda post: post["content"], reverse=True)
        return jsonify(POSTS)
    else:
        return jsonify({"error": "Invalid data for sort or direction"}), 400


@app.route('/api/posts', methods=['GET', 'POST'])
def add_post():
    """
    Gets and validates the new data with a POST method.
    If the data is valid, generates a unique id and
    appends the data and returns it as json.
    """
    if request.method == 'POST':
        new_post = request.get_json()
        if not validate_post_data(new_post):
            return jsonify({"error": "Data in title or content is missing"}), 400
        new_id = max([post["id"] for post in POSTS]) + 1
        new_post["id"] = new_id
        POSTS.append(new_post)
        print(POSTS)
        return jsonify(new_post), 201
    else:
        return jsonify(POSTS)


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """
    Deletes the post with the given index.
    Returns an error message if the post
    with the given index was not found.
    """
    post_index = find_post_by_id(post_id)
    if post_index is None:
        return jsonify({"error": "The post with the given id was not found"}), 404
    del POSTS[post_index]
    return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 200


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """
    Updates the given data of the post
    with the given index and returns it as json
    Returns an error message if the post with
    the given index was not found.
    """
    post_index = find_post_by_id(post_id)
    post = POSTS[post_index]
    if post_index is None:
        return jsonify({"error": "The post with the given id was not found"}), 404
    new_post_data = request.get_json()
    post.update(new_post_data)
    return jsonify(post), 200


@app.route('/api/posts/search', methods=['GET'])
def search_post():
    """
    Searches posts by the given title or
    content and returns it as json.
    Returns an empty list if the given data doesn't
    match with any post.
    """
    title = request.args.get("title")
    content = request.args.get("content")
    filtered_posts = []
    if title:
        for post in POSTS:
            if title.lower() in post.get("title").lower():
                filtered_posts.append(post)
        return jsonify(filtered_posts)
    elif content:
        for post in POSTS:
            if content.lower() in post.get("content").lower():
                filtered_posts.append(post)
        return jsonify(filtered_posts)
    else:
        return jsonify(filtered_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
