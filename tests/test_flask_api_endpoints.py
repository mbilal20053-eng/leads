"""
Integration test for Flask API endpoints with the Ingestion Engine and DuckDB.
"""
import os
import sys
import unittest
import io
import json

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from gui.app import app


class TestFlaskApiEndpoints(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_01_dashboard_metrics(self):
        """Verify dashboard metrics endpoint responds with success and dataset counts."""
        res = self.client.get("/api/dashboard_metrics")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "success")
        self.assertGreater(data["dataset_count"], 0)
        self.assertGreater(data["total_portfolio"], 0)

    def test_02_validate_name_api(self):
        """Verify dataset name validation endpoint."""
        res = self.client.post("/api/import/validate_name", json={"name": "UK Dentists Live Test"})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["valid"])
        self.assertIn("uk_dentists_live_test", data["slug"])

    def test_03_inspect_and_execute_import_api(self):
        """Verify full upload inspection, execution, and query lifecycle."""
        # 1. Upload CSV to inspect
        csv_content = (
            "company,phone,email,website,city,state\n"
            "Highland Dental,555-444-1212,info@highlanddental.com,highlanddental.com,Austin,TX\n"
            "Lone Star Smiles,555-444-1313,dr.smith@lonestarsmiles.com,lonestarsmiles.com,Austin,TX\n"
        ).encode("utf-8")

        data = {
            "files": (io.BytesIO(csv_content), "austin_dentists_api_test.csv")
        }
        inspect_res = self.client.post("/api/import/inspect_files", data=data, content_type="multipart/form-data")
        self.assertEqual(inspect_res.status_code, 200)
        inspect_json = inspect_res.get_json()
        self.assertEqual(inspect_json["status"], "success")
        self.assertEqual(len(inspect_json["files"]), 1)

        staged_path = inspect_json["files"][0]["staged_path"]
        orig_filename = inspect_json["files"][0]["filename"]

        # 2. Execute import
        execute_payload = {
            "dataset_name": "Austin Dentists Test Set",
            "files": [{"original_filename": orig_filename, "staged_path": staged_path}],
            "column_mappings": {
                orig_filename: {
                    "name": "company",
                    "phone": "phone",
                    "email": "email",
                    "website": "website",
                    "city": "city",
                    "state": "state"
                }
            },
            "duplicate_mode": "skip_exact"
        }

        exec_res = self.client.post("/api/import/execute", json=execute_payload)
        self.assertEqual(exec_res.status_code, 200)
        exec_json = exec_res.get_json()
        self.assertTrue(exec_json["success"])
        self.assertEqual(exec_json["total_imported"], 2)
        dataset_id = exec_json["dataset_id"]

        # 3. Verify dataset appears in /api/imported_datasets
        list_res = self.client.get("/api/imported_datasets")
        self.assertEqual(list_res.status_code, 200)
        list_json = list_res.get_json()
        self.assertTrue(any(d["id"] == dataset_id for d in list_json["datasets"]))

        # 4. Verify leads queryable via /api/leads?dataset=<dataset_id>
        leads_res = self.client.get(f"/api/leads?dataset={dataset_id}")
        self.assertEqual(leads_res.status_code, 200)
        leads_json = leads_res.get_json()
        self.assertEqual(leads_json["total"], 2)
        self.assertEqual(len(leads_json["leads"]), 2)
        self.assertIn("Highland Dental", [l["name"] for l in leads_json["leads"]])

        # 5. Clean up test dataset
        del_res = self.client.delete(f"/api/imported_datasets/{dataset_id}")
        self.assertEqual(del_res.status_code, 200)


if __name__ == "__main__":
    unittest.main()
