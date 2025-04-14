import os
import markdown
import uuid
import re

class Video:
    """
    Representa um vídeo com caminho, nome, descrição em Markdown, título e ID único.
    Pode conter referências ao vídeo anterior e ao próximo.
    """
    def __init__(self, path, filename, description, title):
        self.path = path
        self.filename = filename
        self.description = self.__load_description(description)
        self.title = title
        self.id = self.__generate_id()

    def __load_description(self, description):
        """
        Carrega a descrição do vídeo, convertendo de Markdown para HTML.
        Se a descrição for 'Sem descrição.', converte diretamente essa string.
        """
        if description != "Sem descrição.":
            description_file_path = os.path.join(self.path, description)
            with open(description_file_path, encoding="utf-8") as description_file:
                return markdown.markdown(description_file.read().strip())
        else:
            return markdown.markdown(description)

    def __generate_id(self):
        """
        Gera um ID único para o vídeo baseado no caminho e nome,
        utilizando UUID v5 com namespace fixo.
        """
        namespace = uuid.UUID('12345678-1234-5678-1234-567812345678')
        return str(uuid.uuid5(namespace, f"{self.path}/{self.filename}"))

    def set_previous(self, previous):
        """
        Define o ID do vídeo anterior na sequência.
        """
        self.previous = previous

    def set_next(self, next):
        """
        Define o ID do próximo vídeo na sequência.
        """
        self.next = next


class Curso:
    """
    Representa um curso contendo vídeos e/ou módulos (subpastas),
    escaneando a estrutura local para montar e organizar os conteúdos.
    """
    def __init__(self, path: str, curso_id):
        self.curso_id = curso_id
        self.path = path
        self.nome = os.path.basename(os.path.normpath(self.path))
        self._scan()
        self._sort_contents()
        self.video_cache = self.__indexar_videos(self)
        self.__set_navegacao_em_todos_videos()

    def __set_navegacao_em_todos_videos(self):
        """
        Define os IDs de navegação (anterior e próximo) para todos os vídeos indexados.
        """
        video_ids = list(self.video_cache.keys())

        for i, vid in enumerate(video_ids):
            video = self.video_cache[vid]
            if i > 0:
                video.set_previous(video_ids[i - 1])
            if i < len(video_ids) - 1:
                video.set_next(video_ids[i + 1])

    def _ordenar_por_numero_inicio(self, lista):
        """
        Ordena uma lista de strings com base no número inicial, se houver.
        """
        def extrair_numero(s):
            match = re.match(r"(\d+)", s)
            return int(match.group(1)) if match else float('inf')

        return sorted(lista, key=extrair_numero)

    def __indexar_videos(self, modulo):
        """
        Cria um dicionário com todos os vídeos de um curso ou módulo,
        indexados por seu ID.
        """
        video_cache = {}
        if hasattr(modulo, 'videos'):
            for v in modulo.videos:
                video_cache[v.id] = v

        if hasattr(modulo, 'modulos'):
            for m in modulo.modulos:
                video_cache = video_cache | self.__indexar_videos(m)

        return video_cache

    def _contem_mp4_em_pastas(self, path):
        """
        Verifica recursivamente se há arquivos .mp4 em um diretório ou subdiretórios.
        """
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.lower().endswith('.mp4'):
                    return True
        return False

    def _scan(self):
        """
        Realiza a varredura da pasta do curso, identificando vídeos e módulos,
        e instanciando-os conforme necessário.
        """
        has_modules, modules, has_files, files = self._check_folders(self.path)

        if has_files:
            videos = self._filter_files(files)
            if videos:
                self.videos = []
                for video in videos:
                    self.videos.append(Video(self.path, video[0], video[1], video[0].replace('.mp4', '')))

        if has_modules:
            self.modulos = []
            for module_name in modules:
                module_path = os.path.join(self.path, module_name)
                has_submodules, submodules, module_has_files, module_files = self._check_folders(module_path)
                module_files_length = len(module_files)
                module_has_mp4, module_has_txt = self._scan_files(module_files)

                if module_has_mp4 and module_files_length == 2 and module_has_txt:
                    module_videos = self._filter_files(module_files)
                    if module_videos:
                        if not hasattr(self, 'videos'):
                            self.videos = []
                        self.videos.append(Video(module_path, module_videos[0][0], module_videos[0][1], module_videos[0][0].replace('.mp4', '')))
                elif self._contem_mp4_em_pastas(module_path):
                    self.modulos.append(Modulo(module_path))

    def _ordenar_por_numero_inicio(self, lista, attr):
        """
        Ordena objetos de uma lista com base em um atributo que pode começar com número.
        """
        def extrair_numero(obj):
            valor = getattr(obj, attr)
            match = re.match(r"(\d+)", valor)
            return int(match.group(1)) if match else float('inf')

        return sorted(lista, key=extrair_numero)

    def _sort_contents(self):
        """
        Ordena os módulos e vídeos do curso com base em números no início dos nomes.
        """
        if hasattr(self, 'modulos'):
            self.modulos = self._ordenar_por_numero_inicio(self.modulos, 'nome')

        if hasattr(self, 'videos'):
            self.videos = self._ordenar_por_numero_inicio(self.videos, 'title')

    def _check_folders(self, path):
        """
        Verifica os diretórios e arquivos em um caminho.
        Retorna se há subpastas, seus nomes, se há arquivos e a lista de arquivos.
        """
        root, dirs, files = next(os.walk(path))
        has_modules = bool(dirs)
        has_files = bool(files)
        return has_modules, dirs, has_files, files

    def _scan_files(self, files: list):
        """
        Verifica se há arquivos de vídeo (.mp4) e texto (.txt ou .md) em uma lista.
        """
        has_mp4 = False
        has_text = False

        for file in files:
            if file.lower().endswith('.mp4'):
                has_mp4 = True
            elif file.lower().endswith(('.txt', '.md')):
                has_text = True

        return has_mp4, has_text

    def _filter_files(self, files: list):
        """
        Associa vídeos a arquivos de descrição, quando disponíveis.
        Retorna lista de pares [vídeo, descrição].
        """
        videos = []
        tem_mp4, tem_texto = self._scan_files(files)

        if not tem_mp4:
            return videos

        files_length = len(files)

        if files_length == 1:
            if files[0].lower().endswith('.mp4'):
                videos.append([files[0], "Sem descrição."])

        elif files_length == 2:
            if tem_texto:
                video = []
                for file in files:
                    if file.lower().endswith('.mp4'):
                        video.append(file)
                    elif file.lower().endswith(('.txt', '.md')):
                        video.append(file)
                videos.append(video)
            else:
                for file in files:
                    if file.lower().endswith('.mp4'):
                        videos.append([file, "Sem descrição."])

        elif files_length > 2:
            for file in files:
                if file.lower().endswith('.mp4'):
                    videos.append([file, "Sem descrição."])

        return videos


class Modulo(Curso):
    """
    Representa um módulo dentro de um curso.
    Estruturalmente igual a um curso, com lógica de escaneamento herdada.
    """
    def __init__(self, path):
        self.path = path
        self.nome = os.path.basename(os.path.normpath(self.path))
        self._scan()
        self._sort_contents()
