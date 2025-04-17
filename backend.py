from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # This enables cross-origin requests

# Tree data structure classes
class TreeNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1  # For AVL tree

class BinarySearchTree:
    def __init__(self):
        self.root = None
        self.inserted_keys = []
    
    def insert(self, key):
        if key in self.inserted_keys:
            return False  # Prevent duplicate keys
            
        self.root = self._insert_recursive(self.root, key)
        self.inserted_keys.append(key)
        return True
    
    def _insert_recursive(self, root, key):
        if not root:
            return TreeNode(key)
        
        if key < root.key:
            root.left = self._insert_recursive(root.left, key)
        elif key > root.key:
            root.right = self._insert_recursive(root.right, key)
        
        return root
    
    def search(self, key):
        return self._search_recursive(self.root, key)
    
    def _search_recursive(self, root, key, level=0, parent=None, path=None):
        if path is None:
            path = []
        if not root:
            return {"found": False, "key": key, "path": path}

        path.append(root.key)

        if key == root.key:
            return {
                "found": True,
                "key": key,
                "level": level,
                "parent": parent.key if parent else "None",
                "path": path
            }

        if key < root.key:
            return self._search_recursive(root.left, key, level + 1, root, path)
        return self._search_recursive(root.right, key, level + 1, root, path)
    
    def delete(self, key):
        if key not in self.inserted_keys:
            return False
            
        self.root = self._delete_recursive(self.root, key)
        if key in self.inserted_keys:
            self.inserted_keys.remove(key)
        return True
    
    def _delete_recursive(self, root, key):
        if not root:
            return None
        
        if key < root.key:
            root.left = self._delete_recursive(root.left, key)
        elif key > root.key:
            root.right = self._delete_recursive(root.right, key)
        else:
            # Node with only one child or no child
            if not root.left:
                return root.right
            elif not root.right:
                return root.left
            
            # Node with two children
            successor = self._find_min(root.right)
            root.key = successor.key
            root.right = self._delete_recursive(root.right, successor.key)
        
        return root
    
    def _find_min(self, root):
        current = root
        while current.left:
            current = current.left
        return current
    
    def to_dict(self):
        return self._to_dict_recursive(self.root)
    
    def _to_dict_recursive(self, node):
        if not node:
            return None
        
        return {
            "key": node.key,
            "left": self._to_dict_recursive(node.left),
            "right": self._to_dict_recursive(node.right)
        }

class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None
        self.inserted_keys = []

    def height(self, node):
        return node.height if node else 0

    def get_balance(self, node):
        return self.height(node.left) - self.height(node.right) if node else 0

    def right_rotate(self, y):
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        y.height = 1 + max(self.height(y.left), self.height(y.right))
        x.height = 1 + max(self.height(x.left), self.height(x.right))

        return x

    def left_rotate(self, x):
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        x.height = 1 + max(self.height(x.left), self.height(x.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))

        return y

    def insert(self, key):
        if key in self.inserted_keys:
            return False  # Prevent duplicate keys
        self.root = self._insert(self.root, key)
        self.inserted_keys.append(key)
        return True

    def _insert(self, node, key):
        if not node:
            return AVLNode(key)

        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        else:
            return node  # No duplicates

        node.height = 1 + max(self.height(node.left), self.height(node.right))

        balance = self.get_balance(node)

        # LL
        if balance > 1 and key < node.left.key:
            return self.right_rotate(node)

        # RR
        if balance < -1 and key > node.right.key:
            return self.left_rotate(node)

        # LR
        if balance > 1 and key > node.left.key:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        # RL
        if balance < -1 and key < node.right.key:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    def search(self, key):
        return self._search_recursive(self.root, key)

    def _search_recursive(self, root, key, level=0, parent=None, path=None):
        if path is None:
            path = []
        if not root:
            return {"found": False, "key": key, "path": path}

        path.append(root.key)

        if key == root.key:
            return {
                "found": True,
                "key": key,
                "level": level,
                "parent": parent.key if parent else "None",
                "path": path
            }

        if key < root.key:
            return self._search_recursive(root.left, key, level + 1, root, path)
        return self._search_recursive(root.right, key, level + 1, root, path)

        
    def delete(self, key):
        if key not in self.inserted_keys:
            return False
        self.root = self._delete(self.root, key)
        self.inserted_keys.remove(key)
        return True

    def _delete(self, node, key):
        if not node:
            return node

        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left

            temp = self._find_min(node.right)
            node.key = temp.key
            node.right = self._delete(node.right, temp.key)

        node.height = 1 + max(self.height(node.left), self.height(node.right))

        balance = self.get_balance(node)

        # LL
        if balance > 1 and self.get_balance(node.left) >= 0:
            return self.right_rotate(node)

        # RR
        if balance < -1 and self.get_balance(node.right) <= 0:
            return self.left_rotate(node)

        # LR
        if balance > 1 and self.get_balance(node.left) < 0:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        # RL
        if balance < -1 and self.get_balance(node.right) > 0:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    def _find_min(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def to_dict(self):
        return self._to_dict_recursive(self.root)

    def _to_dict_recursive(self, node):
        if not node:
            return None
        
        return {
            "key": node.key,
            "left": self._to_dict_recursive(node.left),
            "right": self._to_dict_recursive(node.right)
        }

# Global tree instance
current_tree = BinarySearchTree()
tree_type = "bst"

# Ensure tree.json file exists
def save_tree_state():
    tree_data = {
        "type": tree_type,
        "insertedKeys": current_tree.inserted_keys,
        "tree": current_tree.to_dict()
    }
    
    with open('tree.json', 'w') as f:
        json.dump(tree_data, f)

# Initialize tree.json if it doesn't exist
if not os.path.exists('tree.json'):
    save_tree_state()

# API Routes
@app.route('/tree.json')
def get_tree():
    # Serve the tree.json file directly
    return send_from_directory('.', 'tree.json')

@app.route('/initialize', methods=['POST'])
def initialize_tree():
    global current_tree, tree_type

    data = request.json
    new_type = data.get('type', 'bst').lower()

    if new_type == 'bst':
        current_tree = BinarySearchTree()
    elif new_type == 'avl':
        current_tree = AVLTree()
    else:
        return jsonify({"success": False, "error": "Invalid tree type"})

    tree_type = new_type  # ✅ update the global AFTER successful type check
    save_tree_state()     # ✅ save the correct structure and type
    return jsonify({"success": True})


@app.route('/insert', methods=['POST'])
def insert_key():
    data = request.json
    key = data.get('key')
    
    if key is None:
        return jsonify({"success": False, "error": "No key provided"})
    
    result = current_tree.insert(key)
    save_tree_state()
    
    if result:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": "Key already exists"})

@app.route('/delete', methods=['POST'])
def delete_key():
    data = request.json
    key = data.get('key')
    
    if key is None:
        return jsonify({"success": False, "error": "No key provided"})
    
    result = current_tree.delete(key)
    save_tree_state()
    
    if result:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": "Key not found"})

@app.route('/search', methods=['POST'])
def search_key():
    data = request.json
    key = data.get('key')
    
    if key is None:
        return jsonify({"success": False, "error": "No key provided"})
    
    result = current_tree.search(key)
    return jsonify(result)

from collections import deque

def inorder(node):
    return inorder(node.left) + [node.key] + inorder(node.right) if node else []

def preorder(node):
    return [node.key] + preorder(node.left) + preorder(node.right) if node else []

def postorder(node):
    return postorder(node.left) + postorder(node.right) + [node.key] if node else []

def level_order(node):
    if not node:
        return []
    queue, result = deque([node]), []
    while queue:
        current = queue.popleft()
        result.append(current.key)
        if current.left:
            queue.append(current.left)
        if current.right:
            queue.append(current.right)
    return result


@app.route('/traverse', methods=['POST'])
def traverse_tree():
    data = request.json
    traversal_type = data.get('type', 'inorder')
    
    result = []  
    if traversal_type == 'inorder':
        result = inorder(current_tree.root)
    elif traversal_type == 'preorder':
        result = preorder(current_tree.root)
    elif traversal_type == 'postorder':
        result = postorder(current_tree.root)
    elif traversal_type == 'levelorder':
        result = level_order(current_tree.root)

    return jsonify({"traversal": result})


# Serve the HTML file
@app.route('/')
def serve_ui():
    return send_from_directory('.', 'treeui.html')

if __name__ == '__main__':
    print("Server running at http://127.0.0.1:5000")
    print("Open this URL in your browser to use the Tree Visualizer")
    app.run(debug=True)