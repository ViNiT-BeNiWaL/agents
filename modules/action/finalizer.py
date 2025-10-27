import os
import shutil


class Finalizer:
    """
    Packages the final project files into a distributable zip archive.
    """

    def package_project(self, project_path, output_filename):
        """
        Creates a zip archive of the completed project directory.
        """
        try:
            # The archive will be saved in the `projects` directory, alongside the project folder
            archive_path_base = os.path.join(os.path.dirname(project_path), output_filename)

            print(f"Packaging project from '{project_path}' into '{archive_path_base}.zip'")
            shutil.make_archive(archive_path_base, 'zip', project_path)

            print(f" -> Project successfully packaged.")
            return f"{archive_path_base}.zip"
        except Exception as e:
            print(f" -> Error during project packaging: {e}")
            return None