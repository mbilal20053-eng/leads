"""
Automated Integration Tests for New Universal Import and Column Management Flask Endpoints
"""
import os
import sys
import unittest
import json
import tempfile
import csv

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from gui.app import app
from gui import importer


class TestApiColumnEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.temp_dir = tempfile.mkdtemp(prefix="test_api_endpoints_")

        self.orig_imported_dir = importer.IMPORTED_DIR
        self.orig_registry = importer.REGISTRY_FILE
        self.orig_staging = importer.STAGING_DIR

        importer.IMPORTED_DIR = os.path.join(self.temp_dir, "imported_datasets")
        importer.STAGING_DIR = os.path.join(importer.IMPORTED_DIR, "staging")
        importer.RAW_UPLOADS_DIR = os.path.join(importer.IMPORTED_DIR, "raw_uploads")
        importer.REPORTS_DIR = os.path.join(importer.IMPORTED_DIR, "reports")
        importer.REGISTRY_FILE = os.path.join(importer.IMPORTED_DIR, "datasets_registry.json")
        importer.AUDIT_LOG_FILE = os.path.join(importer.IMPORTED_DIR, "audit_log.json")

        for d in [importer.IMPORTED_DIR, importer.STAGING_DIR, importer.RAW_UPLOADS_DIR, importer.REPORTS_DIR]:
            os.makedirs(d, exist_ok=True)

    def tearDown(self):
        importer.IMPORTED_DIR = self.orig_imported_dir
        importer.REGISTRY_FILE = self.orig_registry
        importer.STAGING_DIR = self.orig_staging

    def test_import_and_column_management_rest_api(self):
        # 1. Create a staged CSV
        staged_csv = os.path.join(importer.STAGING_DIR, "test_leads.csv")
        with open(staged_csv, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["company", "contact", "email", "phone"])
            writer.writerow(["Summit Digital", "Mark Evans", "mark@summitdigital.co.uk", "020 7946 0888"])
            writer.writerow(["Beacon Labs", "Sarah Stone", "sarah@beaconlabs.co.uk", "020 7946 0999"])

        # 2. Call /api/import/execute with custom columns
        exec_payload = {
            "dataset_name": "REST API Test Dataset",
            "files": [{"original_filename": "test_leads.csv", "staged_path": staged_csv, "format": "csv"}],
            "column_mappings": {"test_leads.csv": {"name": "company", "contact_name": "contact", "email": "email", "phone": "phone"}},
            "custom_columns": [
                {"name": "lead_status", "type": "text", "populate_mode": "same", "default_value": "New"},
                {"name": "tier_level", "type": "text", "populate_mode": "individual", "default_value": ""}
            ],
            "cell_edits": {
                "test_leads.csv": {
                    "0": {"tier_level": "Platinum"},
                    "1": {"tier_level": "Gold"}
                }
            }
        }

        res = self.app.post("/api/import/execute", json=exec_payload)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data.get("success"))
        did = data.get("dataset_id")

        # 3. GET /api/imported_datasets/<id>/columns
        res_cols = self.app.get(f"/api/imported_datasets/{did}/columns")
        self.assertEqual(res_cols.status_code, 200)
        cols_data = json.loads(res_cols.data)
        self.assertTrue(cols_data.get("success"))
        col_names = [c["name"] for c in cols_data.get("columns", [])]
        self.assertIn("lead_status", col_names)
        self.assertIn("tier_level", col_names)

        # 4. POST /api/imported_datasets/<id>/columns (Add new column)
        add_col_payload = {
            "column_name": "assigned_agent",
            "column_type": "text",
            "default_value": "Agent 007",
            "scope": "all"
        }
        res_add = self.app.post(f"/api/imported_datasets/{did}/columns", json=add_col_payload)
        self.assertEqual(res_add.status_code, 200)
        self.assertTrue(json.loads(res_add.data).get("success"))

        # 5. PATCH /api/imported_datasets/<id>/columns/<col>/rename
        res_ren = self.app.patch(f"/api/imported_datasets/{did}/columns/assigned_agent/rename", json={"new_name": "lead_owner"})
        self.assertEqual(res_ren.status_code, 200)
        self.assertTrue(json.loads(res_ren.data).get("success"))

        # 6. POST /api/imported_datasets/<id>/columns/<col>/fill
        res_fill = self.app.post(f"/api/imported_datasets/{did}/columns/lead_status/fill", json={"value": "Contacted", "only_blanks": False})
        self.assertEqual(res_fill.status_code, 200)
        self.assertTrue(json.loads(res_fill.data).get("success"))

        # 7. GET /api/imported_datasets/<id>/leads
        res_leads = self.app.get(f"/api/imported_datasets/{did}/leads?page=1&per_page=10")
        self.assertEqual(res_leads.status_code, 200)
        leads_data = json.loads(res_leads.data)
        self.assertTrue(leads_data.get("success"))
        self.assertEqual(leads_data.get("total"), 2)
        rows = leads_data.get("leads", [])
        self.assertEqual(rows[0]["lead_owner"], "Agent 007")
        self.assertEqual(rows[0]["lead_status"], "Contacted")
        self.assertEqual(rows[0]["tier_level"], "Platinum")
        self.assertEqual(rows[1]["tier_level"], "Gold")

        # 8. DELETE /api/imported_datasets/<id>/columns/<col>
        res_del = self.app.delete(f"/api/imported_datasets/{did}/columns/tier_level")
        self.assertEqual(res_del.status_code, 200)
        self.assertTrue(json.loads(res_del.data).get("success"))

        # 9. GET /api/imported_datasets/<id>/export
        res_exp = self.app.get(f"/api/imported_datasets/{did}/export")
        self.assertEqual(res_exp.status_code, 200)
        self.assertIn("lead_owner", res_exp.data.decode("utf-8"))


if __name__ == "__main__":
    unittest.main()
