# app/submissions/routes.py
from flask import Blueprint, request, jsonify
from database import get_db_connection
from utils import token_required
import json
import logging

submissions_bp = Blueprint("submissions", __name__, url_prefix="/api/submissions")

# -------------------------
# CRUD Endpoints
# -------------------------

# Get all submissions
@submissions_bp.route("", methods=["GET"])
@token_required
def get_submissions(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM submissions WHERE user_id = %s ORDER BY id DESC", (user_id,))
    items = cur.fetchall()
    # Parse JSON fields
    for item in items:
        for field in ["bovines", "feeds"]:
            if field in item and isinstance(item[field], str):
                try:
                    item[field] = json.loads(item[field])
                except:
                    item[field] = []
    cur.close()
    conn.close()
    return jsonify(items), 200


# Get single submission
@submissions_bp.route("/<int:item_id>", methods=["GET"])
@token_required
def get_submission(user_id, item_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM submissions WHERE id = %s AND user_id = %s", (item_id, user_id))
    item = cur.fetchone()
    cur.close()
    conn.close()
    if not item:
        return jsonify({"error": "Not found"}), 404
    return jsonify(item), 200


# Create submission
@submissions_bp.route("", methods=["POST"])
@token_required
def create_submission(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO submissions (user_id) VALUES (%s) RETURNING *", (user_id,))
    new_item = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(new_item), 201


# Update submission
@submissions_bp.route("/<int:item_id>", methods=["PUT"])
@token_required
def update_submission(user_id, item_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM submissions WHERE id = %s AND user_id = %s", (item_id, user_id))
    item = cur.fetchone()
    if not item:
        cur.close()
        conn.close()
        return jsonify({"error": "Not found"}), 404
    # Placeholder update (currently only ownership)
    cur.execute("UPDATE submissions SET user_id = %s WHERE id = %s RETURNING *", (user_id, item_id))
    updated_item = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(updated_item), 200


# Delete submission
@submissions_bp.route("/<int:item_id>", methods=["DELETE"])
@token_required
def delete_submission(user_id, item_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM submissions WHERE id = %s AND user_id = %s RETURNING id", (item_id, user_id))
    deleted = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if not deleted:
        return jsonify({"error": "Not found"}), 404
    return jsonify({"message": "Deleted"}), 200


# -------------------------
# Optimization Endpoint
# -------------------------
@submissions_bp.route("/optimize", methods=["POST"])
@token_required
def optimize(user_id):
    data = request.get_json() or {}
    bovines = data.get("bovines", [])
    if not bovines:
        return jsonify({"error": "bovines must be a non-empty list"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO submissions (user_id, bovines, feeds, indoor_temp, outdoor_temp,
                water_intake, budget, protein, butterfat, somatic_cell_count)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id, created_at
        """, (
            user_id,
            json.dumps(bovines),
            json.dumps(data.get("feeds", [])),
            data.get("indoor_temp"),
            data.get("outdoor_temp"),
            data.get("water_intake"),
            data.get("budget"),
            data.get("protein"),
            data.get("butterfat"),
            data.get("somatic_cell_count")
        ))
        submission = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        # Optimization placeholder logic
        optimized = []
        for b in bovines:
            try:
                score = round(min(100, max(0, float(b.get("milk_yield", 0)) * 3 - float(b.get("age", 0)) * 0.5)))
            except Exception:
                score = 0
            optimized.append({**b, "score": score})

        return jsonify({"message": "Optimization completed", "submission_id": submission["id"], "results": optimized}), 201

    except Exception as e:
        logging.exception("Optimization failed")
        return jsonify({"error": "Optimization failed", "detail": str(e)}), 500
