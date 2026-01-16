# app/analytics/routes.py
from flask import Blueprint, jsonify, request
from database import get_db_connection
from utils import token_required
import logging

analytics_bp = Blueprint("analytics", __name__, url_prefix="/api/analytics")

# -------------------------
# Analytics Endpoints
# -------------------------

@analytics_bp.route("/milk-yield", methods=["GET", "OPTIONS"])
@token_required
def milk_yield_distribution(user_id):
    if request.method == "OPTIONS":
        return "", 200
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                created_at::date AS day,
                SUM((bovine->>'milk_yield')::numeric) AS total_yield
            FROM submissions,
            jsonb_array_elements(COALESCE(bovines::jsonb, '[]'::jsonb)) AS bovine
            WHERE bovine ? 'milk_yield'
            AND date_part('year', created_at) = date_part('year', CURRENT_DATE)
            AND date_part('month', created_at) = date_part('month', CURRENT_DATE)
            GROUP BY day
            ORDER BY day;
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify({
            "labels": [r["day"].strftime("%Y-%m-%d") for r in rows],
            "series": [float(r["total_yield"]) for r in rows]
        })
    except Exception as e:
        logging.exception("Error in milk_yield_distribution")
        return jsonify({"labels": [], "series": [], "error": str(e)}), 500


@analytics_bp.route("/health", methods=["GET", "OPTIONS"])
@token_required
def health_distribution(user_id):
    if request.method == "OPTIONS":
        return "", 200
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT
                COALESCE(bovine->>'health', 'unknown') AS health,
                COUNT(*) AS cnt
            FROM submissions,
            jsonb_array_elements(COALESCE(bovines::jsonb, '[]'::jsonb)) AS bovine
            WHERE submissions.user_id = %s
            GROUP BY health
            ORDER BY cnt DESC;
        """, (user_id,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify({"labels": [r["health"] for r in rows], "series": [r["cnt"] for r in rows]})
    except Exception as e:
        logging.exception("Error in health_distribution")
        return jsonify({"labels": [], "series": [], "error": str(e)}), 500


@analytics_bp.route("/breed", methods=["GET", "OPTIONS"])
@token_required
def breed_distribution(user_id):
    if request.method == "OPTIONS":
        return "", 200
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT bovine->>'breed' AS breed, COUNT(*) AS cnt
            FROM submissions, jsonb_array_elements(COALESCE(bovines::jsonb, '[]'::jsonb)) AS bovine
            WHERE submissions.user_id = %s
            GROUP BY breed
            ORDER BY cnt DESC
        """, (user_id,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify({"labels": [r["breed"] for r in rows], "series": [r["cnt"] for r in rows]})
    except Exception as e:
        logging.exception("Error in breed_distribution")
        return jsonify({"labels": [], "series": [], "error": str(e)}), 500


@analytics_bp.route("/water-intake", methods=["GET", "OPTIONS"])
@token_required
def water_distribution(user_id):
    if request.method == "OPTIONS":
        return "", 200
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT
                SUM(CASE WHEN water_intake < 20 THEN 1 ELSE 0 END) AS low,
                SUM(CASE WHEN water_intake BETWEEN 20 AND 40 THEN 1 ELSE 0 END) AS medium,
                SUM(CASE WHEN water_intake > 40 THEN 1 ELSE 0 END) AS high
            FROM submissions
            WHERE user_id = %s
        """, (user_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        labels = ["Low", "Medium", "High"]
        series = [row["low"] or 0, row["medium"] or 0, row["high"] or 0] if row else [0, 0, 0]
        return jsonify({"labels": labels, "series": series})
    except Exception as e:
        logging.exception("Error in water_distribution")
        return jsonify({"labels": ["Low", "Medium", "High"], "series": [0, 0, 0], "error": str(e)}), 500
