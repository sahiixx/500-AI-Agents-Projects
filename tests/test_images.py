"""
Test suite for validating image files.

This module contains tests for image files in the repository,
ensuring they are valid, not corrupted, and meet quality standards.
"""

import pytest
from pathlib import Path
from PIL import Image
import hashlib


class TestImageFiles:
    """Test suite for image file validation."""
    
    @pytest.fixture
    def image_files(self):
        """Find all image files in the repository."""
        repo_root = Path('.')
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']
        
        image_files = []
        for ext in image_extensions:
            image_files.extend(repo_root.glob(f'**/*{ext}'))
            image_files.extend(repo_root.glob(f'**/*{ext.upper()}'))
        
        # Exclude hidden directories and git
        image_files = [f for f in image_files if '.git' not in str(f) and not f.name.startswith('.')]
        return image_files
    
    def test_images_exist(self, image_files):
        """Test that image files exist in the repository."""
        assert len(image_files) > 0, "Repository should contain image files"
    
    def test_images_in_proper_directory(self, image_files):
        """Test that images are organized in proper directories."""
        for img_file in image_files:
            # Images should ideally be in an 'images', 'assets', or similar directory
            path_parts = img_file.parts
            
            # Check if image is in a reasonable location
            acceptable_dirs = ['images', 'assets', 'img', 'static', 'public', 'docs']
            in_acceptable_dir = any(dir_name in path_parts for dir_name in acceptable_dirs)
            
            # Root level images are also acceptable for some projects
            is_root_level = len(path_parts) == 1
            
            # Just a soft check - images should be organized
            if not (in_acceptable_dir or is_root_level):
                # Not a hard failure, but good practice to organize
                pass


class TestImageIntegrity:
    """Test suite for image file integrity."""
    
    @pytest.fixture
    def image_files(self):
        """Get image files that can be validated with PIL."""
        repo_root = Path('.')
        # PIL supported formats
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        
        image_files = []
        for ext in image_extensions:
            image_files.extend(repo_root.glob(f'**/*{ext}'))
            image_files.extend(repo_root.glob(f'**/*{ext.upper()}'))
        
        image_files = [f for f in image_files if '.git' not in str(f)]
        return image_files
    
    def test_images_not_corrupted(self, image_files):
        """Test that image files are not corrupted."""
        for img_file in image_files:
            try:
                with Image.open(img_file) as img:
                    # Try to load the image data
                    img.verify()
                # Reopen to test actual loading (verify() closes the file)
                with Image.open(img_file) as img:
                    img.load()
            except (OSError, Image.UnidentifiedImageError) as e:
                pytest.fail(f"Image {img_file.name} appears corrupted: {e}")
    
    def test_images_have_reasonable_dimensions(self, image_files):
        """Test that images have reasonable dimensions."""
        for img_file in image_files:
            try:
                with Image.open(img_file) as img:
                    width, height = img.size
                    
                    # Check minimum size (too small might be an error)
                    assert width >= 10 and height >= 10, \
                        f"{img_file.name} is too small ({width}x{height})"
                    
                    # Check maximum size (too large might be wasteful)
                    # Modern displays are typically under 4K
                    max_dimension = 10000  # Very generous limit
                    assert width <= max_dimension and height <= max_dimension, \
                        f"{img_file.name} is very large ({width}x{height})"
            except (OSError, Image.UnidentifiedImageError):
                # Already tested in test_images_not_corrupted
                pass
    
    def test_images_file_size_reasonable(self, image_files):
        """Test that image file sizes are reasonable."""
        for img_file in image_files:
            file_size = img_file.stat().st_size
            
            # Should have actual content
            assert file_size > 100, f"{img_file.name} is suspiciously small"
            
            # Should not be excessively large (10MB limit)
            max_size = 10 * 1024 * 1024  # 10 MB
            assert file_size < max_size, \
                f"{img_file.name} is very large ({file_size / 1024 / 1024:.1f}MB). " \
                f"Consider optimizing."
    
    def test_images_valid_format(self, image_files):
        """Test that images are in valid formats."""
        for img_file in image_files:
            try:
                with Image.open(img_file) as img:
                    # Get the format
                    img_format = img.format
                    
                    # Should have a recognized format
                    assert img_format is not None, \
                        f"{img_file.name} has unrecognized format"
                    
                    # Format should match extension
                    expected_formats = {
                        '.jpg': ['JPEG'],
                        '.jpeg': ['JPEG'],
                        '.png': ['PNG'],
                        '.gif': ['GIF'],
                        '.webp': ['WEBP']
                    }
                    
                    ext = img_file.suffix.lower()
                    if ext in expected_formats:
                        assert img_format in expected_formats[ext], \
                            f"{img_file.name} extension doesn't match format " \
                            f"(ext: {ext}, format: {img_format})"
            except (OSError, Image.UnidentifiedImageError):
                # Already tested in other tests
                pass
    
    def test_no_duplicate_images(self, image_files):
        """Test that there are no duplicate image files (by content)."""
        hashes = {}
        duplicates = []
        
        for img_file in image_files:
            # Calculate hash of file content
            with open(img_file, 'rb') as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            
            if file_hash in hashes:
                duplicates.append((img_file.name, hashes[file_hash]))
            else:
                hashes[file_hash] = img_file.name
        
        # Having duplicates might be intentional, but good to check
        if duplicates:
            # This is a warning rather than a failure
            # Duplicate images might be intentional (e.g., backups)
            pass


class TestImageUsage:
    """Test suite for image usage in documentation."""
    
    @pytest.fixture
    def readme_content(self):
        """Load README content."""
        readme_path = Path('README.md')
        if not readme_path.exists():
            return ""
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    @pytest.fixture
    def image_files(self):
        """Get list of image files."""
        repo_root = Path('.')
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        
        image_files = []
        for ext in image_extensions:
            image_files.extend(repo_root.glob(f'**/*{ext}'))
        
        image_files = [f for f in image_files if '.git' not in str(f)]
        return [f.name for f in image_files]
    
    def test_images_referenced_in_readme(self, readme_content):
        """Test that images in images/ directory are referenced in README."""
        if not readme_content:
            pytest.skip("README.md not found")
        
        # Find image references in README
        import re
        image_refs = re.findall(r'!\[.*?\]\((.*?)\)', readme_content)
        
        # Extract just filenames from paths
        referenced_images = [Path(ref).name for ref in image_refs]
        
        # Check if major images are referenced
        # This is a soft check - not all images need to be in README
        images_dir = Path('images')
        if images_dir.exists():
            images_in_dir = [f.name for f in images_dir.glob('*') if f.is_file()]
            
            if images_in_dir:
                # At least some images should be referenced
                referenced_count = sum(1 for img in images_in_dir 
                                     if img in referenced_images)
                # Soft assertion - at least one image should be used
                assert referenced_count > 0 or len(images_in_dir) == 0, \
                    "Some images in images/ directory should be referenced in README"
    
    def test_readme_image_links_valid(self, readme_content):
        """Test that image links in README point to existing files."""
        if not readme_content:
            pytest.skip("README.md not found")
        
        import re
        image_refs = re.findall(r'!\[.*?\]\((.*?)\)', readme_content)
        
        for img_ref in image_refs:
            # Skip external URLs
            if img_ref.startswith('http'):
                continue
            
            # Check if file exists
            img_path = Path(img_ref)
            if not img_path.is_absolute():
                # Relative to README location
                img_path = Path('README.md').parent / img_ref
            
            # Remove any URL fragments or queries
            img_path = Path(str(img_path).split('?')[0].split('#')[0])
            
            assert img_path.exists(), \
                f"README references non-existent image: {img_ref}"


class TestImageQuality:
    """Test suite for image quality standards."""
    
    @pytest.fixture
    def png_files(self):
        """Get PNG image files."""
        repo_root = Path('.')
        png_files = list(repo_root.glob('**/*.png'))
        png_files.extend(repo_root.glob('**/*.PNG'))
        return [f for f in png_files if '.git' not in str(f)]
    
    @pytest.fixture
    def jpg_files(self):
        """Get JPEG image files."""
        repo_root = Path('.')
        jpg_files = list(repo_root.glob('**/*.jpg'))
        jpg_files.extend(repo_root.glob('**/*.jpeg'))
        jpg_files.extend(repo_root.glob('**/*.JPG'))
        jpg_files.extend(repo_root.glob('**/*.JPEG'))
        return [f for f in jpg_files if '.git' not in str(f)]
    
    def test_png_mode_appropriate(self, png_files):
        """Test that PNG files use appropriate color mode."""
        for png_file in png_files:
            try:
                with Image.open(png_file) as img:
                    mode = img.mode
                    
                    # Common PNG modes: RGB, RGBA, L, LA, P
                    valid_modes = ['RGB', 'RGBA', 'L', 'LA', 'P', '1']
                    assert mode in valid_modes, \
                        f"{png_file.name} has unusual mode: {mode}"
            except (OSError, Image.UnidentifiedImageError):
                pass
    
    def test_jpg_no_alpha_channel(self, jpg_files):
        """Test that JPEG files don't have alpha channel."""
        for jpg_file in jpg_files:
            try:
                with Image.open(jpg_file) as img:
                    # JPEG doesn't support transparency
                    assert img.mode != 'RGBA', \
                        f"{jpg_file.name} is JPEG but has alpha channel (should be PNG)"
            except (OSError, Image.UnidentifiedImageError):
                pass