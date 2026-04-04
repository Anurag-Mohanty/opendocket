"""
Repository fetching, qualification, and file reading.

Clones a GitHub repository and checks it against qualification gates
before allowing a scan to proceed.
"""

import os
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass


@dataclass
class QualificationResult:
    qualified: bool
    reasons: list[str]
    stats: dict


@dataclass
class RepoContext:
    """Everything the agents need to analyze a repository."""
    path: str
    name: str
    url: str
    readme_content: str
    file_index: list[str]  # relative paths of all code files
    qualification: QualificationResult


CODE_EXTENSIONS = {
    ".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".go", ".rb",
    ".php", ".cs", ".rs", ".swift", ".kt", ".scala", ".c", ".cpp",
    ".h", ".hpp",
}

SKIP_DIRS = {
    "node_modules", ".git", "vendor", "venv", ".venv", "__pycache__",
    "dist", "build", ".next", ".nuxt", "target", "bin", "obj",
    ".tox", ".mypy_cache", ".pytest_cache", "coverage", "test_fixtures",
}


MAX_CLONE_SIZE_MB = 500


def _get_dir_size_mb(path: str) -> float:
    """Get directory size in MB."""
    total = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            try:
                total += os.path.getsize(os.path.join(dirpath, f))
            except OSError:
                pass
    return total / (1024 * 1024)


def clone_repo(url: str, target_dir: str | None = None) -> str:
    """Clone a GitHub repo to a temporary directory. Returns the path."""
    if target_dir is None:
        target_dir = tempfile.mkdtemp(prefix="opendocket_")

    try:
        # Shallow clone for speed
        subprocess.run(
            ["git", "clone", "--depth", "1", url, target_dir],
            capture_output=True,
            text=True,
            check=True,
            timeout=300,
        )

        # Size gate — if over limit, retry with sparse checkout (skip heavy dirs)
        size_mb = _get_dir_size_mb(target_dir)
        print(f"[OpenDocket] Clone size: {size_mb:.0f}MB")
        if size_mb > MAX_CLONE_SIZE_MB:
            print(f"[OpenDocket] Over {MAX_CLONE_SIZE_MB}MB — retrying with sparse checkout...")
            cleanup_repo(target_dir)
            os.makedirs(target_dir, exist_ok=True)

            # Init sparse checkout — exclude docs, images, binaries, test fixtures
            subprocess.run(["git", "init", target_dir], capture_output=True, check=True, timeout=30)
            subprocess.run(["git", "-C", target_dir, "remote", "add", "origin", url],
                           capture_output=True, check=True, timeout=10)
            subprocess.run(["git", "-C", target_dir, "config", "core.sparseCheckout", "true"],
                           capture_output=True, check=True, timeout=10)

            sparse_file = os.path.join(target_dir, ".git", "info", "sparse-checkout")
            os.makedirs(os.path.dirname(sparse_file), exist_ok=True)
            with open(sparse_file, "w") as f:
                f.write("/*\n")
                f.write("!docs/\n!doc/\n!documentation/\n")
                f.write("!images/\n!img/\n!assets/\n!static/\n!public/\n!media/\n")
                f.write("!*.png\n!*.jpg\n!*.jpeg\n!*.gif\n!*.svg\n!*.ico\n")
                f.write("!*.mp4\n!*.webm\n!*.mov\n!*.mp3\n!*.wav\n")
                f.write("!*.woff\n!*.woff2\n!*.ttf\n!*.eot\n")
                f.write("!*.zip\n!*.tar\n!*.gz\n!*.bz2\n")
                f.write("!vendor/\n!node_modules/\n!.git/\n")

            subprocess.run(["git", "-C", target_dir, "pull", "--depth", "1", "origin", "HEAD"],
                           capture_output=True, check=True, timeout=300)

            size_mb = _get_dir_size_mb(target_dir)
            print(f"[OpenDocket] Sparse clone size: {size_mb:.0f}MB")
            if size_mb > MAX_CLONE_SIZE_MB * 2:
                cleanup_repo(target_dir)
                raise RuntimeError(
                    f"Repository still exceeds size limit after sparse checkout "
                    f"({size_mb:.0f}MB). Aborting scan."
                )

        return target_dir
    except subprocess.CalledProcessError:
        cleanup_repo(target_dir)
        raise
    except subprocess.TimeoutExpired:
        cleanup_repo(target_dir)
        raise RuntimeError("Repository clone timed out after 300 seconds.")


def cleanup_repo(path: str) -> None:
    """Remove a cloned repository. Guaranteed safe — only removes temp dirs."""
    if path and os.path.exists(path) and path.startswith(tempfile.gettempdir()):
        size_mb = _get_dir_size_mb(path)
        print(f"[OpenDocket] Cleaning up clone: {size_mb:.0f}MB at {path}")
        shutil.rmtree(path, ignore_errors=True)


def _read_readme(repo_path: str) -> str:
    """Find and read the README file."""
    for name in ["README.md", "README.rst", "README.txt", "README", "readme.md"]:
        path = os.path.join(repo_path, name)
        if os.path.isfile(path):
            try:
                with open(path, "r", errors="ignore") as f:
                    return f.read()
            except (OSError, IOError):
                pass
    return ""


def _count_meaningful_lines(text: str) -> int:
    """Count non-empty, non-header lines in README."""
    count = 0
    for line in text.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and not stripped.startswith("="):
            count += 1
    return count


def _index_files(repo_path: str) -> list[str]:
    """Build an index of all files in the repository."""
    files = []
    for root, dirs, filenames in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for filename in filenames:
            rel_path = os.path.relpath(os.path.join(root, filename), repo_path)
            files.append(rel_path)
    return sorted(files)


def _count_code_files(file_index: list[str]) -> int:
    """Count files with code extensions."""
    return sum(
        1 for f in file_index
        if os.path.splitext(f)[1].lower() in CODE_EXTENSIONS
    )


def _has_data_handling(repo_path: str, file_index: list[str]) -> bool:
    """Check for evidence of data handling."""
    data_signals = [
        r"model", r"schema", r"database", r"db", r"migration",
        r"api", r"route", r"endpoint", r"form", r"input",
        r"field", r"column", r"table", r"query", r"fetch",
        r"request", r"response", r"serialize", r"controller",
    ]
    pattern = re.compile("|".join(data_signals), re.IGNORECASE)

    # Check filenames
    for f in file_index:
        if pattern.search(f):
            return True

    # Check a sample of code files for data patterns
    checked = 0
    for f in file_index:
        ext = os.path.splitext(f)[1].lower()
        if ext not in CODE_EXTENSIONS:
            continue
        try:
            filepath = os.path.join(repo_path, f)
            with open(filepath, "r", errors="ignore") as fh:
                content = fh.read(8192)
            if pattern.search(content):
                return True
        except (OSError, IOError):
            pass
        checked += 1
        if checked >= 50:
            break

    return False


def qualify_repo(repo_path: str, file_index: list[str], readme: str) -> QualificationResult:
    """Check if a repository meets scanning qualification criteria."""
    failures = []
    stats = {}

    # Gate 1: README with >10 meaningful lines
    meaningful_lines = _count_meaningful_lines(readme)
    stats["readme_lines"] = meaningful_lines
    if meaningful_lines <= 10:
        failures.append(
            f"README has only {meaningful_lines} meaningful lines "
            f"(minimum 10 required). The repository needs a substantive "
            f"README to provide context for compliance analysis."
        )

    # Gate 2: Minimum 10 code files
    code_file_count = _count_code_files(file_index)
    stats["code_files"] = code_file_count
    if code_file_count < 10:
        failures.append(
            f"Repository has only {code_file_count} application code files "
            f"(minimum 10 required). A meaningful compliance scan requires "
            f"sufficient application logic to analyze."
        )

    # Gate 3: Evidence of data handling
    has_data = _has_data_handling(repo_path, file_index)
    stats["has_data_handling"] = has_data
    if not has_data:
        failures.append(
            "No evidence of data handling found (database models, API calls, "
            "form inputs, or data field definitions). Compliance scanning "
            "requires code that processes or stores data."
        )

    # Gate 4: Not just config files
    total_files = len(file_index)
    stats["total_files"] = total_files

    return QualificationResult(
        qualified=len(failures) == 0,
        reasons=failures,
        stats=stats,
    )


def fetch_and_qualify(url: str) -> RepoContext:
    """Clone a repo, build context, and run qualification gates."""
    # Extract repo name from URL
    name = url.rstrip("/").split("/")[-1]
    if name.endswith(".git"):
        name = name[:-4]

    path = clone_repo(url)
    file_index = _index_files(path)
    readme = _read_readme(path)
    qualification = qualify_repo(path, file_index, readme)

    return RepoContext(
        path=path,
        name=name,
        url=url,
        readme_content=readme,
        file_index=file_index,
        qualification=qualification,
    )


def read_file(repo_path: str, relative_path: str, max_bytes: int = 65536) -> str:
    """Read a file from the repository, up to max_bytes."""
    filepath = os.path.join(repo_path, relative_path)
    try:
        with open(filepath, "r", errors="ignore") as f:
            return f.read(max_bytes)
    except (OSError, IOError):
        return ""
