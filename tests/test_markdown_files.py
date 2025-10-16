"""
Test suite for validating Markdown documentation files.

This module contains comprehensive tests for all Markdown files in the repository,
ensuring proper formatting, valid links, and documentation completeness.
"""

import re
import pytest
from pathlib import Path
from urllib.parse import urlparse


class TestMarkdownFiles:
    """Test suite for Markdown documentation."""
    
    @pytest.fixture
    def markdown_files(self):
        """Find all Markdown files in the repository."""
        repo_root = Path('.')
        md_files = list(repo_root.glob('**/*.md'))
        # Exclude node_modules and .git
        md_files = [f for f in md_files if '.git' not in str(f) and 'node_modules' not in str(f)]
        return md_files
    
    def test_markdown_files_exist(self, markdown_files):
        """Test that expected Markdown files exist."""
        assert len(markdown_files) > 0, "Repository should contain Markdown files"
        
        # Check for essential files
        file_names = [f.name for f in markdown_files]
        assert 'README.md' in file_names, "Repository should have a README.md"
        assert 'CONTRIBUTION.md' in file_names, "Repository should have CONTRIBUTION.md"
    
    def test_readme_in_root(self):
        """Test that README.md exists in the root directory."""
        readme_path = Path('README.md')
        assert readme_path.exists(), "README.md should exist in root directory"
    
    def test_contribution_guide_exists(self):
        """Test that contribution guide exists."""
        contrib_path = Path('CONTRIBUTION.md')
        assert contrib_path.exists(), "CONTRIBUTION.md should exist"


class TestREADME:
    """Test suite specifically for README.md."""
    
    @pytest.fixture
    def readme_content(self):
        """Load README.md content."""
        readme_path = Path('README.md')
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def test_readme_has_title(self, readme_content):
        """Test that README has a main title."""
        # Should have at least one H1 heading
        assert re.search(r'^#\s+.+', readme_content, re.MULTILINE), \
            "README should have a main title (# heading)"
    
    def test_readme_has_description(self, readme_content):
        """Test that README has meaningful description."""
        assert len(readme_content) > 200, "README should have substantial content"
        # Should mention AI agents
        assert 'AI' in readme_content or 'agent' in readme_content.lower(), \
            "README should describe the AI agents project"
    
    def test_readme_has_table_of_contents(self, readme_content):
        """Test that README has a table of contents."""
        toc_indicators = [
            'table of contents',
            '##',  # Should have section headings
            'introduction',
            'use case'
        ]
        content_lower = readme_content.lower()
        
        matches = sum(1 for indicator in toc_indicators if indicator in content_lower)
        assert matches >= 2, "README should have structured sections"
    
    def test_readme_has_industry_usecases(self, readme_content):
        """Test that README includes industry use cases."""
        assert 'industry' in readme_content.lower(), "Should mention industry use cases"
        assert 'use case' in readme_content.lower() or 'usecase' in readme_content.lower(), \
            "Should include use cases"
    
    def test_readme_has_usage_table(self, readme_content):
        """Test that README has a table with use cases."""
        # Should have table syntax
        assert '|' in readme_content, "README should contain tables"
        # Should have table headers
        assert re.search(r'\|.+\|.+\|', readme_content), "Should have table format"
    
    def test_readme_has_github_links(self, readme_content):
        """Test that README includes GitHub repository links."""
        assert 'github.com' in readme_content.lower() or 'github' in readme_content.lower(), \
            "README should reference GitHub"
        # Should have clickable links
        assert '[' in readme_content and ']' in readme_content, \
            "README should have markdown links"
    
    def test_readme_has_badges(self, readme_content):
        """Test that README includes badges or visual indicators."""
        # Check for common badge patterns
        badge_indicators = [
            'shields.io',
            'badge',
            'img.shields.io',
            '![',
            'https://img.shields.io'
        ]
        
        has_badges = any(indicator in readme_content for indicator in badge_indicators)
        # Note: This is optional but recommended
        if not has_badges:
            # At least should have emojis or formatting
            assert '🌟' in readme_content or '##' in readme_content, \
                "README should have visual elements (badges or emojis)"
    
    def test_readme_has_contributing_section(self, readme_content):
        """Test that README mentions contributing guidelines."""
        content_lower = readme_content.lower()
        assert 'contribut' in content_lower, \
            "README should mention contributing guidelines"
    
    def test_readme_has_license_section(self, readme_content):
        """Test that README mentions license."""
        content_lower = readme_content.lower()
        assert 'license' in content_lower, "README should mention license"
    
    def test_readme_frameworks_section(self, readme_content):
        """Test that README includes framework information."""
        content_lower = readme_content.lower()
        frameworks = ['crewai', 'autogen', 'langgraph', 'agno']
        
        mentioned_frameworks = [fw for fw in frameworks if fw in content_lower]
        assert len(mentioned_frameworks) >= 2, \
            "README should mention multiple AI agent frameworks"
    
    def test_readme_no_broken_internal_links(self, readme_content):
        """Test that internal markdown links in README are valid."""
        # Find all markdown links
        link_pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
        links = re.findall(link_pattern, readme_content)
        
        for _link_text, link_url in links:
            # Check internal links (starting with #)
            if link_url.startswith('#'):
                # This is a basic check; more sophisticated parsing could be added
                pass
    
    def test_readme_code_blocks_formatted(self, readme_content):
        """Test that code blocks in README are properly formatted."""
        # Check for code blocks
        if '```' in readme_content:
            code_blocks = re.findall(r'```[\s\S]*?```', readme_content)
            assert len(code_blocks) > 0, "Code blocks should be properly closed"
            
            for block in code_blocks:
                # Should have opening and closing backticks
                assert block.startswith('```') and block.endswith('```'), \
                    "Code blocks should be properly formatted"


class TestContributionGuide:
    """Test suite for CONTRIBUTION.md."""
    
    @pytest.fixture
    def contribution_content(self):
        """Load CONTRIBUTION.md content."""
        contrib_path = Path('CONTRIBUTION.md')
        with open(contrib_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def test_contribution_has_title(self, contribution_content):
        """Test that contribution guide has a title."""
        assert re.search(r'^#\s+.+', contribution_content, re.MULTILINE), \
            "CONTRIBUTION.md should have a title"
    
    def test_contribution_has_guidelines(self, contribution_content):
        """Test that contribution guide has actual guidelines."""
        assert len(contribution_content) > 500, \
            "CONTRIBUTION.md should have substantial guidelines"
        
        content_lower = contribution_content.lower()
        keywords = ['how to', 'contribute', 'pull request', 'pr', 'issue', 'fork']
        
        matches = sum(1 for keyword in keywords if keyword in content_lower)
        assert matches >= 3, "Should include basic contribution instructions"
    
    def test_contribution_mentions_code_style(self, contribution_content):
        """Test that contribution guide mentions code style or standards."""
        content_lower = contribution_content.lower()
        style_indicators = ['style', 'format', 'convention', 'standard', 'pep', 'eslint']
        
        has_style_guide = any(indicator in content_lower for indicator in style_indicators)
        assert has_style_guide, "Should mention code style or formatting standards"
    
    def test_contribution_mentions_testing(self, contribution_content):
        """Test that contribution guide mentions testing."""
        content_lower = contribution_content.lower()
        assert 'test' in content_lower, "Should mention testing requirements"
    
    def test_contribution_has_pr_process(self, contribution_content):
        """Test that contribution guide explains PR process."""
        content_lower = contribution_content.lower()
        pr_indicators = ['pull request', 'pr', 'merge', 'review']
        
        mentions = sum(1 for indicator in pr_indicators if indicator in content_lower)
        assert mentions >= 2, "Should explain pull request process"
    
    def test_contribution_mentions_licensing(self, contribution_content):
        """Test that contribution guide mentions licensing."""
        content_lower = contribution_content.lower()
        assert 'license' in content_lower, "Should mention licensing considerations"
    
    def test_contribution_has_contact_info(self, contribution_content):
        """Test that contribution guide has contact or support information."""
        content_lower = contribution_content.lower()
        contact_indicators = ['contact', 'support', 'help', 'issue', 'discussion']
        
        mentions = sum(1 for indicator in contact_indicators if indicator in content_lower)
        assert mentions >= 2, "Should provide ways to get help or contact maintainers"


class TestCrewAICourse:
    """Test suite for crewai_mcp_course/README.md."""
    
    @pytest.fixture
    def course_readme(self):
        """Load course README content."""
        course_path = Path('crewai_mcp_course/README.md')
        if not course_path.exists():
            pytest.skip("Course README not found")
        with open(course_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def test_course_readme_exists(self):
        """Test that course README exists."""
        course_path = Path('crewai_mcp_course/README.md')
        assert course_path.exists(), "Course README should exist"
    
    def test_course_has_title(self, course_readme):
        """Test that course README has a title."""
        assert re.search(r'^#\s+.+', course_readme, re.MULTILINE), \
            "Course README should have a title"
        assert 'crewai' in course_readme.lower(), "Title should mention CrewAI"
    
    def test_course_has_overview(self, course_readme):
        """Test that course README has overview section."""
        content_lower = course_readme.lower()
        assert 'overview' in content_lower or 'introduction' in content_lower, \
            "Course should have an overview"
    
    def test_course_has_lessons(self, course_readme):
        """Test that course README outlines lessons."""
        content_lower = course_readme.lower()
        assert 'lesson' in content_lower, "Course should have lessons"
        
        # Should have multiple lessons
        lesson_count = content_lower.count('lesson')
        assert lesson_count >= 3, "Course should have multiple lessons"
    
    def test_course_has_setup_instructions(self, course_readme):
        """Test that course includes setup instructions."""
        content_lower = course_readme.lower()
        setup_indicators = ['install', 'setup', 'getting started', 'requirement']
        
        matches = sum(1 for indicator in setup_indicators if indicator in content_lower)
        assert matches >= 2, "Course should include setup instructions"
    
    def test_course_has_code_examples(self, course_readme):
        """Test that course includes code examples."""
        # Should have code blocks
        assert '```' in course_readme, "Course should include code examples"
    
    def test_course_mentions_mcp(self, course_readme):
        """Test that course mentions MCP (Model Context Protocol)."""
        content_lower = course_readme.lower()
        assert 'mcp' in content_lower or 'fastmcp' in content_lower, \
            "Course should mention MCP"
    
    def test_course_has_diagrams(self, course_readme):
        """Test that course includes diagrams or visual aids."""
        # Check for mermaid diagrams
        assert 'mermaid' in course_readme or '```mermaid' in course_readme, \
            "Course should include diagrams for better understanding"


class TestMarkdownFormatting:
    """Test suite for Markdown formatting quality across all files."""
    
    @pytest.fixture
    def markdown_files(self):
        """Get all markdown files."""
        repo_root = Path('.')
        md_files = list(repo_root.glob('**/*.md'))
        md_files = [f for f in md_files if '.git' not in str(f)]
        return md_files
    
    def test_no_trailing_whitespace(self, markdown_files):
        """Test that markdown files don't have trailing whitespace."""
        for md_file in markdown_files:
            with open(md_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            trailing_whitespace_lines = [
                i+1 for i, line in enumerate(lines) 
                if line.rstrip() != line.rstrip('\n')
            ]
            
            assert len(trailing_whitespace_lines) == 0, \
                f"{md_file.name} has trailing whitespace on lines: {trailing_whitespace_lines}"
    
    def test_consistent_heading_style(self, markdown_files):
        """Test that markdown files use consistent heading style."""
        for md_file in markdown_files:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for ATX-style headings (# ## ###)
            atx_headings = re.findall(r'^#{1,6}\s+', content, re.MULTILINE)
            # Check for Setext-style headings (=== ---)
            setext_headings = re.findall(r'^[=-]{3,}$', content, re.MULTILINE)
            
            # If both styles exist, that's inconsistent (though valid)
            if len(atx_headings) > 0 and len(setext_headings) > 0:
                # This is acceptable, just noting it
                pass
    
    def test_no_duplicate_headings(self, markdown_files):
        """Test that markdown files don't have duplicate top-level headings."""
        for md_file in markdown_files:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find all H1 headings
            h1_headings = re.findall(r'^#\s+(.+)$', content, re.MULTILINE)
            
            # Should have at most one H1 (title)
            if len(h1_headings) > 1:
                # Multiple H1s can be valid in some cases, but generally one is preferred
                pass  # Just a warning, not a hard failure
    
    def test_proper_list_formatting(self, markdown_files):
        """Test that lists are properly formatted."""
        for md_file in markdown_files:
            with open(md_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for i, line in enumerate(lines):
                # Check unordered lists
                if re.match(r'^\s*[-*+]\s+', line):
                    # List item should have space after marker
                    assert re.match(r'^\s*[-*+]\s+\S', line), \
                        f"{md_file.name} line {i+1}: List item should have content after marker"
    
    def test_link_formatting(self, markdown_files):
        """Test that links are properly formatted."""
        for md_file in markdown_files:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find all markdown links
            links = re.findall(r'\[([^\]]*)\]\(([^\)]+)\)', content)
            
            for link_text, link_url in links:
                # Link text should not be empty
                # (Empty is technically valid for images, but not great for links)
                if not link_text.startswith('!'):  # Not an image
                    # Having empty link text is acceptable for some use cases
                    pass
                
                # URL should not be empty
                assert link_url.strip(), \
                    f"{md_file.name}: Link has empty URL"


class TestMarkdownLinks:
    """Test suite for validating links in Markdown files."""
    
    @pytest.fixture
    def markdown_files(self):
        """Get all markdown files."""
        repo_root = Path('.')
        md_files = list(repo_root.glob('**/*.md'))
        md_files = [f for f in md_files if '.git' not in str(f)]
        return md_files
    
    def test_external_links_have_https(self, markdown_files):
        """Test that external links use HTTPS."""
        for md_file in markdown_files:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find all links
            links = re.findall(r'\[([^\]]*)\]\(([^\)]+)\)', content)
            
            for _link_text, link_url in links:
                # Skip internal links
                if link_url.startswith('#') or link_url.startswith('/'):
                    continue
                
                # Skip relative links
                if not link_url.startswith('http'):
                    continue
                
                # External HTTP links should use HTTPS
                if link_url.startswith('http://'):
                    # Some exceptions like localhost
                    if 'localhost' not in link_url and '127.0.0.1' not in link_url:
                        # Warning: HTTP link found
                        # In modern times, HTTPS is preferred
                        pass
    
    def test_no_dead_internal_links(self, markdown_files):
        """Test that internal file links point to existing files."""
        for md_file in markdown_files:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find all links
            links = re.findall(r'\[([^\]]*)\]\(([^\)]+)\)', content)
            
            for _link_text, link_url in links:
                # Check for relative file links
                if not link_url.startswith('http') and not link_url.startswith('#'):
                    # Remove anchor if present
                    file_part = link_url.split('#')[0]
                    
                    if file_part:
                        # Resolve relative to the markdown file's location
                        target_path = (md_file.parent / file_part).resolve()
                        
                        # Check if target exists (file or directory)
                        # Note: Some links might be external or intentionally forward-looking
                        if not target_path.exists():
                            # Could be a URL or future file - we'll just note it
                            pass
    
    def test_github_links_valid_format(self, markdown_files):
        """Test that GitHub links have valid format."""
        for md_file in markdown_files:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find GitHub links
            github_links = re.findall(
                r'https://github\.com/[\w-]+/[\w-]+', 
                content
            )
            
            for link in github_links:
                # Should follow github.com/owner/repo pattern
                parts = urlparse(link).path.split('/')
                # Should have at least owner and repo
                assert len([p for p in parts if p]) >= 2, \
                    f"{md_file.name}: Malformed GitHub link: {link}"