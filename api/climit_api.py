import os
from datetime import datetime, timedelta, timezone

import psycopg2
import psycopg2.extras
import bcrypt
import jwt
from flask import Flask, jsonify, request
from flask_cors import CORS

DB_HOST = os.getenv("DB_HOST", "postgres")
DB_NAME = os.getenv("DB_NAME", "climitdb")
DB_USER = os.getenv("DB_USER", "climit")
DB_PASS = os.getenv("DB_PASS", "climit")

JWT_SECRET = os.getenv("JWT_SECRET", "change-me-in-prod")
JWT_ALGO = "HS256"
JWT_EXPIRES_MIN = 60

app = Flask(__name__)
CORS(app)  # tu pourras le désactiver quand tout passera via Nginx reverse proxy

app.config["JSON_SORT_KEYS"] = False


def get_db():
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
    )
    return conn


def create_token(user):
    payload = {
        "sub": user["id"],
        "email": user["email"],
        "role": user["role"],
        "client_name": user["client_name"],
        "exp": datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRES_MIN),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)


def decode_token(token):
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])


def auth_required(f):
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        parts = auth_header.split()

        if len(parts) != 2 or parts[0].lower() != "bearer":
            return jsonify({"error": "Missing or invalid Authorization header"}), 401

        token = parts[1]
        try:
            payload = decode_token(token)
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expiré"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token invalide"}), 401

        request.user = payload
        return f(*args, **kwargs)

    wrapper.__name__ = f.__name__
    return wrapper


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email et mot de passe requis"}), 400

    conn = get_db()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(
                "SELECT id, email, password_hash, role, client_name "
                "FROM users WHERE email = %s",
                (email,),
            )
            row = cur.fetchone()
    finally:
        conn.close()

    if not row:
        return jsonify({"error": "Identifiants invalides"}), 401

    if not bcrypt.checkpw(password.encode("utf-8"), row["password_hash"].encode("utf-8")):
        return jsonify({"error": "Identifiants invalides"}), 401

    user = {
        "id": row["id"],
        "email": row["email"],
        "role": row["role"],
        "client_name": row["client_name"],
    }
    token = create_token(user)

    return jsonify({"token": token, "user": user})


@app.route("/api/me", methods=["GET"])
@auth_required
def me():
    return jsonify(request.user)


@app.route("/api/measurements", methods=["GET"])
def get_measurements():
    sensor_id = request.args.get("sensor_id", type=int)
    limit = request.args.get("limit", default=100, type=int)

    if sensor_id is None:
        return jsonify({"error": "sensor_id requis"}), 400

    # NOTE: plus tard, tu pourras filtrer par client en fonction de request.user["role"]

    conn = get_db()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(
                """
                SELECT id, sensor_id, measured_at, value_celsius
                FROM measurements
                WHERE sensor_id = %s
                ORDER BY measured_at DESC
                LIMIT %s
                """,
                (sensor_id, limit),
            )
            rows = cur.fetchall()
    finally:
        conn.close()

    return jsonify(
        [
            {
                "id": r["id"],
                "sensor_id": r["sensor_id"],
                "measured_at": r["measured_at"].isoformat(),
                "value_celsius": float(r["value_celsius"]),
            }
            for r in rows
        ]
    )


@app.route("/api/admin/overview", methods=["GET"])
@auth_required
def admin_overview():
    if request.user.get("role") != "admin":
        return jsonify({"error": "Accès refusé"}), 403

    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM measurements")
            total_measurements = cur.fetchone()[0]
            cur.execute("SELECT COUNT(DISTINCT sensor_id) FROM measurements")
            total_sensors = cur.fetchone()[0]
    finally:
        conn.close()

    return jsonify(
        {
            "total_measurements": total_measurements,
            "total_sensors": total_sensors,
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
