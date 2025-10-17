"""
Unit tests for file reading utilities
Tests PDF, DOCX, and TXT file reading functionality
"""

import sys
from pathlib import Path

import pytest

from src.utils.file_readers import FileReader

# Ensure module import
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))


class TestFileReader:
    """Test suite for file reading functionality"""

    @pytest.fixture
    def reader(self):
        """Create a file reader instance"""
        return FileReader()

    @pytest.fixture
    def temp_txt_file(self, tmp_path):
        """Create a temporary text file"""
        file_path = tmp_path / "test.txt"
        content = "This is a test text file.\nWith multiple lines.\nFor testing purposes."
        file_path.write_text(content, encoding="utf-8")
        return file_path

    def test_read_txt_file(self, reader, temp_txt_file):
        """Test reading plain text files"""
        content = reader.read_file(str(temp_txt_file))

        assert "test text file" in content
        assert "multiple lines" in content

    def test_detect_file_type(self, reader):
        """Test file type detection"""
        assert reader.detect_type("document.txt") == "txt"
        assert reader.detect_type("document.pdf") == "pdf"
        assert reader.detect_type("document.docx") == "docx"
        assert reader.detect_type("document.doc") == "doc"

    def test_file_not_found(self, reader):
        """Test handling of non-existent files"""
        with pytest.raises(FileNotFoundError):
            reader.read_file("nonexistent_file.txt")

    def test_unsupported_file_type(self, reader):
        """Test handling of unsupported file types"""
        with pytest.raises(ValueError):
            reader.read_file("document.xyz")

    def test_empty_file(self, reader, tmp_path):
        """Test reading empty file"""
        empty_file = tmp_path / "empty.txt"
        empty_file.write_text("", encoding="utf-8")

        content = reader.read_file(str(empty_file))
        assert content == ""

    def test_unicode_content(self, reader, tmp_path):
        """Test reading files with unicode characters"""
        unicode_file = tmp_path / "unicode.txt"
        content = "Hello 世界!\nПривет мир!"
        unicode_file.write_text(content, encoding="utf-8")

        read_content = reader.read_file(str(unicode_file))
        assert "世界" in read_content
        assert "Привет" in read_content

    def test_large_file(self, reader, tmp_path):
        """Test reading large files"""
        large_file = tmp_path / "large.txt"
        content = "Line\n" * 10000  # 10,000 lines
        large_file.write_text(content, encoding="utf-8")

        read_content = reader.read_file(str(large_file))
        assert len(read_content) > 0
        assert read_content.count("Line") == 10000


class TestFileReaderUtilities:
    """Test file reader utility functions"""

    @pytest.fixture
    def reader(self):
        return FileReader()

    def test_clean_text(self, reader):
        """Test text cleaning function"""
        dirty_text = "Text  with   extra    spaces\n\n\nand\n\n\nnewlines"
        clean = reader.clean_text(dirty_text)

        assert "  " not in clean
        assert "\n\n\n" not in clean

    def test_extract_metadata(self, reader, tmp_path):
        """Test metadata extraction"""
        file_path = tmp_path / "meta.txt"
        file_path.write_text("Metadata test")
        metadata = reader.get_metadata(str(file_path))

        assert "file_size" in metadata
        assert "file_type" in metadata
        assert "created_date" in metadata

    def test_validate_file(self, reader, tmp_path):
        """Test file validation"""
        file_path = tmp_path / "valid.txt"
        file_path.write_text("Valid test file")
        is_valid = reader.validate_file(str(file_path))

        assert is_valid is True

    def test_get_file_encoding(self, reader, tmp_path):
        """Test file encoding detection"""
        file_path = tmp_path / "encode.txt"
        file_path.write_text("Encoding test äöü", encoding="utf-8")

        encoding = reader.detect_encoding(str(file_path))
        assert encoding in ["utf-8", "ascii", "latin-1"]


class TestBatchFileReading:
    """Test batch file reading operations"""

    @pytest.fixture
    def reader(self):
        return FileReader()

    def test_read_multiple_files(self, reader, tmp_path):
        """Test reading multiple files at once"""
        files = []
        for i in range(3):
            file_path = tmp_path / f"file{i}.txt"
            file_path.write_text(f"Content of file {i}")
            files.append(str(file_path))

        contents = reader.read_multiple(files)

        assert len(contents) == 3
        assert all("Content of file" in c for c in contents)

    def test_read_directory(self, reader, tmp_path):
        """Test reading all files in a directory"""
        for i in range(3):
            file_path = tmp_path / f"file{i}.txt"
            file_path.write_text(f"File {i}")

        contents = reader.read_directory(str(tmp_path), pattern="*.txt")
        assert len(contents) >= 3

    def test_filter_by_extension(self, reader, tmp_path):
        """Test filtering files by extension"""
        (tmp_path / "file1.txt").write_text("Text 1")
        (tmp_path / "file2.pdf").write_text("PDF content")
        (tmp_path / "file3.txt").write_text("Text 2")

        txt_files = reader.filter_files(str(tmp_path), extensions=[".txt"])
        assert len(txt_files) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
