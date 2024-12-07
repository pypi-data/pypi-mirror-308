import logging
from ..pod_manager.pod_manager import PodManager
from ..varible_manager.path_manager import PathManager
from ..varible_manager.name_manager import NameManager

class IsolatedPodManager:
    """Class for handling isolated pod configurations and setup."""

    def __init__(self, isolation_config):
        self.isolation_config = isolation_config
        self.pod_manager = PodManager()
        self.path_manager = PathManager()
        self.name_manager = NameManager()

    def check_and_start_isolated_pod(self):
        """Check if isolation is enabled and start the pod if it is."""
        if self.isolation_config and self.isolation_config.get("enabled"):
            logging.info("Running in isolated mode.")
            self._start_isolated_pod()
        else:
            logging.info("Running in non-isolated mode.")

    def _start_isolated_pod(self, isolation_config: dict, library_names: list, host_mount_path:str, rebuild:str) -> None:
        """Start a pod in isolated mode."""
        try:
            pod_name = isolation_config.get("name", "isolated_pod").lower()
            version = isolation_config.get("version", "latest")
            base_image = isolation_config.get("base_image", "ubuntu:latest")
            commands = isolation_config.get("commands", [])
            working_dir = isolation_config.get("working_dir", "/app")
            volumes = []
            paths = []

            for lib_name in library_names:
                formatted_name = self.name_manager._format_library_name(lib_name)
                volume_str = f"-v {self.path_manager.get_volume_path(formatted_name, host_mount_path)}:{self.path_manager.get_mount_path(formatted_name, working_dir)} \\\n"
                volumes.append(volume_str)
                paths.append(self.path_manager.get_mount_path(formatted_name, working_dir))

            volumes_str = " ".join(volumes)

            env_command = f'PYTHONPATH="{":".join(paths)}"'
            result = [{"name": "ENV", "command": env_command}]
            commands = result + commands
            if all([pod_name, version, base_image]) and rebuild:
                self.pod_manager.build_pod(
                    library=None,
                    image_name=base_image,
                    working_dir=working_dir,
                    pod_name=f"{pod_name}:{version}",
                    commands=commands,
                )
                print(
                    f"You can work with the isolated pod:\ndocker run -it --name isolated-container {volumes_str} {pod_name}:{version} bash"
                )
                logging.info(
                    f"Isolated pod '{pod_name}:{version}' started successfully."
                )
            elif all([pod_name, version, base_image]) and not rebuild:
                print(
                    f"You can work with the isolated pod:\ndocker run -it --name isolated-container {volumes_str} {pod_name}:{version} bash"
                )
                logging.info(
                    f"Isolated pod '{pod_name}:{version}' already exists. Skipping build."
                )
            else:
                print(
                    f"docker run -it --name isolated-container {volumes_str} {pod_name}:{version} bash"
                )
                logging.error("Isolation configuration is missing required fields.")
        except Exception as e:
            logging.error(f"Error in isolation mode: {e}")
            raise
