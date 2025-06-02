# app/routes/symptom_routes.py
from flask import Blueprint, request, jsonify
from app.models.symptom_log_model import SymptomLog
from app.db import SessionLocal
from datetime import datetime
from sqlalchemy import text
from sqlalchemy import func
from flask import jsonify


symptom_bp = Blueprint("symptom", __name__)

# 新增一筆症狀紀錄
@symptom_bp.route("/symptoms", methods=["POST"])
def add_symptom():
    data = request.get_json()
    name = data.get("name")
    date_str = data.get("date")

    if not name or not date_str:
        return jsonify({"error": "缺少症狀名稱或日期"}), 400

    try:
        print("接收到資料：", name, date_str)
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        db = SessionLocal()
        print("SymptomLog =", SymptomLog)
        print("type(SymptomLog) =", type(SymptomLog))
        new_log = SymptomLog(Name=name, CreateDate=date_obj)
        db.add(new_log)
        db.commit()
        db.refresh(new_log)
        db.close()
        return jsonify({"message": f"已記錄：{name} @ {date_str}"}), 201
    except Exception as e:
        print("錯誤：", str(e))
        return jsonify({"error": str(e)}), 500

# 測試資料庫連線
@symptom_bp.route("/db-test", methods=["GET"])
def db_test():
    try:
        db = SessionLocal()
        result = db.execute(text("SELECT 1")).fetchone()
        db.close()
        return jsonify({"message": "資料庫連線成功", "result": result[0]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 查詢某年月症狀點擊統計
@symptom_bp.route("/symptoms/stats", methods=["GET"])
def get_symptom_stats():
    year = request.args.get("year")
    month = request.args.get("month")

    if not year or not month:
        return jsonify({"error": "year 和 month 為必填參數"}), 400

    try:
        db = SessionLocal()
        query = text("""
            SELECT 
                DATE(create_date) as date, 
                COUNT(*) as count
            FROM symptom_log
            WHERE YEAR(create_date) = :year AND MONTH(create_date) = :month
            GROUP BY DATE(create_date)
            ORDER BY DATE(create_date)
        """)
        results = db.execute(query, {"year": int(year), "month": int(month)}).fetchall()
        db.close()

        data = [{"date": str(row[0]), "count": row[1]} for row in results]
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@symptom_bp.route("/symptoms/summary", methods=["GET"])
def symptom_summary():
    db = SessionLocal()
    try:
        # 統計每種症狀的次數
        results = db.query(SymptomLog.Name, func.count(SymptomLog.ID)).group_by(SymptomLog.Name).all()
        summary = [{"name": name, "count": count} for name, count in results]
        return jsonify(summary)
    finally:
        db.close()
