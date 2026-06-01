import mysql.connector


class Database:

    def __init__(self):

        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="2005",
            database="infraguard"
        )

        self.cursor = self.conn.cursor()

    def get_next_scan_id(self):

        self.cursor.execute(
            "SELECT COALESCE(MAX(scan_id),0)+1 FROM drift_findings"
        )

        return self.cursor.fetchone()[0]

    def save_finding(self, finding, scan_id):

        query = """
        INSERT INTO drift_findings (
            resource,
            attribute_name,
            expected_value,
            actual_value,
            risk,
            drift_status,
            scan_id
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        """

        values = (
            finding["resource"],
            finding["attribute"],
            str(finding["expected"]),
            str(finding["actual"]),
            finding["risk"],
            finding["drift"],
            scan_id
        )

        self.cursor.execute(
            query,
            values
        )

        self.conn.commit()
