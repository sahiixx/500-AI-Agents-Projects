"""
Test suite for validating GitHub Actions workflow files.

This module contains comprehensive tests for the Jekyll deployment workflow,
ensuring proper YAML syntax, required fields, and GitHub Actions best practices.
"""

import yaml
import pytest
from pathlib import Path


class TestGitHubActionsWorkflow:
    """Test suite for .github/workflows/jekyll-gh-pages.yml"""
    
    @pytest.fixture
    def workflow_file(self):
        """Load the workflow YAML file."""
        workflow_path = Path('.github/workflows/jekyll-gh-pages.yml')
        assert workflow_path.exists(), "Workflow file must exist"
        with open(workflow_path, 'r') as f:
            return yaml.safe_load(f)
    
    @pytest.fixture
    def workflow_content(self):
        """Load raw workflow content."""
        workflow_path = Path('.github/workflows/jekyll-gh-pages.yml')
        with open(workflow_path, 'r') as f:
            return f.read()
    
    def test_workflow_file_exists(self):
        """Test that the workflow file exists in the correct location."""
        workflow_path = Path('.github/workflows/jekyll-gh-pages.yml')
        assert workflow_path.exists(), "GitHub Actions workflow file should exist"
        assert workflow_path.is_file(), "Workflow should be a file, not a directory"
    
    def test_workflow_valid_yaml(self, workflow_file):
        """Test that the workflow file is valid YAML."""
        assert workflow_file is not None, "Workflow YAML should be parseable"
        assert isinstance(workflow_file, dict), "Workflow should be a dictionary"
    
    def test_workflow_has_name(self, workflow_file):
        """Test that workflow has a descriptive name."""
        assert 'name' in workflow_file, "Workflow must have a name"
        assert len(workflow_file['name']) > 0, "Workflow name should not be empty"
        assert 'Jekyll' in workflow_file['name'], "Workflow name should mention Jekyll"
    
    def test_workflow_has_triggers(self, workflow_file):
        """Test that workflow has proper trigger configuration."""
        assert 'on' in workflow_file, "Workflow must have 'on' triggers defined"
        triggers = workflow_file['on']
        
        # Should have push trigger
        assert 'push' in triggers or (isinstance(triggers, list) and 'push' in triggers), \
            "Workflow should trigger on push events"
        
        # Should have workflow_dispatch for manual triggering
        assert 'workflow_dispatch' in triggers or \
               (isinstance(triggers, list) and 'workflow_dispatch' in triggers), \
            "Workflow should support manual dispatch"
    
    def test_workflow_push_trigger_branches(self, workflow_file):
        """Test that push trigger targets correct branches."""
        triggers = workflow_file['on']
        if isinstance(triggers, dict) and 'push' in triggers:
            push_config = triggers['push']
            if 'branches' in push_config:
                branches = push_config['branches']
                assert isinstance(branches, list), "Branches should be a list"
                assert 'main' in branches, "Should trigger on main branch"
    
    def test_workflow_has_permissions(self, workflow_file):
        """Test that workflow has appropriate permissions configured."""
        assert 'permissions' in workflow_file, "Workflow should define permissions"
        permissions = workflow_file['permissions']
        
        # For GitHub Pages deployment
        assert 'contents' in permissions, "Should have contents permission"
        assert 'pages' in permissions, "Should have pages permission"
        assert 'id-token' in permissions, "Should have id-token permission"
        
        # Verify permission levels
        assert permissions['contents'] == 'read', "Contents should be read-only"
        assert permissions['pages'] == 'write', "Pages should have write permission"
        assert permissions['id-token'] == 'write', "ID token should have write permission"
    
    def test_workflow_has_concurrency(self, workflow_file):
        """Test that workflow has concurrency configuration."""
        assert 'concurrency' in workflow_file, "Workflow should define concurrency"
        concurrency = workflow_file['concurrency']
        
        assert 'group' in concurrency, "Concurrency should have a group"
        assert concurrency['group'] == 'pages', "Should use 'pages' concurrency group"
        
        assert 'cancel-in-progress' in concurrency, "Should define cancel-in-progress"
        assert concurrency['cancel-in-progress'] is False, \
            "Should not cancel in-progress deployments"
    
    def test_workflow_has_jobs(self, workflow_file):
        """Test that workflow has jobs defined."""
        assert 'jobs' in workflow_file, "Workflow must have jobs"
        jobs = workflow_file['jobs']
        assert len(jobs) > 0, "Workflow should have at least one job"
    
    def test_workflow_has_build_job(self, workflow_file):
        """Test that workflow has a build job."""
        jobs = workflow_file['jobs']
        assert 'build' in jobs, "Workflow should have a 'build' job"
        
        build_job = jobs['build']
        assert 'runs-on' in build_job, "Build job should specify runs-on"
        assert build_job['runs-on'] == 'ubuntu-latest', \
            "Build job should run on ubuntu-latest"
        
        assert 'steps' in build_job, "Build job should have steps"
        assert len(build_job['steps']) > 0, "Build job should have at least one step"
    
    def test_workflow_build_steps(self, workflow_file):
        """Test that build job has required steps."""
        build_steps = workflow_file['jobs']['build']['steps']
        step_names = [step.get('name', '') for step in build_steps]
        
        # Should checkout code
        assert any('Checkout' in name for name in step_names), \
            "Build should checkout the repository"
        
        # Should setup pages
        assert any('Setup Pages' in name or 'Pages' in name for name in step_names), \
            "Build should setup GitHub Pages"
        
        # Should build with Jekyll
        assert any('Jekyll' in name for name in step_names), \
            "Build should build with Jekyll"
        
        # Should upload artifact
        assert any('Upload' in name or 'artifact' in name for name in step_names), \
            "Build should upload artifact"
    
    def test_workflow_build_uses_official_actions(self, workflow_file):
        """Test that build job uses official GitHub Actions."""
        build_steps = workflow_file['jobs']['build']['steps']
        
        # Find actions used
        actions_used = [step.get('uses', '') for step in build_steps if 'uses' in step]
        
        # Should use official checkout action
        assert any('actions/checkout@v' in action for action in actions_used), \
            "Should use official checkout action"
        
        # Should use official pages actions
        assert any('actions/configure-pages@v' in action for action in actions_used), \
            "Should use official configure-pages action"
        
        assert any('actions/jekyll-build-pages@v' in action for action in actions_used), \
            "Should use official jekyll-build-pages action"
        
        assert any('actions/upload-pages-artifact@v' in action for action in actions_used), \
            "Should use official upload-pages-artifact action"
    
    def test_workflow_has_deploy_job(self, workflow_file):
        """Test that workflow has a deploy job."""
        jobs = workflow_file['jobs']
        assert 'deploy' in jobs, "Workflow should have a 'deploy' job"
        
        deploy_job = jobs['deploy']
        assert 'runs-on' in deploy_job, "Deploy job should specify runs-on"
        assert deploy_job['runs-on'] == 'ubuntu-latest', \
            "Deploy job should run on ubuntu-latest"
        
        assert 'needs' in deploy_job, "Deploy job should depend on other jobs"
        assert 'build' in deploy_job['needs'] or deploy_job['needs'] == 'build', \
            "Deploy should depend on build job"
    
    def test_workflow_deploy_environment(self, workflow_file):
        """Test that deploy job has proper environment configuration."""
        deploy_job = workflow_file['jobs']['deploy']
        
        assert 'environment' in deploy_job, "Deploy job should specify environment"
        environment = deploy_job['environment']
        
        if isinstance(environment, dict):
            assert 'name' in environment, "Environment should have a name"
            assert environment['name'] == 'github-pages', \
                "Should deploy to github-pages environment"
            
            assert 'url' in environment, "Environment should have a URL"
    
    def test_workflow_deploy_steps(self, workflow_file):
        """Test that deploy job has required steps."""
        deploy_job = workflow_file['jobs']['deploy']
        
        assert 'steps' in deploy_job, "Deploy job should have steps"
        deploy_steps = deploy_job['steps']
        assert len(deploy_steps) > 0, "Deploy job should have at least one step"
        
        # Should use deploy-pages action
        actions_used = [step.get('uses', '') for step in deploy_steps if 'uses' in step]
        assert any('actions/deploy-pages@v' in action for action in actions_used), \
            "Should use official deploy-pages action"
    
    def test_workflow_no_syntax_errors(self, workflow_content):
        """Test that workflow has no common YAML syntax errors."""
        # Check for common issues
        assert '\t' not in workflow_content, "Should not contain tabs (use spaces)"
        
        # Check for proper indentation (should be 2 spaces for YAML)
        lines = workflow_content.split('\n')
        for i, line in enumerate(lines, 1):
            if line.strip() and not line.startswith('#'):
                # Count leading spaces
                leading_spaces = len(line) - len(line.lstrip())
                if leading_spaces > 0:
                    assert leading_spaces % 2 == 0, \
                        f"Line {i} has inconsistent indentation (should be multiples of 2)"
    
    def test_workflow_has_comments(self, workflow_content):
        """Test that workflow has helpful comments."""
        assert '#' in workflow_content, "Workflow should have comments for clarity"
        comment_lines = [line for line in workflow_content.split('\n') if line.strip().startswith('#')]
        assert len(comment_lines) >= 3, "Should have multiple explanatory comments"
    
    def test_workflow_version_pinning(self, workflow_file):
        """Test that actions are pinned to specific versions."""
        all_jobs = workflow_file['jobs']
        
        for job_name, job in all_jobs.items():
            if 'steps' in job:
                for step in job['steps']:
                    if 'uses' in step:
                        action = step['uses']
                        assert '@' in action, \
                            f"Action '{action}' in job '{job_name}' should be pinned to a version"
                        assert '@v' in action.lower() or '@sha' in action.lower(), \
                            f"Action '{action}' should use version tag or SHA"


class TestWorkflowFileQuality:
    """Test suite for workflow file quality and best practices."""
    
    def test_workflow_file_size(self):
        """Test that workflow file is not excessively large."""
        workflow_path = Path('.github/workflows/jekyll-gh-pages.yml')
        file_size = workflow_path.stat().st_size
        assert file_size < 10000, "Workflow file should be under 10KB"
        assert file_size > 100, "Workflow file should have meaningful content"
    
    def test_workflow_line_length(self):
        """Test that workflow lines are not excessively long."""
        workflow_path = Path('.github/workflows/jekyll-gh-pages.yml')
        with open(workflow_path, 'r') as f:
            lines = f.readlines()
        
        long_lines = [i+1 for i, line in enumerate(lines) if len(line) > 120]
        assert len(long_lines) == 0, \
            f"Lines {long_lines} exceed 120 characters. Consider breaking them up."
    
    def test_workflow_no_secrets_exposed(self):
        """Test that workflow doesn't contain hardcoded secrets."""
        workflow_path = Path('.github/workflows/jekyll-gh-pages.yml')
        with open(workflow_path, 'r') as f:
            content = f.read().lower()
        
        # Common secret patterns to avoid
        forbidden_patterns = [
            'password:',
            'api_key:',
            'secret:',
            'token:',
            'ghp_',
            'github_token:',
        ]
        
        for pattern in forbidden_patterns:
            if pattern in content:
                # Check if it's properly using secrets
                assert 'secrets.' in content or '${{' in content, \
                    f"Potential hardcoded secret detected: {pattern}"


class TestWorkflowIntegration:
    """Test suite for workflow integration and compatibility."""
    
    def test_workflow_compatible_with_github_pages(self):
        """Test that workflow is compatible with GitHub Pages."""
        workflow_path = Path('.github/workflows/jekyll-gh-pages.yml')
        with open(workflow_path, 'r') as f:
            content = f.read()
        
        # Should mention pages or Jekyll
        assert 'pages' in content.lower() or 'jekyll' in content.lower(), \
            "Workflow should be related to GitHub Pages or Jekyll"
    
    def test_workflow_directory_structure(self):
        """Test that workflow directory structure is correct."""
        workflows_dir = Path('.github/workflows')
        assert workflows_dir.exists(), "Workflows directory should exist"
        assert workflows_dir.is_dir(), "Workflows should be a directory"
        
        # Check for proper permissions (on Unix-like systems)
        import os
        if hasattr(os, 'access'):
            assert os.access(workflows_dir, os.R_OK), "Workflows directory should be readable"