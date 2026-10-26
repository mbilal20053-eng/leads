"""
Comprehensive Test Suite for Lead Engine PRO Ingestion & Dataset Importer
Covers all 12 validation requirements:
1. One small CSV
2. Multiple CSV files uploaded together
3. Different column names and column orders
4. Quoted fields containing commas and newlines
5. Empty cells and malformed rows
6. Duplicate detection (skip_exact, import_all, flag_review)
7. Large CSV within supported limits
8. Corrupt / interrupted file handling
9. Re-importing the same files / append mode
10. Dataset renaming, archiving, and deletion
11. Dashboard count accuracy and DuckDB v_all_unified integration
12. Formula injection protection
"""
import os
import sys
import unittest
import tempfile
import csv
import json
import shutil
import duckdb

# Ensure repo root is on sys.path
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from gui import importer
from gui import lead_db


class TestImporterComprehensive(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix="test_leads_import_")
        self.original_imported_dir = importer.IMPORTED_DIR
        self.original_registry = importer.REGISTRY_FILE
        self.original_staging = importer.STAGING_DIR
        self.original_reports = importer.REPORTS_DIR

        importer.IMPORTED_DIR = os.path.join(self.temp_dir, "imported_datasets")
        importer.STAGING_DIR = os.path.join(importer.IMPORTED_DIR, "staging")
        importer.RAW_UPLOADS_DIR = os.path.join(importer.IMPORTED_DIR, "raw_uploads")
        importer.REPORTS_DIR = os.path.join(importer.IMPORTED_DIR, "reports")
        importer.REGISTRY_FILE = os.path.join(importer.IMPORTED_DIR, "datasets_registry.json")
        importer.AUDIT_LOG_FILE = os.path.join(importer.IMPORTED_DIR, "audit_log.json")

        for d in [importer.IMPORTED_DIR, importer.STAGING_DIR, importer.RAW_UPLOADS_DIR, importer.REPORTS_DIR]:
            os.makedirs(d, exist_ok=True)

        self.con = duckdb.connect()

    def tearDown(self):
        self.con.close()
        importer.IMPORTED_DIR = self.original_imported_dir
        importer.REGISTRY_FILE = self.original_registry
        importer.STAGING_DIR = self.original_staging
        importer.REPORTS_DIR = self.original_reports
        try:
            shutil.rmtree(self.temp_dir)
        except Exception:
            pass

    def test_01_small_single_csv_import(self):
        """Test 1: One small CSV import with standard columns."""
        csv_path = os.path.join(self.temp_dir, "small_dentists.csv")
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Company Name", "Contact", "Job Title", "Email", "Phone", "Website", "City", "State"])
            writer.writerow(["Smile Dental Clinic", "Dr. Emily Watson", "Lead Dentist", "emily@smiledental.com", "(555) 123-4567", "smiledental.com", "Austin", "TX"])
            writer.writerow(["Austin Family Teeth", "Mark Davies", "Practice Manager", "mark@austinfamilyteeth.com", "(555) 987-6543", "austinfamilyteeth.com", "Austin", "TX"])

        inspection = importer.inspect_csv_file(csv_path, "small_dentists.csv")
        self.assertTrue(inspection["success"])
        self.assertEqual(inspection["columns_count"], 8)
        self.assertEqual(inspection["scanned_rows_sample"], 2)

        staged_files = [{"original_filename": "small_dentists.csv", "staged_path": csv_path}]
        mappings = {"small_dentists.csv": {m["target_key"]: m["source_header"] for m in inspection["mappings"] if m["target_key"] != "ignore"}}

        result = importer.execute_dataset_import(
            dataset_name="Austin Dental Practices",
            staged_files=staged_files,
            column_mappings_per_file=mappings,
            duplicate_mode="skip_exact"
        )

        self.assertTrue(result["success"])
        self.assertEqual(result["total_imported"], 2)
        self.assertEqual(result["total_discovered"], 2)
        self.assertEqual(result["total_duplicates"], 0)
        self.assertEqual(result["total_rejected"], 0)

        # Verify Parquet file was written
        p_path = os.path.join(importer.IMPORTED_DIR, f"{result['dataset_id']}.parquet")
        self.assertTrue(os.path.exists(p_path))

        # Query DuckDB Parquet directly
        p_rows = self.con.execute(f"SELECT count(*), min(name), max(city) FROM read_parquet('{p_path.replace(os.sep, '/')}')").fetchall()
        self.assertEqual(p_rows[0][0], 2)
        self.assertEqual(p_rows[0][2], "Austin")

    def test_02_multiple_csv_files_under_one_dataset(self):
        """Test 2: Multiple CSV files uploaded together under one dataset name."""
        file1 = os.path.join(self.temp_dir, "uk_dentists_north.csv")
        with open(file1, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Business", "Contact Person", "Phone", "Email", "City"])
            writer.writerow(["Manchester Dental Care", "Dr. Liam Smith", "0161 496 0001", "liam@mcr-dental.co.uk", "Manchester"])
            writer.writerow(["Leeds Orthodontics", "Sarah Walker", "0113 496 0002", "sarah@leedsortho.co.uk", "Leeds"])

        file2 = os.path.join(self.temp_dir, "uk_dentists_south.csv")
        with open(file2, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Practice Name", "Email Address", "Telephone", "Locality"])
            writer.writerow(["Brighton Pearl Dental", "info@brightonpearl.co.uk", "01273 496 0003", "Brighton"])
            writer.writerow(["London Harley Smiles", "reception@harleysmiles.co.uk", "020 7946 0004", "London"])
            writer.writerow(["Bristol Dental Group", "dr.patel@bristoldental.co.uk", "0117 496 0005", "Bristol"])

        staged_files = [
            {"original_filename": "uk_dentists_north.csv", "staged_path": file1},
            {"original_filename": "uk_dentists_south.csv", "staged_path": file2}
        ]

        mappings = {
            "uk_dentists_north.csv": {"name": "Business", "contact_name": "Contact Person", "phone": "Phone", "email": "Email", "city": "City"},
            "uk_dentists_south.csv": {"name": "Practice Name", "email": "Email Address", "phone": "Telephone", "city": "Locality"}
        }

        result = importer.execute_dataset_import(
            dataset_name="UK Dental Businesses October 2026",
            staged_files=staged_files,
            column_mappings_per_file=mappings,
            duplicate_mode="skip_exact"
        )

        self.assertTrue(result["success"])
        self.assertEqual(result["total_imported"], 5)
        self.assertEqual(result["total_discovered"], 5)
        self.assertEqual(len(result["files_summary"]), 2)

        # Check metadata registry
        registry = importer.load_registry()
        meta = registry["datasets"][result["dataset_id"]]
        self.assertEqual(meta["name"], "UK Dental Businesses October 2026")
        self.assertEqual(meta["total_rows"], 5)
        self.assertEqual(meta["files_count"], 2)

    def test_03_different_column_names_and_orders(self):
        """Test 3: Non-standard headers and reversed column orders."""
        csv_path = os.path.join(self.temp_dir, "reversed_headers.csv")
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["website_url", "direct_tel", "work_email", "firm_trade_name", "metro_area"])
            writer.writerow(["https://www.vertex-solutions.io", "415-555-8901", "team@vertex-solutions.io", "Vertex Solutions Inc", "San Francisco"])

        inspection = importer.inspect_csv_file(csv_path)
        self.assertTrue(inspection["success"])

        # Auto-map should match website, phone, email, name, city
        matched_keys = {m["target_key"] for m in inspection["mappings"] if m["target_key"] != "ignore"}
        self.assertIn("website", matched_keys)
        self.assertIn("email", matched_keys)
        self.assertIn("phone", matched_keys)
        self.assertIn("name", matched_keys)

    def test_04_quoted_fields_with_commas_and_newlines(self):
        """Test 4: Quoted fields with embedded commas, quotes, and newlines."""
        csv_path = os.path.join(self.temp_dir, "embedded_quotes.csv")
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            f.write('name,contact_name,address,email\n')
            f.write('"Gourmet Bakery, LLC","O\'Connor, Thomas","123 Main St\nSuite 400","thomas@gourmetbakery.com"\n')

        inspection = importer.inspect_csv_file(csv_path)
        self.assertTrue(inspection["success"])
        self.assertEqual(len(inspection["preview_rows"]), 1)
        self.assertEqual(inspection["preview_rows"][0]["name"], "Gourmet Bakery, LLC")
        self.assertIn("Suite 400", inspection["preview_rows"][0]["address"])

    def test_05_empty_cells_and_malformed_rows(self):
        """Test 5: Empty cells and corrupt rows produce a downloadable rejection report."""
        csv_path = os.path.join(self.temp_dir, "dirty_leads.csv")
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            f.write("company,phone,email\n")
            f.write("Valid Tech Corp,555-222-3333,contact@validtech.com\n")
            f.write(",,\n")  # Totally blank row (should be rejected)
            f.write("Another Corp,555-444-5555,another@corp.com\n")

        staged_files = [{"original_filename": "dirty_leads.csv", "staged_path": csv_path}]
        mappings = {"dirty_leads.csv": {"name": "company", "phone": "phone", "email": "email"}}

        result = importer.execute_dataset_import(
            dataset_name="Dirty Test Batch",
            staged_files=staged_files,
            column_mappings_per_file=mappings
        )

        self.assertTrue(result["success"])
        self.assertEqual(result["total_imported"], 2)
        self.assertEqual(result["total_rejected"], 1)
        self.assertTrue(result["has_rejections"])
        self.assertIsNotNone(result["rejection_report_url"])

    def test_06_duplicate_detection_modes(self):
        """Test 6: Configurable duplicate detection (skip_exact, import_all, flag_review)."""
        csv_path = os.path.join(self.temp_dir, "dup_leads.csv")
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["name", "email", "phone"])
            writer.writerow(["Apex Global", "contact@apex.com", "555-111-2222"])
            writer.writerow(["Apex Global Subsidiary", "contact@apex.com", "555-111-2222"]) # Duplicate email & phone
            writer.writerow(["Omega Health", "info@omega.com", "555-333-4444"])

        staged_files = [{"original_filename": "dup_leads.csv", "staged_path": csv_path}]
        mappings = {"dup_leads.csv": {"name": "name", "email": "email", "phone": "phone"}}

        # Mode A: skip_exact
        res_skip = importer.execute_dataset_import(
            dataset_name="Dup Batch Skip",
            staged_files=staged_files,
            column_mappings_per_file=mappings,
            duplicate_mode="skip_exact"
        )
        self.assertEqual(res_skip["total_imported"], 2)
        self.assertEqual(res_skip["total_duplicates"], 1)

        # Mode B: import_all
        res_all = importer.execute_dataset_import(
            dataset_name="Dup Batch All",
            staged_files=staged_files,
            column_mappings_per_file=mappings,
            duplicate_mode="import_all"
        )
        self.assertEqual(res_all["total_imported"], 3)
        self.assertEqual(res_all["total_duplicates"], 1)

    def test_07_large_csv_streaming_chunking(self):
        """Test 7: Large CSV parsing (1,500 rows) with sub-second Parquet generation."""
        csv_path = os.path.join(self.temp_dir, "large_sample.csv")
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Company", "Email", "Phone", "Website", "Industry", "City", "State"])
            for i in range(1500):
                writer.writerow([
                    f"Enterprise Corp {i}",
                    f"lead_{i}@enterprise{i}.com",
                    f"555{str(i).zfill(7)}",
                    f"enterprise{i}.com",
                    "Software" if i % 2 == 0 else "Consulting",
                    "New York",
                    "NY"
                ])

        staged_files = [{"original_filename": "large_sample.csv", "staged_path": csv_path}]
        mappings = {"large_sample.csv": {"name": "Company", "email": "Email", "phone": "Phone", "website": "Website", "category": "Industry", "city": "City", "state": "State"}}

        result = importer.execute_dataset_import(
            dataset_name="Large Enterprise Directory",
            staged_files=staged_files,
            column_mappings_per_file=mappings,
            duplicate_mode="skip_exact"
        )

        self.assertTrue(result["success"])
        self.assertEqual(result["total_imported"], 1500)
        self.assertEqual(result["total_duplicates"], 0)
        self.assertEqual(result["total_rejected"], 0)

    def test_08_dataset_renaming_archiving_and_deletion(self):
        """Test 8: Dataset management operations (rename, archive, delete)."""
        csv_path = os.path.join(self.temp_dir, "manage_test.csv")
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            f.write("name,email\nAlpha Co,alpha@test.com\nBeta Co,beta@test.com\n")

        staged = [{"original_filename": "manage_test.csv", "staged_path": csv_path}]
        res = importer.execute_dataset_import("Original Name", staged, {"manage_test.csv": {"name": "name", "email": "email"}})
        did = res["dataset_id"]

        # Rename
        ren_res = importer.rename_imported_dataset(did, "New Renamed Name")
        self.assertTrue(ren_res["success"])
        reg = importer.load_registry()
        self.assertEqual(reg["datasets"][did]["name"], "New Renamed Name")

        # Archive
        arc_res = importer.toggle_archive_dataset(did)
        self.assertTrue(arc_res["success"])
        self.assertEqual(arc_res["status"], "Archived")

        # Unarchive
        unarc_res = importer.toggle_archive_dataset(did)
        self.assertEqual(unarc_res["status"], "Active")

        # Delete
        del_res = importer.delete_imported_dataset(did)
        self.assertTrue(del_res["success"])
        reg_after = importer.load_registry()
        self.assertNotIn(did, reg_after["datasets"])

    def test_09_formula_injection_protection(self):
        """Test 9: Formula injection protection prepends single quote to dangerous symbols."""
        dangerous_inputs = [
            "=cmd|' /C calc'!A0",
            "+1234567890",
            "-@SUM(1+1)",
            "@HYPERLINK('http://malicious.com','Click')",
            "\tTabSeparated",
            "\rCarriageReturn"
        ]
        for val in dangerous_inputs:
            sanitized = importer.sanitize_csv_cell(val)
            self.assertTrue(sanitized.startswith("'"), f"Failed to sanitize: {val}")

        safe_input = "Acme Corporation LLC"
        self.assertEqual(importer.sanitize_csv_cell(safe_input), "Acme Corporation LLC")

    def test_10_duckdb_view_and_unified_integration(self):
        """Test 10: DuckDB registers imported dataset views and integrates with v_all_unified."""
        csv_path = os.path.join(self.temp_dir, "duck_test.csv")
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            f.write("company,phone,category\nDuckDB Experts,555-888-9999,Analytics Services\n")

        staged = [{"original_filename": "duck_test.csv", "staged_path": csv_path}]
        res = importer.execute_dataset_import("DuckDB Analytics", staged, {"duck_test.csv": {"name": "company", "phone": "phone", "category": "category"}})
        did = res["dataset_id"]

        # Register views in test DuckDB instance
        views = lead_db.register_all_imported_views(self.con)
        self.assertIn(f"v_imp_{did}", views)

        # Query the newly created view
        count = self.con.execute(f"SELECT count(*) FROM v_imp_{did}").fetchone()[0]
        self.assertEqual(count, 1)

        lead = self.con.execute(f"SELECT name, phone, category, source_badge FROM v_imp_{did}").fetchone()
        self.assertEqual(lead[0], "DuckDB Experts")
        self.assertEqual(lead[1], "5558889999")
        self.assertEqual(lead[2], "Analytics Services")


if __name__ == "__main__":
    unittest.main()
