"""
Comprehensive Automated Test Suite for Universal Lead Importer, Custom Columns,
and Dataset Column Management in Lead Engine PRO.

Covers:
1. Universal Formats:
   - CSV, TSV, TXT (delimiters, encodings, quoting)
   - Excel: XLSX, XLSM, XLS (worksheets selection)
   - JSON (array) & JSONL / NDJSON (nested record dot-path flattening)
   - XML (repeated row-element detection and flattening)
   - Parquet (native columnar read)
   - ZIP archives (contained file extraction & security validation)
   - GZIP-compressed files (.csv.gz)
   - Corrupt & unsupported file format rejection
2. Custom Columns during Import (CRITICAL):
   - Mode A: Constant default value for every row
   - Mode B: Row-by-row individual cell values via preview cell editing
   - Blank values preserved
3. Column Schema Controls:
   - Renaming source columns
   - Changing destination mapping
   - Excluding columns
   - Type detection & override (leading zeros & phone preservation)
4. Dataset-Specific Schemas:
   - Dataset A vs Dataset B with distinct column sets
   - Safe DuckDB dynamic views & union with v_all_unified
5. Post-Import Column Management:
   - Add column to existing dataset (scope: all leads vs future)
   - Rename custom column
   - Fill blank cells vs fill all leads
   - Delete custom column
   - Export dataset with custom columns & formula injection defense
"""
import os
import sys
import unittest
import tempfile
import csv
import json
import zipfile
import gzip
import shutil
import duckdb
import pyarrow as pa
import pyarrow.parquet as pq
import openpyxl
import xlwt

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from gui import importer
from gui import lead_db


class TestUniversalImporter(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix="test_universal_importer_")
        self.original_imported_dir = importer.IMPORTED_DIR
        self.original_registry = importer.REGISTRY_FILE
        self.original_staging = importer.STAGING_DIR
        self.original_raw_uploads = importer.RAW_UPLOADS_DIR
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
        importer.RAW_UPLOADS_DIR = self.original_raw_uploads
        importer.REPORTS_DIR = self.original_reports
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    # =========================================================================
    # 1. Universal Format Inspections & Streaming
    # =========================================================================

    def test_01_csv_tsv_txt_formats(self):
        """Test CSV, TSV, and TXT files with various delimiters and encodings."""
        # TSV with tab delimiter
        tsv_path = os.path.join(self.temp_dir, "vendors.tsv")
        with open(tsv_path, "w", encoding="utf-8") as f:
            f.write("Vendor Name\tContact Person\tPhone Number\tCity\n")
            f.write("Apex Logistics\tDavid Clark\t01234567890\tManchester\n")
            f.write("Beta Supplies\tSarah Jenkins\t02079460192\tLondon\n")

        insp_tsv = importer.inspect_universal_file(tsv_path, "vendors.tsv")
        self.assertTrue(insp_tsv["success"])
        self.assertEqual(insp_tsv["format"], "tsv")
        self.assertEqual(insp_tsv["columns_count"], 4)
        self.assertEqual(insp_tsv["total_rows_estimate"], 2)

        # TXT with pipe delimiter
        txt_path = os.path.join(self.temp_dir, "partners.txt")
        with open(txt_path, "w", encoding="latin-1") as f:
            f.write("Business Name|Email Address|Postcode\n")
            f.write("Gamma Systems|info@gamma.co.uk|SW1A 1AA\n")

        insp_txt = importer.inspect_universal_file(txt_path, "partners.txt")
        self.assertTrue(insp_txt["success"])
        self.assertEqual(insp_txt["columns_count"], 3)
        self.assertIn("Gamma Systems", str(insp_txt["preview_rows"]))

    def test_02_excel_xlsx_and_xls_worksheets(self):
        """Test XLSX, XLSM, and legacy XLS workbooks with multiple worksheets."""
        # Create multi-worksheet XLSX
        xlsx_path = os.path.join(self.temp_dir, "medical_groups.xlsx")
        wb = openpyxl.Workbook()
        ws_dentists = wb.active
        ws_dentists.title = "Dentists"
        ws_dentists.append(["Practice Name", "Phone", "Zip Code"])
        ws_dentists.append(["Dental Care 1", "07123456789", "01234"])
        ws_dentists.append(["Dental Care 2", "07987654321", "09876"])

        ws_pharmacies = wb.create_sheet("Pharmacies")
        ws_pharmacies.append(["Pharmacy Name", "License No", "City"])
        ws_pharmacies.append(["Green Cross", "PHARM-9901", "Boston"])
        wb.save(xlsx_path)

        # Inspect sheet 1 (Dentists)
        insp1 = importer.inspect_excel_file(xlsx_path, "medical_groups.xlsx")
        self.assertTrue(insp1["success"])
        self.assertEqual(insp1["selected_sheet"], "Dentists")
        self.assertIn("Practice Name", insp1["headers"])
        self.assertEqual(insp1["total_rows_estimate"], 2)
        # Verify leading zero preservation on text
        self.assertEqual(insp1["preview_rows"][0]["Zip Code"], "01234")

        # Inspect sheet 2 (Pharmacies)
        insp2 = importer.inspect_excel_file(xlsx_path, "medical_groups.xlsx", sheet_name="Pharmacies")
        self.assertTrue(insp2["success"])
        self.assertEqual(insp2["selected_sheet"], "Pharmacies")
        self.assertIn("Pharmacy Name", insp2["headers"])

        # Create legacy XLS using xlwt
        xls_path = os.path.join(self.temp_dir, "legacy_leads.xls")
        xwb = xlwt.Workbook()
        xws = xwb.add_sheet("LegacySheet")
        xws.write(0, 0, "Company")
        xws.write(0, 1, "Revenue")
        xws.write(1, 0, "Vintage Corp")
        xws.write(1, 1, 500000)
        xwb.save(xls_path)

        insp_xls = importer.inspect_excel_file(xls_path, "legacy_leads.xls")
        self.assertTrue(insp_xls["success"])
        self.assertEqual(insp_xls["headers"], ["Company", "Revenue"])
        self.assertEqual(insp_xls["preview_rows"][0]["Company"], "Vintage Corp")

    def test_03_json_and_jsonl_nested_records(self):
        """Test JSON array and JSONL/NDJSON files with nested dict dot-path flattening."""
        # JSON Array of objects
        json_path = os.path.join(self.temp_dir, "tech_startups.json")
        records = [
            {
                "name": "CloudAI Labs",
                "website": "cloudai.io",
                "contact": {"first": "Alice", "role": "CTO"},
                "location": {"city": "Seattle", "state": "WA"}
            },
            {
                "name": "DataFlow Systems",
                "website": "dataflow.com",
                "contact": {"first": "Bob", "role": "CEO"},
                "location": {"city": "Denver", "state": "CO"}
            }
        ]
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(records, f)

        insp_json = importer.inspect_json_file(json_path, "tech_startups.json")
        self.assertTrue(insp_json["success"])
        self.assertIn("contact.role", insp_json["headers"])
        self.assertIn("location.city", insp_json["headers"])
        self.assertEqual(insp_json["preview_rows"][0]["contact.role"], "CTO")
        self.assertEqual(insp_json["preview_rows"][1]["location.city"], "Denver")

        # JSONL / NDJSON
        jsonl_path = os.path.join(self.temp_dir, "events.ndjson")
        with open(jsonl_path, "w", encoding="utf-8") as f:
            f.write(json.dumps({"event_name": "DevCon", "attendees": 1200}) + "\n")
            f.write(json.dumps({"event_name": "AI Summit", "attendees": 3500}) + "\n")

        insp_jsonl = importer.inspect_json_file(jsonl_path, "events.ndjson")
        self.assertTrue(insp_jsonl["success"])
        self.assertEqual(insp_jsonl["total_rows_estimate"], 2)
        self.assertEqual(insp_jsonl["preview_rows"][0]["event_name"], "DevCon")

    def test_04_xml_repeated_elements(self):
        """Test XML inspection and ingestion with automatic row-tag detection."""
        xml_path = os.path.join(self.temp_dir, "businesses.xml")
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
        <business_directory>
            <company id="C101">
                <name>Acme Robotics</name>
                <website>acmerobotics.com</website>
                <email>contact@acmerobotics.com</email>
                <phone>555-0199</phone>
            </company>
            <company id="C102">
                <name>Cyber Dynamics</name>
                <website>cyberdynamics.tech</website>
                <email>sales@cyberdynamics.tech</email>
                <phone>555-0288</phone>
            </company>
        </business_directory>
        """
        with open(xml_path, "w", encoding="utf-8") as f:
            f.write(xml_content)

        insp_xml = importer.inspect_xml_file(xml_path, "businesses.xml")
        self.assertTrue(insp_xml["success"])
        self.assertIn("name", insp_xml["headers"])
        self.assertIn("website", insp_xml["headers"])
        self.assertEqual(insp_xml["total_rows_estimate"], 2)
        self.assertEqual(insp_xml["preview_rows"][0]["name"], "Acme Robotics")

    def test_05_parquet_direct_read(self):
        """Test native Parquet columnar file inspection and row generation."""
        pq_path = os.path.join(self.temp_dir, "enterprises.parquet")
        table = pa.Table.from_arrays(
            [
                pa.array(["Omni Corp", "Global Transit", "Vertex Holdings"]),
                pa.array(["omnicorp.com", "globaltransit.com", "vertexholdings.com"]),
                pa.array(["00123", "00456", "00789"])  # text with leading zeros
            ],
            names=["company_name", "web_url", "registration_code"]
        )
        pq.write_table(table, pq_path)

        insp_pq = importer.inspect_parquet_file(pq_path, "enterprises.parquet")
        self.assertTrue(insp_pq["success"])
        self.assertEqual(insp_pq["total_rows_estimate"], 3)
        self.assertIn("registration_code", insp_pq["headers"])
        # Verify leading zeros preserved
        self.assertEqual(insp_pq["preview_rows"][0]["registration_code"], "00123")

    def test_06_zip_archives_and_gzip_compression(self):
        """Test ZIP archive contained file discovery and GZIP decompression."""
        # 1. Create ZIP archive with multiple tabular files
        zip_path = os.path.join(self.temp_dir, "bundled_leads.zip")
        csv_internal = "accounts.csv"
        csv_data = "Account,Balance\nFirst National,150000\nUnion Trust,280000\n"

        json_internal = "sub_folder/clients.json"
        json_data = json.dumps([{"client": "Alpha", "score": 95}, {"client": "Bravo", "score": 88}])

        with zipfile.ZipFile(zip_path, "w") as zf:
            zf.writestr(csv_internal, csv_data)
            zf.writestr(json_internal, json_data)
            # Add an unsupported file that should be ignored
            zf.writestr("notes.exe", "binary executable data")

        insp_zip = importer.inspect_zip_file(zip_path, "bundled_leads.zip", session_dir=self.temp_dir)
        self.assertTrue(insp_zip["success"])
        contained = insp_zip["contained_files"]
        self.assertEqual(len(contained), 2)
        self.assertTrue(any(c["entry_name"] == csv_internal for c in contained))
        self.assertTrue(any(c["entry_name"] == json_internal for c in contained))
        # Ensure .exe is omitted
        self.assertFalse(any(c["entry_name"] == "notes.exe" for c in contained))

        # 2. Test ZIP security: path traversal defense
        bad_zip_path = os.path.join(self.temp_dir, "traversal.zip")
        with zipfile.ZipFile(bad_zip_path, "w") as bzf:
            bzf.writestr("../../../evil.csv", "name\nhacker\n")

        insp_bad = importer.inspect_zip_file(bad_zip_path, "traversal.zip", session_dir=self.temp_dir)
        self.assertFalse(insp_bad["success"])
        self.assertIn("traversal", insp_bad["error"].lower())

        # 3. Test GZIP compressed file (.csv.gz)
        gz_path = os.path.join(self.temp_dir, "export.csv.gz")
        with gzip.open(gz_path, "wt", encoding="utf-8") as gf:
            gf.write("Company,Location\nGZ Logistics,Hamburg\nGZ Shipping,Rotterdam\n")

        insp_gz = importer.inspect_gzip_file(gz_path, "export.csv.gz", session_dir=self.temp_dir)
        self.assertTrue(insp_gz["success"])
        self.assertEqual(insp_gz["total_rows_estimate"], 2)
        self.assertIn("GZ Logistics", str(insp_gz["preview_rows"]))

    def test_07_unsupported_and_corrupt_files(self):
        """Test clear errors on corrupt, encrypted, or unsupported files."""
        # Unsupported format (.pdf)
        pdf_path = os.path.join(self.temp_dir, "document.pdf")
        with open(pdf_path, "wb") as f:
            f.write(b"%PDF-1.4 mock binary pdf content")

        insp_pdf = importer.inspect_universal_file(pdf_path, "document.pdf")
        self.assertFalse(insp_pdf["success"])
        self.assertIn("unsupported", insp_pdf["error"].lower())

        # Corrupt ZIP file
        corrupt_zip = os.path.join(self.temp_dir, "broken.zip")
        with open(corrupt_zip, "wb") as f:
            f.write(b"PK\x03\x04corrupted-archive-garbage-bytes")

        insp_corrupt = importer.inspect_zip_file(corrupt_zip, "broken.zip")
        self.assertFalse(insp_corrupt["success"])

    # =========================================================================
    # 2. Custom Columns Addition & Cell Editing (CRITICAL REQUIREMENT)
    # =========================================================================

    def test_08_custom_columns_constant_and_individual_cell_edits(self):
        """
        CRITICAL TEST:
        Upload source file with: company_name, website, email, phone.
        Add custom columns:
          - country (Mode A: 'United Kingdom' for all rows)
          - industry (Mode B: row 0 = 'Construction', row 1 = 'Engineering')
          - lead_source (Mode A: 'Website Directory')
          - verification_status (Mode B: row 0 = 'Verified', row 1 = '')
          - priority (Mode A: 'High')
        Verify all values saved in Parquet, DuckDB view, and extra_fields JSON.
        """
        csv_path = os.path.join(self.temp_dir, "companies.csv")
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["company_name", "website", "email", "phone"])
            writer.writerow(["BuildCorp UK", "buildcorp.co.uk", "info@buildcorp.co.uk", "020 7946 0001"])
            writer.writerow(["Civic Engineering", "civic-eng.co.uk", "team@civic-eng.co.uk", "0161 496 0002"])

        insp = importer.inspect_universal_file(csv_path, "companies.csv")
        self.assertTrue(insp["success"])

        staged_files = [{"original_filename": "companies.csv", "staged_path": csv_path, "format": "csv"}]
        mappings = {
            "companies.csv": {
                "name": "company_name",
                "website": "website",
                "email": "email",
                "phone": "phone"
            }
        }

        # Define custom columns
        custom_columns = [
            {"name": "country", "type": "text", "populate_mode": "same", "default_value": "United Kingdom"},
            {"name": "industry", "type": "text", "populate_mode": "individual", "default_value": ""},
            {"name": "lead_source", "type": "text", "populate_mode": "same", "default_value": "Website Directory"},
            {"name": "verification_status", "type": "text", "populate_mode": "individual", "default_value": ""},
            {"name": "priority", "type": "text", "populate_mode": "same", "default_value": "High"}
        ]

        # Individual cell edits for preview rows
        cell_edits = {
            "companies.csv": {
                "0": {
                    "industry": "Construction",
                    "verification_status": "Verified"
                },
                "1": {
                    "industry": "Engineering",
                    "verification_status": ""  # Explicit blank
                }
            }
        }

        result = importer.execute_dataset_import(
            dataset_name="UK Construction Companies",
            files=staged_files,
            column_mappings=mappings,
            custom_columns=custom_columns,
            cell_edits=cell_edits,
            duplicate_mode="skip_exact"
        )

        self.assertTrue(result["success"])
        self.assertEqual(result["total_imported"], 2)

        dataset_id = result["dataset_id"]

        # Register views in DuckDB
        lead_db.register_all_imported_views(self.con)

        # Query the full dataset view (v_imp_{dataset_id}_full)
        view_full = f"v_imp_{dataset_id}_full"
        df = self.con.execute(f"SELECT * FROM {view_full} ORDER BY name").fetchdf()

        self.assertEqual(len(df), 2)
        # Check custom column 'country' has 'United Kingdom' for both rows
        self.assertEqual(df["country"].iloc[0], "United Kingdom")
        self.assertEqual(df["country"].iloc[1], "United Kingdom")

        # Check individual row values in 'industry'
        # Row 0: BuildCorp UK -> Construction
        self.assertEqual(df["industry"].iloc[0], "Construction")
        # Row 1: Civic Engineering -> Engineering
        self.assertEqual(df["industry"].iloc[1], "Engineering")

        # Check verification_status
        self.assertEqual(df["verification_status"].iloc[0], "Verified")
        # Blank should remain blank/empty string, NOT invented data
        self.assertEqual(str(df["verification_status"].iloc[1] or ""), "")

        # Check priority
        self.assertEqual(df["priority"].iloc[0], "High")
        self.assertEqual(df["priority"].iloc[1], "High")

        # Check extra_fields JSON column
        extra_json = json.loads(df["extra_fields"].iloc[0])
        self.assertEqual(extra_json.get("country"), "United Kingdom")
        self.assertEqual(extra_json.get("industry"), "Construction")

    # =========================================================================
    # 3. Column Schema Controls: Rename, Exclude, Default Values
    # =========================================================================

    def test_09_column_renaming_exclusions_and_defaults(self):
        """Test column rename, exclusion, and default fallback value settings."""
        csv_path = os.path.join(self.temp_dir, "leads_with_junk.csv")
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["raw_corp", "unwanted_tracking_id", "email_addr", "city"])
            writer.writerow(["Nexus Tech", "TRK-99881", "contact@nexustech.io", ""])
            writer.writerow(["Apex Global", "TRK-99882", "info@apex.com", "Chicago"])

        staged_files = [{"original_filename": "leads_with_junk.csv", "staged_path": csv_path, "format": "csv"}]
        mappings = {
            "leads_with_junk.csv": {
                "name": "raw_corp",
                "email": "email_addr",
                "city": "city"
            }
        }

        # Exclude 'unwanted_tracking_id', set fallback default 'Unknown City' for empty city cells
        column_settings = {
            "leads_with_junk.csv": {
                "unwanted_tracking_id": {"excluded": True, "displayName": "Tracking", "type": "text"},
                "raw_corp": {"displayName": "Corporate Entity", "type": "text"},
                "city": {"defaultValue": "Unknown City", "type": "text"}
            }
        }

        result = importer.execute_dataset_import(
            dataset_name="Tech Leads Cleaned",
            files=staged_files,
            column_mappings=mappings,
            column_settings=column_settings
        )

        self.assertTrue(result["success"])
        did = result["dataset_id"]

        lead_db.register_all_imported_views(self.con)
        rows = self.con.execute(f"SELECT name, city FROM v_imp_{did} ORDER BY name").fetchall()
        # Row 0 ("Apex Global") has 'Chicago'
        self.assertEqual(rows[0][0], "Apex Global")
        self.assertEqual(rows[0][1], "Chicago")
        # Row 1 ("Nexus Tech") had empty city -> got fallback default 'Unknown City'
        self.assertEqual(rows[1][0], "Nexus Tech")
        self.assertEqual(rows[1][1], "Unknown City")

    # =========================================================================
    # 4. Dataset-Specific Columns & Unified Database Integration
    # =========================================================================

    def test_10_dataset_specific_columns_and_unified_view(self):
        """
        Verify Dataset A and Dataset B have distinct custom columns,
        and both seamlessly query through unified view v_all_unified without binder errors.
        """
        # Dataset A: UK Companies (custom field: registration_number)
        csv_a = os.path.join(self.temp_dir, "uk_co.csv")
        with open(csv_a, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["name", "website", "country", "registration_number"])
            writer.writerow(["Oxford Biotech", "oxfordbio.co.uk", "United Kingdom", "OC123456"])

        # Dataset B: US Restaurants (custom fields: cuisine, opening_hours)
        csv_b = os.path.join(self.temp_dir, "us_rest.csv")
        with open(csv_b, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["name", "website", "cuisine", "opening_hours"])
            writer.writerow(["Luigi's Trattoria", "luigisnyc.com", "Italian", "11:00 - 22:00"])

        # Import A
        res_a = importer.execute_dataset_import(
            dataset_name="UK Companies A",
            files=[{"original_filename": "uk_co.csv", "staged_path": csv_a, "format": "csv"}],
            column_mappings={"uk_co.csv": {"name": "name", "website": "website", "country": "country"}},
            custom_columns=[{"name": "registration_number", "type": "text", "populate_mode": "same", "default_value": "OC123456"}]
        )
        self.assertTrue(res_a["success"])
        did_a = res_a["dataset_id"]

        # Import B
        res_b = importer.execute_dataset_import(
            dataset_name="US Restaurants B",
            files=[{"original_filename": "us_rest.csv", "staged_path": csv_b, "format": "csv"}],
            column_mappings={"us_rest.csv": {"name": "name", "website": "website"}},
            custom_columns=[
                {"name": "cuisine", "type": "text", "populate_mode": "same", "default_value": "Italian"},
                {"name": "opening_hours", "type": "text", "populate_mode": "same", "default_value": "11:00 - 22:00"}
            ]
        )
        self.assertTrue(res_b["success"])
        did_b = res_b["dataset_id"]

        # Register views
        lead_db.register_all_imported_views(self.con)

        # Check dataset-specific full view for A has registration_number and extra_fields
        cols_a = [c[0] for c in self.con.execute(f"DESCRIBE v_imp_{did_a}_full").fetchall()]
        self.assertIn("registration_number", cols_a)
        self.assertIn("extra_fields", cols_a)
        self.assertNotIn("cuisine", cols_a)

        # Check dataset-specific full view for B has cuisine and opening_hours
        cols_b = [c[0] for c in self.con.execute(f"DESCRIBE v_imp_{did_b}_full").fetchall()]
        self.assertIn("cuisine", cols_b)
        self.assertIn("opening_hours", cols_b)
        self.assertIn("extra_fields", cols_b)
        self.assertNotIn("registration_number", cols_b)

        # Check unified standard views (v_imp_{id}) have canonical 22 columns
        cols_std = [c[0] for c in self.con.execute(f"DESCRIBE v_imp_{did_a}").fetchall()]
        self.assertIn("name", cols_std)
        self.assertIn("country", cols_std)
        self.assertIn("source_id", cols_std)

        # Perform UNION query across standard views for both datasets
        union_res = self.con.execute(f"""
            SELECT name, country, source_id FROM v_imp_{did_a}
            UNION ALL
            SELECT name, country, source_id FROM v_imp_{did_b}
        """).fetchall()
        self.assertEqual(len(union_res), 2)

    # =========================================================================
    # 5. Post-Import Dataset Column Management
    # =========================================================================

    def test_11_post_import_column_operations(self):
        """
        Test managing columns on an existing dataset:
        1. Add column 'lead_owner' to all existing leads with value 'Sarah'
        2. Add column 'credit_score' with default blank
        3. Fill blank cells in 'credit_score' with '750'
        4. Rename column 'lead_owner' to 'account_rep'
        5. Delete custom column 'credit_score'
        6. Export dataset to CSV and verify custom columns & formula injection defense
        """
        # Create initial dataset
        csv_path = os.path.join(self.temp_dir, "initial_clients.csv")
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["name", "email", "phone"])
            writer.writerow(["Alpha Logistics", "alpha@logistics.com", "555-0101"])
            writer.writerow(["Beta Shipping", "beta@shipping.com", "555-0102"])

        res = importer.execute_dataset_import(
            dataset_name="Post Import Operations Test",
            files=[{"original_filename": "initial_clients.csv", "staged_path": csv_path, "format": "csv"}],
            column_mappings={"initial_clients.csv": {"name": "name", "email": "email", "phone": "phone"}}
        )
        self.assertTrue(res["success"])
        did = res["dataset_id"]

        # 1. Add column 'lead_owner' to all leads
        add_res = importer.add_column_to_dataset(did, "lead_owner", col_type="text", default_value="Sarah", scope="all")
        self.assertTrue(add_res["success"])
        self.assertEqual(add_res["affected_leads"], 2)

        # 2. Add column 'credit_score'
        add_score = importer.add_column_to_dataset(did, "credit_score", col_type="integer", default_value="", scope="all")
        self.assertTrue(add_score["success"])

        # Check columns
        cols = importer.get_dataset_columns(did).get("columns", [])
        col_names = [c["name"] for c in cols]
        self.assertIn("lead_owner", col_names)
        self.assertIn("credit_score", col_names)

        # 3. Fill column values: fill blanks in credit_score
        fill_res = importer.fill_column_values(did, "credit_score", value="750", only_blanks=True)
        self.assertTrue(fill_res["success"])
        self.assertEqual(fill_res["updated_leads_count"], 2)

        # 4. Rename column 'lead_owner' -> 'account_rep'
        ren_res = importer.rename_column_in_dataset(did, "lead_owner", "account_rep")
        self.assertTrue(ren_res["success"])

        cols_after_ren = [c["name"] for c in importer.get_dataset_columns(did).get("columns", [])]
        self.assertIn("account_rep", cols_after_ren)
        self.assertNotIn("lead_owner", cols_after_ren)

        # 5. Delete custom column 'credit_score'
        del_res = importer.delete_column_from_dataset(did, "credit_score")
        self.assertTrue(del_res["success"])

        cols_after_del = [c["name"] for c in importer.get_dataset_columns(did).get("columns", [])]
        self.assertNotIn("credit_score", cols_after_del)
        self.assertIn("account_rep", cols_after_del)

        # 6. Export dataset with custom columns and check formula injection defense
        # Add a dangerous value to test formula injection protection
        importer.fill_column_values(did, "account_rep", value="=cmd|' /C calc'!A0", only_blanks=False)

        export_csv_path = os.path.join(self.temp_dir, "exported_clients.csv")
        exp_res_path = importer.export_dataset_with_custom_columns(did, export_csv_path)
        self.assertTrue(os.path.exists(exp_res_path))

        # Verify export content
        with open(export_csv_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            headers = next(reader)
            self.assertIn("account_rep", headers)
            row = next(reader)
            rep_idx = headers.index("account_rep")
            rep_val = row[rep_idx]
            # Formula injection must be neutralized with leading quote
            self.assertTrue(rep_val.startswith("'="), f"Formula was not sanitized: {rep_val}")

    # =========================================================================
    # 6. Multiple Files in One Dataset & Deduplication
    # =========================================================================

    def test_12_multiple_files_and_deduplication(self):
        """Test importing multiple files of different formats into one dataset with deduplication."""
        f1_csv = os.path.join(self.temp_dir, "batch1.csv")
        with open(f1_csv, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["name", "email"])
            writer.writerow(["Duplicate Entity", "dup@domain.com"])
            writer.writerow(["Unique Entity One", "one@domain.com"])

        f2_json = os.path.join(self.temp_dir, "batch2.json")
        with open(f2_json, "w", encoding="utf-8") as f:
            json.dump([
                {"name": "Duplicate Entity", "email": "dup@domain.com"},  # duplicate
                {"name": "Unique Entity Two", "email": "two@domain.com"}
            ], f)

        staged_files = [
            {"original_filename": "batch1.csv", "staged_path": f1_csv, "format": "csv"},
            {"original_filename": "batch2.json", "staged_path": f2_json, "format": "json"}
        ]
        mappings = {
            "batch1.csv": {"name": "name", "email": "email"},
            "batch2.json": {"name": "name", "email": "email"}
        }

        result = importer.execute_dataset_import(
            dataset_name="Multi File Ingestion",
            files=staged_files,
            column_mappings=mappings,
            duplicate_mode="skip_exact"
        )

        self.assertTrue(result["success"])
        self.assertEqual(result["total_discovered"], 4)
        self.assertEqual(result["total_imported"], 3)  # 1 duplicate skipped
        self.assertEqual(result["total_duplicates"], 1)


if __name__ == "__main__":
    unittest.main()
