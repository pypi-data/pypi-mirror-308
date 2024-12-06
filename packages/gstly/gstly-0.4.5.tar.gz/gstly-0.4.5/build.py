import multiprocessing
from pathlib import Path
from typing import List
import subprocess
import tempfile
import shutil
import platform

# This import must be run before Cython imports to avoid an AttributeError
from setuptools import Extension, Distribution

from Cython.Build import cythonize
from Cython.Distutils.build_ext import new_build_ext as cython_build_ext

SOURCE_DIR = Path("gstly")
BUILD_DIR = Path("cython_build")
C_EXTENSIONS_DIR = Path("extensions")
EXCLUDED_FILES = []
THREAD_COUNT = multiprocessing.cpu_count() * 2

# https://github.com/cython/cython/issues/2968
CYTHONIZE_INIT = True


def build() -> None:
    # Collect and cythonize all files
    extension_modules = cythonize_helper(get_extension_modules())

    # Use setuptools to collect files
    distribution = Distribution(
        {"ext_modules": extension_modules, "cmdclass": {"build_ext": cython_build_ext}}
    )

    # Grab the build_ext command and copy all files back to source dir. This is
    # done so that Poetry grabs the files during the next step in its build.
    distribution.run_command("build_ext")
    build_ext_cmd = distribution.get_command_obj("build_ext")
    build_ext_cmd.copy_extensions_to_source()

    build_c_extensions()


def build_c_extensions():
    """Builds all hand-written C extensions in the extensions folder"""
    for extension_path in C_EXTENSIONS_DIR.iterdir():
        print(f"Building C extension {extension_path.name}...")

        with tempfile.TemporaryDirectory() as build_dir:
            subprocess.run(
                ["meson", "setup", build_dir], cwd=extension_path, check=True
            )
            subprocess.run(["ninja"], cwd=Path(build_dir), check=True)

            platform_system = platform.system()
            suffix = "so" if platform.system() == "Linux" else "dll"
            glob = f"{extension_path.name}*.{suffix}"

            try:
                print(f"Building {glob} for {platform_system}")
                shared_library = next(Path(build_dir).glob(glob))
            except StopIteration:
                raise RuntimeError(
                    f"Missing shared library file for extension {extension_path.name}"
                )
            shutil.copy2(shared_library, Path("gstly/utils"))


def get_extension_modules() -> List[Extension]:
    """Collect all .py files and turn them into Setuptools Extensions"""
    extension_modules: List[Extension] = []

    for py_file in SOURCE_DIR.rglob("*.py"):
        if py_file.name == "__init__.py" and not CYTHONIZE_INIT:
            continue

        if py_file not in EXCLUDED_FILES:
            # Get path (not just name) without .py extension
            module_path = py_file.with_suffix("").as_posix()

            # Convert path to module name
            module_name = str(module_path).replace("/", ".")

            extension_module = Extension(name=module_name, sources=[str(py_file)])

            extension_modules.append(extension_module)

    return extension_modules


def cythonize_helper(extension_modules: List[Extension]) -> List[Extension]:
    """Cythonize all Python extensions"""
    return cythonize(
        extension_modules,
        # Don't build in source tree (this leaves behind .c files)
        build_dir=BUILD_DIR,
        # No .html output file
        annotate=False,
        # Parallel build
        nthreads=THREAD_COUNT,
        # Python 3
        compiler_directives={"language_level": "3"},
        # Always rebuild, even if file untouched
        force=True,
    )


if __name__ == "__main__":
    build()
