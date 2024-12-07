import subprocess
import random

def default(ports=None, count=1, shuffle=True):
    """
    Finds the specified number of available ports from a given list of ports or port ranges 
    on the local machine using platform-specific commands.

    Args:
        ports (list[int | tuple[int, int]], optional): List of specific ports or ranges to check for availability.
            If a range is specified as (min, max), ports within that range are checked. Defaults to [(32767, 65535)].
        count (int, optional): The number of available ports to find. Defaults to 1.
        shuffle (bool, optional): Whether to shuffle the order of the ports before checking. Defaults to True.

    Returns:
        list[int]: A list of available port numbers. The list length matches the specified count or fewer 
                   if not enough available ports are found.
    """
    if ports is None:
        ports = [(32767, 65535)]

    is_windows = subprocess.os.name == 'nt'

    # Flatten ports to individual port numbers
    ports_to_check = []
    for port in ports:
        if isinstance(port, (tuple, list)) and len(port) == 2:
            ports_to_check.extend(range(port[0], port[1] + 1))
        else:
            ports_to_check.append(port)

    # Shuffle ports if required
    if shuffle:
        random.shuffle(ports_to_check)

    def is_port_available(port):
        """
        Helper function to check if a single port is available.

        Args:
            port (int): Port number to check.

        Returns:
            bool: True if the port is available, False otherwise.
        """
        command = (
            f"netstat -ano | findstr :{port}" if is_windows 
            else f"lsof -i :{port}"
        )
        try:
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return result.stdout.strip() == b""
        except Exception:
            return False

    # List to store available ports
    available_ports = []

    # Check each port until the desired count is reached
    for port in ports_to_check:
        if is_port_available(port):
            available_ports.append(port)
            if len(available_ports) == count:
                break

    return available_ports

# if __name__ == "__main__":
#     print(default())  # Example usage: Find a single available port in the default range
#     print(default(ports=[(1024, 49151)], count=5))  # Find 5 available ports in the range 1024-49151