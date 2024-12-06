import os
import re
import shutil
import tempfile
import yaml

from pathlib import Path
from importlib import resources
from computenestcli.processor.jinja2 import Jinja2Processor
from computenestcli.common import project_setup_constant, constant
from computenestcli.common.artifact_source_type import ArtifactSourceType
from computenestcli.common.arch import Arch
from computenestcli.common.service_type import ServiceType
from computenestcli.service.credentials import CredentialsService

from computenestcli.base_log import get_developer_logger
from computenestcli.base_log import get_user_logger
from dockerfile_parse import DockerfileParser

developer_logger = get_developer_logger()
user_logger = get_user_logger()


def _get_replaced_file_name(file_name):
    base, ext = os.path.splitext(file_name)
    return f"{base}-replaced{ext}"


class ProjectSetup:
    def __init__(self, output_base_path, parameters, replace_image=False,
                 context=None):
        self.output_base_path = Path(output_base_path).absolute()
        # 检查将Parameters中的RepoName，并修改为符合正则表达式的RepoName
        repo_name = parameters.get(project_setup_constant.REPO_NAME_KEY)
        if not repo_name:
            repo_name = project_setup_constant.APP_NAME
        else:
            repo_name = self._sanitize_name(repo_name)
        parameters[project_setup_constant.REPO_NAME_KEY] = repo_name
        self.parameters = parameters
        self.processor = Jinja2Processor()
        self.replace_image = replace_image
        self.context = context

    def setup_project(self):
        user_logger.info("Setting up the project...")
        self._validate_parameters()
        self._handle_source_code_packaging()
        self._render_templates()
        self._copy_resources()
        user_logger.info("Project setup complete.")

    def _validate_parameters(self):
        user_logger.info("Validating parameters...")
        artifact_source_type = self.parameters.get(project_setup_constant.ARTIFACT_SOURCE_TYPE_KEY)
        if artifact_source_type not in [ArtifactSourceType.SOURCE_CODE.value, ArtifactSourceType.INSTALL_PACKAGE.value,
                                        ArtifactSourceType.DOCKERFILE.value, ArtifactSourceType.HELM_CHART.value,
                                        ArtifactSourceType.DOCKER_COMPOSE.value]:
            raise Exception("Invalid artifact source type.")
        if artifact_source_type == ArtifactSourceType.SOURCE_CODE.value:
            source_code_path = self.parameters.get(project_setup_constant.SOURCE_CODE_PATH_KEY)
            if not source_code_path:
                raise Exception("Source code path is empty.")
            if not os.path.exists(source_code_path):
                raise Exception(f"Source code path:{source_code_path} does not exist.")
        if artifact_source_type == ArtifactSourceType.INSTALL_PACKAGE.value:
            package_path = self.parameters.get(project_setup_constant.PACKAGE_PATH_KEY)
            if not package_path:
                raise Exception("Package path is empty.")
            if not os.path.exists(package_path):
                raise Exception(f"Package path:{package_path} does not exist.")
            if not os.path.isfile(package_path):
                raise Exception(f"Package path:{package_path} is not a file.")
        if artifact_source_type == ArtifactSourceType.DOCKERFILE.value:
            dockerfile_path = self.parameters.get(project_setup_constant.DOCKERFILE_PATH_KEY)
            if not dockerfile_path:
                raise Exception("Dockerfile path is empty.")
            if not os.path.exists(dockerfile_path):
                raise Exception(f"Dockerfile path:{dockerfile_path} does not exist.")
        if artifact_source_type == ArtifactSourceType.DOCKER_COMPOSE.value:
            docker_compose_path = self.parameters.get(project_setup_constant.DOCKER_COMPOSE_PATH_KEY)
            if not docker_compose_path:
                raise Exception("Docker compose path is empty.")
            if not os.path.exists(docker_compose_path):
                raise Exception(f"Docker compose path:{docker_compose_path} does not exist.")
            docker_compose_env_path = self.parameters.get(project_setup_constant.DOCKER_COMPOSE_ENV_PATH_KEY)
            if not docker_compose_env_path:
                return
            if not os.path.exists(docker_compose_env_path):
                user_logger.error(f"Docker compose env path:{docker_compose_env_path} does not exist.")

    def _create_directories(self):
        user_logger.info("Creating necessary directories...")
        necessary_dirs = [project_setup_constant.OUTPUT_DOCS_DIR,
                          project_setup_constant.OUTPUT_ROS_TEMPLATE_DIR,
                          project_setup_constant.OUTPUT_ICON_DIR]

        for directory in necessary_dirs:
            Path(self.output_base_path, directory).mkdir(parents=True, exist_ok=True)

        artifact_source_type = self.parameters.get(project_setup_constant.ARTIFACT_SOURCE_TYPE_KEY)

        # 创建特定于软件形态的目录
        map_artifact_to_dir = {
            ArtifactSourceType.INSTALL_PACKAGE.value: project_setup_constant.OUTPUT_PACKAGE_DIR,
            ArtifactSourceType.SOURCE_CODE.value: project_setup_constant.OUTPUT_PACKAGE_DIR,
            ArtifactSourceType.DOCKERFILE.value: project_setup_constant.OUTPUT_DOCKERFILE_DIR,
            ArtifactSourceType.DOCKER_COMPOSE.value: project_setup_constant.OUTPUT_DOCKER_COMPOSE_DIR,
            ArtifactSourceType.HELM_CHART.value: project_setup_constant.OUTPUT_HELM_CHART_DIR
        }

        if artifact_source_type in map_artifact_to_dir:
            Path(self.output_base_path, map_artifact_to_dir[artifact_source_type]).mkdir(parents=True, exist_ok=True)
            user_logger.info(
                f"Created {map_artifact_to_dir[artifact_source_type]} directory at {self.output_base_path}.")

    def _render_templates(self):
        user_logger.info("Rendering ros_templates...")
        self._create_directories()
        artifact_source_type = self.parameters.get(project_setup_constant.ARTIFACT_SOURCE_TYPE_KEY)
        architecture = self.parameters.get(project_setup_constant.ARCHITECTURE_KEY, Arch.ECS_SINGLE.value)
        user_logger.info(f"Artifact source type: {artifact_source_type}")

        template_paths = {
            ArtifactSourceType.SOURCE_CODE.value: (
                project_setup_constant.INPUT_SOURCE_CODE_ROS_TEMPLATE_NAME,
                project_setup_constant.INPUT_SOURCE_CODE_CONFIG_NAME
            ),
            ArtifactSourceType.INSTALL_PACKAGE.value: (
                project_setup_constant.INPUT_INSTALL_PACKAGE_ROS_TEMPLATE_NAME,
                project_setup_constant.INPUT_INSTALL_PACKAGE_CONFIG_NAME
            ),
            ArtifactSourceType.DOCKERFILE.value: (
                project_setup_constant.INPUT_DOCKERFILE_ROS_TEMPLATE_NAME,
                project_setup_constant.INPUT_DOCKERFILE_CONFIG_NAME
            ),
            ArtifactSourceType.DOCKER_COMPOSE.value: (
                project_setup_constant.INPUT_DOCKER_COMPOSE_ROS_TEMPLATE_NAME,
                project_setup_constant.INPUT_DOCKER_COMPOSE_CONFIG_NAME
            ),
            ArtifactSourceType.HELM_CHART.value: (
                project_setup_constant.INPUT_HELM_CHART_ROS_TEMPLATE_NAME,
                project_setup_constant.INPUT_HELM_CHART_CONFIG_NAME
            ),
        }

        if artifact_source_type in template_paths:
            input_ros_template_name, input_config_name = template_paths[artifact_source_type]
            user_logger.info(f"Rendering ros_templates for {artifact_source_type}...")
        else:
            raise Exception("Invalid artifact source type.")

        # 根据架构选择不同的模板所在的包
        if Arch.ECS_SINGLE.value == architecture:
            package_name = project_setup_constant.INPUT_ROS_TEMPLATE_ECS_SINGLE_PATH
        elif Arch.ECS_CLUSTER.value == architecture:
            package_name = project_setup_constant.INPUT_ROS_TEMPLATE_ECS_CLUSTER_PATH
        else:
            # 目前仅支持单节点和集群版（可弹性伸缩）架构
            raise Exception("Invalid architecture.")

        self._replace_variables()

        # 如果是docker compose，
        # 1. 提取出端口，修改对应的Parameters
        # 2. 提取出替换参数，生成替换命令
        if artifact_source_type == ArtifactSourceType.DOCKER_COMPOSE.value:
            ports_to_open, service_ports = self._parse_docker_compose_ports()
            self._replace_docker_image_docker_compose()
            self.parameters[project_setup_constant.SECURITY_GROUP_PORTS_KEY] = ports_to_open
            self.parameters[project_setup_constant.SERVICE_PORTS_KEY] = service_ports
        # 如果是docker file，
        # 1. 提取出端口，修改对应的Parameters
        if artifact_source_type == ArtifactSourceType.DOCKERFILE.value:
            security_ports, service_ports = self._extract_ports_from_dockerfile()
            self.parameters[project_setup_constant.SERVICE_PORTS_KEY] = service_ports
            self.parameters[project_setup_constant.SECURITY_GROUP_PORTS_KEY] = security_ports
            custom_parameters = self.parameters.get(project_setup_constant.CUSTOM_PARAMETERS_KEY)
            docker_run_env_parameters = self.build_docker_run_parameters(custom_parameters)
            if docker_run_env_parameters and len(docker_run_env_parameters) > 0:
                self.parameters[project_setup_constant.DOCKERFILE_RUN_ENV_ARGS] = docker_run_env_parameters
        output_ros_template_path = os.path.join(self.output_base_path, project_setup_constant.OUTPUT_ROS_TEMPLATE_DIR,
                                                project_setup_constant.OUTPUT_ROS_TEMPLATE_NAME)
        self.processor.process(input_ros_template_name, self.parameters, output_ros_template_path, package_name)
        developer_logger.info(f"Template rendered to {output_ros_template_path}")

        output_config_path = os.path.join(self.output_base_path, project_setup_constant.OUTPUT_CONFIG_NAME)
        if artifact_source_type == ArtifactSourceType.INSTALL_PACKAGE.value:
            self.parameters[project_setup_constant.PACKAGE_NAME_KEY] = self.parameters.get(
                project_setup_constant.PACKAGE_PATH_KEY).split("/")[-1]
        self.processor.process(input_config_name, self.parameters, output_config_path,
                               project_setup_constant.INPUT_CONFIG_PATH)
        developer_logger.info(f"Config rendered to {output_config_path}")

        user_logger.info("Template rendering complete.")

    # 替换不是自定义服务参数的${xxx}变量为${!xxx}
    # DockerCompose场景替换PRE_START_COMMAND
    def _replace_variables(self):

        def replace_variable(match):
            var_name = match.group(1)
            if var_name not in names:
                return f'${{!{var_name}}}'
            return match.group(0)

        pattern = r'\$\{([^}]+)\}'
        custom_parameters = self.parameters.get(project_setup_constant.CUSTOM_PARAMETERS_KEY)
        if not custom_parameters:
            return
        names = [item['Name'] for item in custom_parameters]
        artifact_source_type = self.parameters.get(project_setup_constant.ARTIFACT_SOURCE_TYPE_KEY)
        if artifact_source_type == ArtifactSourceType.SOURCE_CODE.value:
            run_command = self.parameters.get(project_setup_constant.RUN_COMMAND_KEY)
            if not run_command:
                return
            run_command = re.sub(pattern, replace_variable, run_command)
            self.parameters[project_setup_constant.RUN_COMMAND_KEY] = run_command
        elif artifact_source_type == ArtifactSourceType.DOCKER_COMPOSE.value:
            pre_start_command = self.parameters.get(project_setup_constant.PRE_START_COMMAND_KEY)
            docker_compose_env_path = self.parameters.get(project_setup_constant.DOCKER_COMPOSE_ENV_PATH_KEY)
            replace_parameters_sed_commands = ProjectSetup.generate_sed_commands(custom_parameters,
                                                                                 docker_compose_env_path)
            if replace_parameters_sed_commands:
                pre_start_command = "\n".join(replace_parameters_sed_commands)

            self.parameters[project_setup_constant.PRE_START_COMMAND_KEY] = pre_start_command
        else:
            return

    # 生成替换.env中指定参数的值的sed命令与echo命令
    @staticmethod
    def generate_sed_commands(custom_parameters, env_file_relative_path):
        commands = []
        # 检查文件是否存在，不存在则创建.env文件
        env_abs_path = os.path.abspath(env_file_relative_path)
        if not os.path.exists(env_abs_path):
            with open(env_abs_path, 'w') as file:
                file.write('')
        with open(os.path.abspath(env_abs_path), 'r') as file:
            env_content = file.read()

        # DockerCompose相关文件在ROS模板中的的实际路径
        docker_compose_path = f'{project_setup_constant.DOCKER_COMPOSE_DIR}{env_file_relative_path}'
        for param in custom_parameters:
            name = param.get("Name")
            if name:
                variable_pattern = f"{name}="

                # 如果变量存在，则替换
                if variable_pattern in env_content:
                    command = f"sed -i 's/{variable_pattern}[^\\n]*/{variable_pattern}${{{name}}}/' {docker_compose_path}"
                else:
                    # 如果变量不存在，则添加
                    command = f"echo '{name}=${{{name}}}' >> {docker_compose_path}"

                commands.append(command)

        return commands

    def _copy_resources(self):
        output_base = Path(self.output_base_path)

        # 复制静态资源文件，包括icon、README.md、软件包、Docs
        self._copy_icons(output_base)
        self._copy_readme(output_base)
        self._copy_docs(output_base)

        artifact_source_type = self.parameters.get(project_setup_constant.ARTIFACT_SOURCE_TYPE_KEY)
        # 源代码
        if artifact_source_type == ArtifactSourceType.SOURCE_CODE.value:
            user_logger.info("Handling source code copying.")
        # 软件包
        elif artifact_source_type == ArtifactSourceType.INSTALL_PACKAGE.value:
            self._copy_software_package()
        elif artifact_source_type == ArtifactSourceType.DOCKER_COMPOSE.value:
            self._copy_and_package_docker_compose()
        # Dockerfile
        elif artifact_source_type == ArtifactSourceType.DOCKERFILE.value:
            self._copy_dockerfile()
        else:
            raise Exception("Invalid artifact source type.")

        service_type = self.parameters.get(project_setup_constant.SERVICE_TYPE_KEY)
        if service_type == ServiceType.MANAGED.value:
            self._copy_preset_parameters(output_base)

        user_logger.info("Resource copying complete.")

    @staticmethod
    def _copy_from_package(src_package, src_name, dst_directory):
        with resources.path(src_package, src_name) as src_path:
            if src_path.is_dir():
                shutil.copytree(src_path, dst_directory, dirs_exist_ok=True)
            else:
                shutil.copy2(src_path, dst_directory / src_name)

    def _copy_icons(self, output_base):
        icon_dir = project_setup_constant.INPUT_ICON_DIR
        output_icon_dir = output_base / project_setup_constant.OUTPUT_ICON_DIR
        self._copy_from_package(project_setup_constant.INPUT_ROOT_PATH, icon_dir, output_icon_dir)
        user_logger.info(f"Copied icons to {output_icon_dir}")

    def _copy_docs(self, output_base):
        arch = self.parameters.get(project_setup_constant.ARCHITECTURE_KEY, Arch.ECS_SINGLE.value)
        if Arch.ECS_SINGLE.value == arch:
            docs_dir = project_setup_constant.INPUT_DOCS_ECS_SINGLE_PATH
        elif Arch.ECS_CLUSTER.value == arch:
            docs_dir = project_setup_constant.INPUT_DOCS_ECS_CLUSTER_PATH
        else:
            raise Exception("Invalid architecture.")
        output_docs_dir = output_base / project_setup_constant.OUTPUT_DOCS_DIR
        self._copy_from_package(docs_dir, ".", output_docs_dir)

    def _copy_readme(self, output_base):
        readme_name = project_setup_constant.INPUT_README_NAME
        self._copy_from_package(project_setup_constant.INPUT_ROOT_PATH, readme_name, output_base)
        user_logger.info(f"Copied README to {output_base}")

    def _copy_preset_parameters(self, output_base):
        self._copy_from_package(project_setup_constant.INPUT_ROOT_PATH,
                                project_setup_constant.INPUT_PRESET_PARAMETERS_NAME, output_base)
        user_logger.info(f"Copied preset parameters to {output_base}")

    # 处理软件包文件的复制，如 tar.gz
    def _copy_software_package(self):
        user_logger.info("Handling install package copying...")
        install_package_path = self.parameters.get(project_setup_constant.PACKAGE_PATH_KEY)
        # abspath
        if not os.path.isabs(install_package_path):
            install_package_path = os.path.abspath(install_package_path)
        shutil.copy(install_package_path,
                    os.path.join(self.output_base_path, project_setup_constant.OUTPUT_PACKAGE_DIR))
        user_logger.info(
            f"Copied install package to {os.path.join(self.output_base_path, project_setup_constant.OUTPUT_PACKAGE_DIR)}")

    # 复制 Dockerfile
    def _copy_dockerfile(self):
        user_logger.info("Handling Dockerfile copying...")
        dockerfile_path = self.parameters.get(project_setup_constant.DOCKERFILE_PATH_KEY)
        if not os.path.isabs(dockerfile_path):
            dockerfile_path = os.path.abspath(dockerfile_path)
        shutil.copy(dockerfile_path,
                    os.path.join(self.output_base_path, project_setup_constant.OUTPUT_DOCKERFILE_DIR))
        user_logger.info(
            f"Copied Dockerfile to {os.path.join(self.output_base_path, project_setup_constant.OUTPUT_DOCKERFILE_DIR)}")

    # 识别并替换docker compose文件开源镜像，并托管到计算巢仓库中
    def _replace_docker_image_docker_compose(self):
        if not self.replace_image:
            return
        user_logger.info("docker compose replace docker image start")
        docker_compose_path = self.parameters.get(project_setup_constant.DOCKER_COMPOSE_PATH_KEY)
        if not os.path.isabs(docker_compose_path):
            docker_compose_path = os.path.abspath(docker_compose_path)
        # 解析docker-compose.yaml,替换其中的开源镜像
        with open(docker_compose_path, 'r') as stream:
            docker_compose_json = yaml.load(stream, Loader=yaml.FullLoader)
        # 获取计算巢容器镜像仓库路径
        response = CredentialsService.get_artifact_repository_credentials(self.context, constant.ACR_IMAGE)
        docker_host_path = os.path.dirname(response.body.available_resources[0].path)
        acr_image_artifact_parameters = []
        # 遍历 services 找到所有的 image_url
        services = docker_compose_json.get('services', {})
        try:
            for service, config in services.items():
                image_url = config.get('image')
                if not image_url or project_setup_constant.ALI_DOCKER_REPO_HOST_SUFFIX in image_url \
                        or config.get('secrets'):
                    continue
                image_split = image_url.split("/")
                image_split_len = len(image_split)
                if image_split_len >= 2:
                    # image为<registry>/<namespace>/<image_name>:<tag>类型 或 <namespace>/<image_name>:<tag>类型
                    namespace = image_split[-2]
                    last_name = image_split[-1]
                    last_name_split = last_name.split(":")
                    # image_name保留namespace，便于做区分
                    image_name = "{}/{}".format(namespace, last_name_split[0])
                    image_tag = last_name_split[1] if len(last_name_split) == 2 else 'latest'
                else:
                    # image为<image_name>:<tag>类型
                    last_name_split = image_split[0].split(":")
                    image_name = last_name_split[0]
                    image_tag = last_name_split[1] if len(last_name_split) == 2 else 'latest'
                artifact_name = "{}-{}".format(constant.ACR_IMAGE, image_name.replace("/", "-"))
                artifact_parameter = {
                    "ArtifactName": artifact_name,
                    "DockerImageUrl": image_url,
                    "DockerImageName": image_name,
                    "DockerImageTag": image_tag
                }
                config['image'] = f"{docker_host_path}/{image_name}:{image_tag}"
                acr_image_artifact_parameters.append(artifact_parameter)
        except Exception as e:
            developer_logger.error(f"docker compose replace docker image fail: {e}")
            raise
        user_logger.info(f"Docker compose replace image, artifact parameters:{acr_image_artifact_parameters}")
        self.parameters["ArtifactParameters"] = acr_image_artifact_parameters
        # 替换过的写到新文件中
        docker_compose_path_replaced = _get_replaced_file_name(docker_compose_path)
        with open(docker_compose_path_replaced, 'w') as file:
            file.write(yaml.dump(docker_compose_json))

    def _copy_and_package_docker_compose(self):
        user_logger.info("Handling Docker compose copying...")
        docker_compose_path = self.parameters.get(project_setup_constant.DOCKER_COMPOSE_PATH_KEY)
        if not os.path.isabs(docker_compose_path):
            docker_compose_path = os.path.abspath(docker_compose_path)
        if self.replace_image:
            docker_compose_file_name = os.path.basename(docker_compose_path)
            docker_compose_path_replaced = _get_replaced_file_name(docker_compose_path)
            output_docker_compose_path = os.path.join(self.output_base_path,
                                                      project_setup_constant.OUTPUT_DOCKER_COMPOSE_DIR,
                                                      docker_compose_file_name)
            shutil.move(docker_compose_path_replaced, output_docker_compose_path)
            user_logger.info(f"Move Docker compose replaced to {output_docker_compose_path}")
        else:
            shutil.copy(docker_compose_path,
                        os.path.join(self.output_base_path, project_setup_constant.OUTPUT_DOCKER_COMPOSE_DIR))
            user_logger.info(f"Copied Docker compose to "
                             f"{os.path.join(self.output_base_path, project_setup_constant.OUTPUT_DOCKER_COMPOSE_DIR)}")
        # 复制环境变量文件
        env_file_path = self.parameters.get(project_setup_constant.DOCKER_COMPOSE_ENV_PATH_KEY)
        if env_file_path:
            if not os.path.isabs(env_file_path):
                env_file_path = os.path.abspath(env_file_path)
            # 检查文件是否存在，不存在则创建.env文件
            if not os.path.exists(env_file_path):
                with open(env_file_path, 'w') as file:
                    file.write('')
            shutil.copy(env_file_path,
                        os.path.join(self.output_base_path, project_setup_constant.OUTPUT_DOCKER_COMPOSE_DIR))
            user_logger.info(
                f"Copied env file to {os.path.join(self.output_base_path, project_setup_constant.OUTPUT_DOCKER_COMPOSE_DIR)}")
        root_path = os.path.dirname(self.output_base_path / project_setup_constant.OUTPUT_DOCKER_COMPOSE_DIR)
        developer_logger.info(f"path: {root_path}")
        docker_compose_dir = 'docker_compose'
        try:
            archive_path = shutil.make_archive(
                base_name=str(self.output_base_path / project_setup_constant.OUTPUT_DOCKER_COMPOSE_DIR),
                format='tar',
                root_dir=root_path,
                base_dir=docker_compose_dir)
            developer_logger.info(f"Directory '{self.output_base_path}' has been packed into '{archive_path}'")
        except Exception as e:
            developer_logger.error(f"Packing failed: {e}")
            return

        shutil.rmtree(self.output_base_path / project_setup_constant.OUTPUT_DOCKER_COMPOSE_DIR)
        developer_logger.info(
            f"Removed directory '{self.output_base_path / project_setup_constant.OUTPUT_DOCKER_COMPOSE_DIR}'")

    def _handle_source_code_packaging(self):
        artifact_source_type = self.parameters.get(project_setup_constant.ARTIFACT_SOURCE_TYPE_KEY)
        if artifact_source_type != ArtifactSourceType.SOURCE_CODE.value:
            return
        user_logger.info("Handling source code packaging...")
        source_code_path = self.parameters.get(project_setup_constant.SOURCE_CODE_PATH_KEY)
        # 确保源文件目录存在且转换为 Path 对象
        source_code_path = Path(source_code_path).resolve()

        if not source_code_path.exists():
            raise FileNotFoundError(f"Source code path '{source_code_path}' does not exist.")

        # 创建临时目录用于存放需要打包的文件和目录
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            repo_name = self.parameters.get(project_setup_constant.REPO_NAME_KEY)
            package_dir = temp_dir_path / repo_name
            package_dir.mkdir(parents=True, exist_ok=True)
            # 定义需要排除的目录
            exclude_dirs = {'.computenest', '.git'}

            # 遍历原始目录，复制非排除的文件和目录到临时目录
            for item in source_code_path.iterdir():
                if item.name not in exclude_dirs:
                    if item.is_dir():
                        shutil.copytree(item, package_dir / item.name)
                    else:
                        shutil.copy2(item, package_dir / item.name)

            destination_dir = self.output_base_path / project_setup_constant.OUTPUT_PACKAGE_DIR
            # 如果存在则先删除
            if destination_dir.exists():
                shutil.rmtree(destination_dir)

            destination_dir.mkdir(parents=True, exist_ok=True)

            # 使用临时目录作为源进行打包
            try:
                archive_path = shutil.make_archive(
                    base_name=str(destination_dir / repo_name), format='gztar',
                    root_dir=temp_dir_path, base_dir=repo_name)
                developer_logger.info(f"Directory '{source_code_path}' has been packed into '{archive_path}'")
            except Exception as e:
                developer_logger.error(f"Packing failed: {e}")
                return

            # 确保目标base路径存在
            if not self.output_base_path.exists():
                self.output_base_path.mkdir(parents=True, exist_ok=True)

            # 移动.tar.gz文件到指定目录
            tar_gz_path = destination_dir / (repo_name + '.tar.gz')
            shutil.move(archive_path, tar_gz_path)
            user_logger.info(f"'{archive_path}' has been moved to '{tar_gz_path}'")

    def _parse_docker_compose_ports(self):
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
        docker_compose_path = self.parameters.get(project_setup_constant.DOCKER_COMPOSE_PATH_KEY)
        if not os.path.isabs(docker_compose_path):
            docker_compose_path = os.path.abspath(docker_compose_path)
        with open(docker_compose_path, 'r') as file:
            compose_content = yaml.safe_load(file)

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

                    if '/' in container_port:  # "50000:50000/tcp"
                        container_port, protocol = container_port.split('/')

                elif isinstance(port, dict):
                    host_port = str(port.get('published', port.get('target')))
                    container_port = str(port.get('target'))
                    protocol = port.get('protocol', 'tcp')

                ports_to_open.append((host_port, protocol))

                # 默认认为未标明协议的情况为 TCP
                if protocol == 'tcp':
                    service_ports.append(host_port)

        return ports_to_open, service_ports

    def _get_dockerfile_content(self) -> str:
        """
        获取 Dockerfile 的内容。

        返回:
            str: Dockerfile 的内容。

        异常:
            FileNotFoundError: 如果找不到 Dockerfile。
        """
        docker_file_path = self.parameters.get(project_setup_constant.DOCKERFILE_PATH_KEY)
        if not docker_file_path:
            raise ValueError("未找到有效的 Dockerfile 路径。")
        if not os.path.isabs(docker_file_path):
            docker_file_path = os.path.abspath(docker_file_path)

        try:
            with open(docker_file_path) as file:
                return file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"找不到 Dockerfile：{docker_file_path}")

    def _extract_ports_from_dockerfile(self):
        """
        从 Dockerfile 中提取暴露的端口信息（包括端口号和协议）。
        返回:
            list: 包含元组的列表，每个元组包含端口和协议（例如，('8080', 'tcp')）。
            如果没有暴露的端口，默认添加 ('8080', 'tcp')。
        """
        # 获取 Dockerfile 内容
        content = self._get_dockerfile_content()

        # 使用 DockerfileParser
        parser = DockerfileParser()
        parser.content = content

        ports_to_open = []  # 初始化返回的端口和协议列表
        service_ports = []  # 初始化仅端口的列表

        # 获取环境变量
        env_vars = parser.envs

        # 遍历指令并寻找 EXPOSE
        for line in content.splitlines():
            if line.lower().startswith('expose'):
                _, *ports = line.split()
                for port in ports:
                    # 处理环境变量的两种形式
                    if port.startswith('${') and port.endswith('}'):
                        var_name = port[2:-1]  # 去掉 ${ 和 }
                    elif port.startswith('$'):
                        var_name = port[1:]  # 去掉 $
                    else:
                        var_name = None

                    if var_name:
                        # 尝试从 env_vars 中获取值
                        port_num = env_vars.get(var_name)
                        if port_num is None:
                            continue  # 如果未找到值，则跳过
                        protocol = 'tcp'  # 默认协议
                    else:
                        # 处理常规端口和协议
                        port_parts = port.split('/')
                        port_num = port_parts[0]
                        protocol = port_parts[1] if len(port_parts) > 1 else 'tcp'  # 默认协议为 TCP

                    ports_to_open.append((port_num, protocol))  # 添加元组形式的端口和协议
                    service_ports.append(port_num)

        # 如果没有暴露任何端口，默认返回空的 ports_to_open 和 service_ports
        if not ports_to_open:
            ports_to_open.append(('8080', 'tcp'))
            service_ports.append('8080')

        return ports_to_open, service_ports

    def build_docker_run_parameters(self, custom_parameters: list):
        """
        构建docker run的自定义参数
        入参：
        "CustomParameters": [
                {
                    "Name": "InstanceSize",
                    "Type": "String",
                    "Label": "ECS Instance Size",
                    "Description": "The size of the EC2 instance",
                    "Default": "t2.micro",
                    "AllowedValues": ["t2.micro", "t2.small", "t2.medium"]
                }
            ]
        返回:
            -e InstanceSize=${InstanceSize}
        """
        if not custom_parameters:
            return None
        run_parameters = []
        for param in custom_parameters:
            name = param.get("Name")
            if name:
                run_parameters.append(f"-e {name}=${{{name}}}")  # 拼接环境变量格式

            # 返回拼接的参数字符串
        return ' '.join(run_parameters)

    # 将输入参数改为计算巢部署物允许的格式
    @staticmethod
    def _sanitize_name(name):
        # 只允许字母、数字、下划线、和中划线
        pattern = r'[^\w-]+'
        # 替换不符合的字符为下划线
        sanitized_name = re.sub(pattern, '_', name)
        return sanitized_name
