# This test file was written for the SQLite database layer.
# That layer has been removed in favour of SessionStore + CSV audit logging.
# Delete this file and write new tests against the new API when needed.
raise SystemExit("test_db.py is stale — delete and rewrite for SessionStore.")

import database


class DatabaseInitializationTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.prev_data_dir = os.environ.get("ETHICAL_CRAWLER_DATA_DIR")
        os.environ["ETHICAL_CRAWLER_DATA_DIR"] = self.temp_dir.name
        database.DATABASE_PATH = Path(self.temp_dir.name) / "db" / "li_evidence.db"

    def tearDown(self):
        if self.prev_data_dir is None:
            os.environ.pop("ETHICAL_CRAWLER_DATA_DIR", None)
        else:
            os.environ["ETHICAL_CRAWLER_DATA_DIR"] = self.prev_data_dir
        self.temp_dir.cleanup()

    def test_init_db_uses_runtime_paths_and_creates_expected_tables(self):
        conn, cursor = database.init_db(debug=True)

        self.assertIsNotNone(conn)
        self.assertIsNotNone(cursor)
        self.assertTrue(database.DATABASE_PATH.exists())
        self.assertEqual(database.get_session_state_dir(), Path(self.temp_dir.name) / "session_states")

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        table_names = {row[0] for row in cursor.fetchall()}

        self.assertTrue({"users", "personalities", "quips", "mood_config", "services", "sessions", "logs", "evidence"}.issubset(table_names))

        conn.close()


if __name__ == "__main__":
    unittest.main()