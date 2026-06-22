import os
import tempfile
import shutil
import unittest
from src.context.repomap import RepoMapGenerator

class TestRepoMap(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_compaction(self):
        file_path = os.path.join(self.test_dir, "math_utils.py")
        code = (
            "class Calculator:\n"
            "    def add(self, a: int, b: int) -> int:\n"
            "        return a + b\n\n"
            "def greet(name: str):\n"
            "    print(name)\n"
        )
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)

        generator = RepoMapGenerator(self.test_dir)
        compact_map = generator.generate_compact_map()

        self.assertIn("class Calculator:", compact_map)
        self.assertIn("def add(self, a: int, b: int) -> int", compact_map)
        self.assertIn("def greet(name: str)", compact_map)

if __name__ == "__main__":
    unittest.main()
