from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


def validate_post_data(data):
    if "title" not in data or "content" not in data:
        return False
    return True


def find_post_by_id(post_id):
    for i in range(len(POSTS)):
        if post_id == POSTS[i]["id"]:
            post = POSTS[i]
            return post
    return None


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


@app.route('/api/posts', methods=['GET', 'POST'])
def add_post():
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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
