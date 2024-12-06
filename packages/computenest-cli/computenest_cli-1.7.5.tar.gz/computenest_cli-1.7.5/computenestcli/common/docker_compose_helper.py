import os
import yaml
from computenestcli.base_log import get_developer_logger
from computenestcli.base_log import get_user_logger
from computenestcli.common import project_setup_constant

developer_logger = get_developer_logger()
user_logger = get_user_logger()


class DockerComposeHelper:
    def __init__(self):
        pass

    # 生成替换.env中指定参数的值的sed命令与echo命令
    @staticmethod
    def generate_sed_commands(custom_parameters, docker_compose_path):
        commands = []

        # 解析 docker-compose.yaml 获取 env_file 引用
        with open(docker_compose_path, 'r') as stream:
            try:
                compose_data = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                user_logger.info(f"Error parsing YAML file: {exc}")
                return []

        # 获取 docker-compose 中所有的 env_file 路径
        env_files = set()
        docker_compose_dir = os.path.dirname(docker_compose_path)
        for service in compose_data.get('services', {}).values():
            env_file_in_service = service.get('env_file', [])
            if isinstance(env_file_in_service, str):
                env_file_in_service = [env_file_in_service]
            for env_file in env_file_in_service:
                env_files.add(os.path.join(docker_compose_dir, env_file))

        # 如果 docker-compose.yaml 中没有指定env_file，但用户指定了一个env文件，那么默认会采用.env文件
        default_env_path = os.path.join(docker_compose_dir, '.env')
        if not env_files:
            env_files.add(default_env_path)

        for env_file_path in env_files:
            # 检查文件是否存在，不存在则创建
            env_abs_path = os.path.abspath(env_file_path)
            directory = os.path.dirname(env_abs_path)
            os.makedirs(directory, exist_ok=True)
            env_content = ''
            if os.path.exists(env_abs_path):
                with open(env_abs_path, 'r') as file:
                    env_content = file.read()

            # DockerCompose 相关文件在 ROS 模板中的实际路径
            docker_compose_env_path = f'{project_setup_constant.DOCKER_COMPOSE_DIR}{os.path.relpath(env_file_path, os.getcwd())}'

            for param in custom_parameters:
                name = param.get("Name")
                if name:
                    variable_pattern = f"{name}="
                    # 如果变量存在则替换
                    if variable_pattern in env_content:
                        command = f"sed -i 's/{variable_pattern}[^\\n]*/{variable_pattern}${{{name}}}/' {docker_compose_env_path}"
                        commands.append(command)
                    elif env_file_path == default_env_path:
                        # 如果变量不存在则添加到.env文件中
                        command = f"echo '{name}=${{{name}}}' >> {docker_compose_env_path}"
                        commands.append(command)

        return commands

    @staticmethod
    def parse_docker_compose_ports(docker_compose_path, docker_compose_env_path):
        """
        解析 docker-compose 文件以提取端口信息。

        此方法读取 docker-compose YAML 文件，并提取每个服务定义的端口。
        将端口分为需要开放的端口（带协议）和可以通过 IP 和端口直接访问的端口（仅 TCP）。

        返回:
            tuple: 包含两个列表的元组：
                - ports_to_open: 每个元素是一个元组，包含端口和协议（例如，('8080', 'tcp')）。
                - service_ports: 可以使用 IP 和端口访问的 TCP 端口列表（例如，['8080']）。

        异常:
            FileNotFoundError: 如果 docker-compose 文件路径无效或找不到该文件。

        备注:
            - 如果端口未指定协议，默认假定为 TCP。
            - 处理各种端口表示法，包括：
                - 单个端口（例如，"3000"）
                - 映射端口（例如，"8000:8080"）
                - 主机特定端口（例如，"127.0.0.1:8001:8001"）
                - 指定协议的端口（例如，"50000:50000/tcp"）
        """
        if not os.path.isabs(docker_compose_path):
            docker_compose_path = os.path.abspath(docker_compose_path)
        with open(docker_compose_path, 'r') as file:
            compose_content = yaml.safe_load(file)

        env_dict = DockerComposeHelper.parse_docker_compose_env(docker_compose_env_path)

        ports_to_open = []
        service_ports = []

        services = compose_content.get('services', {})
        for service_name, service_data in services.items():
            service_ports_list = service_data.get('ports', [])

            for port in service_ports_list:
                protocol = 'tcp'  # 默认协议为 tcp

                if isinstance(port, str) or isinstance(port, int):
                    port_str = str(port)
                    parts = port_str.split(':')

                    if len(parts) == 1:  # "3000"
                        host_port = container_port = parts[0]
                    elif len(parts) == 2:  # "8000:8000", "49100:22"
                        host_port, container_port = parts
                    elif len(parts) == 3:  # "127.0.0.1:8001:8001"
                        _, host_port, container_port = parts
                    else:
                        raise ValueError(f"Invalid port format: {port}")

                    if '/' in container_port:  # "50000:50000/tcp"
                        container_port, protocol = container_port.split('/')

                elif isinstance(port, dict):
                    host_port = str(port.get('published', port.get('target')))
                    protocol = port.get('protocol', 'tcp')
                else:
                    raise ValueError(f"Invalid port format: {port}")

                # 如果host_port是${xxx}这样的格式，则需要从环境变量中获取
                if host_port.startswith('$'):
                    if not os.path.exists(docker_compose_env_path):
                        raise FileNotFoundError(f"Docker compose env path '{docker_compose_env_path}' does not exist.")
                    host_port = env_dict.get(host_port[2:-1])
                ports_to_open.append((host_port, protocol))

                # 默认认为未标明协议的情况为 TCP
                if protocol == 'tcp':
                    service_ports.append(host_port)

        return ports_to_open, service_ports

    # 读取docker compose环境变量文件，并将其中的键值对返回
    @staticmethod
    def parse_docker_compose_env(docker_compose_env_path):
        env_vars = {}
        if not docker_compose_env_path:
            return env_vars
        if not os.path.isabs(docker_compose_env_path):
            docker_compose_env_path = os.path.abspath(docker_compose_env_path)
        if os.path.exists(docker_compose_env_path):
            with open(docker_compose_env_path, 'r') as file:
                for line in file:
                    # 去除空白和换行
                    line = line.strip()
                    # 忽略注释行
                    if line.startswith('#') or not line:
                        continue
                    # 分割键值对
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
            return env_vars
        return {}
