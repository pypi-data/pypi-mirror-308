import os


class Scan:
    base_path = "."
    dir_to_search: str  # default ".cosmctl"
    max_depth: int  # default 1

    def __init__(self, dir_to_search=".cosmctl", max_depth=1):
        self.dir_to_search = dir_to_search
        self.max_depth = max_depth

    def is_subproject(self, base_path, target_dir_name):
        if not os.path.exists(base_path):
            return False

        try:
            for item in os.listdir(base_path):
                full_path = os.path.join(base_path, item)
                if os.path.isdir(full_path) and item == target_dir_name:
                    return True

            return False
        except PermissionError:
            # TODO log error Permission denied
            return False

    def recursively_find_dir(
        self, start_path, target_dir_name, found_dirs=[], current_depth=0
    ):
        if current_depth >= self.max_depth:
            return found_dirs

        for item in os.listdir(start_path):
            full_path = os.path.join(start_path, item)
            if os.path.isdir(full_path) and self.is_subproject(full_path, target_dir_name):
                # subdir recursive search
                subprojects = self.recursively_find_dir(
                    full_path, target_dir_name, found_dirs=[], current_depth=current_depth + 1
                )

                for subproject in subprojects:
                    found_dirs.append(subproject)
                found_dirs.append(full_path)
        return found_dirs

    def execute(self):
        cwd = os.getcwd()

        return self.recursively_find_dir(cwd, self.dir_to_search)
