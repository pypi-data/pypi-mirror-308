import unittest
from unittest.mock import Mock, patch, mock_open
from pathlib import Path
import django
from django.conf import settings
from django.test import override_settings
from django_spellbook.management.commands.processing.file_processor import (
    MarkdownFileProcessor,
    MarkdownProcessingError,
)


def setup_django_settings():
    from django.conf import settings
    if not settings.configured:
        settings.configure(
            DEBUG=True,
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': ':memory:',
                }
            },
            INSTALLED_APPS=[
                'django_spellbook',
            ],
            MIDDLEWARE=[],
            ROOT_URLCONF=[],
            TEMPLATES=[],
            SECRET_KEY='test-key',
            SPELLBOOK_MD_PATH='/fake/path',
        )
    django.setup()


# Run settings configuration before tests
setup_django_settings()


class TestMarkdownFileProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = MarkdownFileProcessor()

    @override_settings(SPELLBOOK_MD_PATH='/fake/path')
    def test_validate_and_get_path(self):
        """Test path validation and creation"""
        dirpath = "/test/path"
        filename = "test.md"

        result = self.processor._validate_and_get_path(dirpath, filename)

        self.assertIsInstance(result, Path)
        self.assertEqual(str(result), "/test/path/test.md")

    @override_settings(SPELLBOOK_MD_PATH='/fake/path')
    def test_validate_and_get_path_invalid(self):
        """Test path validation with invalid input"""
        dirpath = None
        filename = "test.md"

        with self.assertRaises(MarkdownProcessingError):
            self.processor._validate_and_get_path(dirpath, filename)

    @override_settings(SPELLBOOK_MD_PATH='/fake/path')
    @patch('builtins.open', new_callable=mock_open, read_data="# Test Content")
    def test_read_markdown_file(self, mock_file):
        """Test reading markdown file content"""
        test_path = Path("/test/path/test.md")

        content = self.processor._read_markdown_file(test_path)

        self.assertEqual(content, "# Test Content")
        mock_file.assert_called_once_with(test_path, 'r', encoding='utf-8')

    @override_settings(SPELLBOOK_MD_PATH='/fake/path')
    @patch('builtins.open')
    def test_read_markdown_file_error(self, mock_file):
        """Test reading markdown file with error"""
        mock_file.side_effect = IOError("File not found")
        test_path = Path("/test/path/test.md")

        with self.assertRaises(MarkdownProcessingError) as context:
            self.processor._read_markdown_file(test_path)

        self.assertIn("Error reading file", str(context.exception))

    @override_settings(SPELLBOOK_MD_PATH='/fake/path')
    @patch('django_spellbook.management.commands.processing.file_processor.FrontMatterParser')
    @patch('django_spellbook.management.commands.processing.file_processor.MarkdownParser')
    def test_process_markdown_content(self, mock_md_parser, mock_frontmatter):
        """Test markdown content processing"""
        # Setup mocks
        mock_frontmatter.return_value.raw_content = "# Test Content"
        mock_md_parser.return_value.get_html.return_value = "<h1>Test Content</h1>"

        md_text = "---\ntitle: Test\n---\n# Test Content"
        file_path = Path("/test/path/test.md")

        html_content, frontmatter = self.processor._process_markdown_content(
            md_text, file_path)

        self.assertEqual(html_content, "<h1>Test Content</h1>")
        mock_frontmatter.assert_called_once_with(md_text, file_path)

    @override_settings(SPELLBOOK_MD_PATH='/fake/path')
    def test_calculate_relative_url(self):
        """Test relative URL calculation"""
        file_path = Path("/fake/path/subfolder/test.md")

        relative_url = self.processor._calculate_relative_url(file_path)

        self.assertEqual(relative_url, "subfolder/test")

    @override_settings(SPELLBOOK_MD_PATH='/fake/path')
    @patch('django_spellbook.management.commands.spellbook_md.FrontMatterParser')
    def test_generate_file_metadata(self, mock_frontmatter):
        """Test file metadata generation"""
        # Setup
        file_path = Path("/fake/path/test.md")
        html_content = "<h1>Test</h1>"
        mock_context = Mock()
        mock_frontmatter.return_value.get_context.return_value = mock_context

        processed_content = (html_content, mock_frontmatter.return_value)

        # Test
        result_html, result_path, result_context = self.processor._generate_file_metadata(
            file_path, processed_content
        )

        # Assertions
        self.assertEqual(result_html, html_content)
        self.assertEqual(result_path, file_path)
        self.assertEqual(result_context, mock_context)

    @override_settings(SPELLBOOK_MD_PATH='/fake/path')
    @patch.object(MarkdownFileProcessor, '_validate_and_get_path')
    @patch.object(MarkdownFileProcessor, '_read_markdown_file')
    @patch.object(MarkdownFileProcessor, '_process_markdown_content')
    @patch.object(MarkdownFileProcessor, '_generate_file_metadata')
    def test_process_file_integration(self, mock_generate, mock_process,
                                      mock_read, mock_validate):
        """Test the full process_file integration"""
        # Setup mocks
        mock_validate.return_value = Path("/test/path/test.md")
        mock_read.return_value = "# Test Content"
        mock_process.return_value = ("<h1>Test Content</h1>", Mock())
        mock_generate.return_value = ("<h1>Test Content</h1>",
                                      Path("/test/path/test.md"),
                                      Mock())

        # Test
        result = self.processor.process_file(
            Path("/test/path"),
            "/test/path",
            "test.md",
            ["test"]
        )

        # Assertions
        self.assertIsNotNone(result)
        mock_validate.assert_called_once()
        mock_read.assert_called_once()
        mock_process.assert_called_once()
        mock_generate.assert_called_once()
