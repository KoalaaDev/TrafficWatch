import sqlite3

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS evidence (id INTEGER PRIMARY KEY, Date TEXT, VehicleID TEXT, ViolationType INTEGER, Vehicle TEXT, Image TEXT, speed)")
        self.conn.commit()
    
    def insert_violation(self, date, vehicle_id, violation_type, vehicle, image, speed=None):
        self.cur.execute("INSERT INTO evidence VALUES (NULL, ?, ?, ?, ?, ?, ?)", (date, vehicle_id, violation_type, vehicle, image, speed))
        self.conn.commit()

    def fetch_violations(self, date="All"):
        if date == "All":
            self.cur.execute("SELECT * FROM evidence")
        else:
            self.cur.execute("SELECT * FROM evidence WHERE Date=?", (date,))
        return self.cur.fetchall()
    
    def __del__(self):
        self.conn.close()
