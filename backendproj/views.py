from flask import Flask, request, jsonify
import uuid
from datetime import datetime

app = Flask(__name__)

# Приблизна структура даних
users = {}
categories = {}
records = {}
record_id_counter = 1


# Ендпоінти для користувачів
@app.route('/user/<user_id>', methods=['GET', 'DELETE'])
def get_user(user_id):
    user = users.get(user_id)
    if user:
        return jsonify(user), 200
    else:
        return jsonify({"message": "User not found"}), 404


@app.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = users.get(user_id)
    if user:
        del users[user_id]
        return jsonify(user), 200
    else:
        return jsonify({"message": "User not found"}), 404


@app.route('/user', methods=['POST'])
def create_user():
    try:
        data = request.json
        user_id = str(uuid.uuid4())
        user = {"id": user_id, "name": data.get("name")}
        users[user_id] = user
        return jsonify(user), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(list(users.values()))


# Ендпоінти для категорій
@app.route('/category/<category_id>', methods=['GET', 'DELETE'])
def get_category(category_id):
    category = categories.get(category_id)
    if category:
        return jsonify(category), 200
    else:
        return jsonify({"message": "Category not found"}), 404


@app.route('/category/<category_id>', methods=['DELETE'])
def delete_category(category_id):
    category = categories.get(category_id)
    if category:
        del categories[category_id]
        return jsonify(category), 200
    else:
        return jsonify({"message": "Category not found"}), 404


@app.route('/category', methods=['POST'])
def create_category():
    try:
        data = request.json
        category_id = str(uuid.uuid4())
        category = {"id": category_id, "name": data.get("name")}
        categories[category_id] = category
        return jsonify(category), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/categories', methods=['GET'])
def get_categories():
    return jsonify(list(categories.values()))


# Ендпоінти для записів
@app.route('/record/<record_id>', methods=['GET', 'DELETE'])
def get_record(record_id):
    record = records.get(record_id)
    if record:
        return jsonify(record), 200
    else:
        return jsonify({"message": "Record not found"}), 404


@app.route('/record/<record_id>', methods=['DELETE'])
def delete_record(record_id):
    record = records.get(record_id)
    if record:
        del records[record_id]
        return jsonify(record), 200
    else:
        return jsonify({"message": "Record not found"}), 404


@app.route('/record', methods=['POST'])
def create_record():
    global record_id_counter
    try:
        data = request.json
        user_id = data.get("user_id")
        category_id = data.get("category_id")
        date_time = data.get("date_time")
        amount = data.get("amount")

        if not (user_id and category_id and date_time and amount):
            return jsonify({"message": "Invalid data"}), 400

        record_id = record_id_counter
        record_id_counter += 1

        record = {
            "id": record_id,
            "user_id": user_id,
            "category_id": category_id,
            "date_time": date_time,
            "amount": amount
        }

        records[record_id] = record
        return jsonify(record), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/records', methods=['GET'])
def get_records():
    user_id = request.args.get('user_id')
    category_id = request.args.get('category_id')

    if user_id and category_id:
        filtered_records = {k: v for k, v in records.items() if v['user_id'] == user_id and v['category_id'] == category_id}
    elif user_id:
        filtered_records = {k: v for k, v in records.items() if v['user_id'] == user_id}
    elif category_id:
        filtered_records = {k: v for k, v in records.items() if v['category_id'] == category_id}
    else:
        return jsonify({"message": "Invalid parameters"}), 400

    return jsonify(filtered_records)


if __name__ == '__main__':
    app.run(debug=True)
