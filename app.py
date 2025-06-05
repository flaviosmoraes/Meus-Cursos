from flask import Flask, render_template, send_from_directory, request, jsonify
from flask_caching import Cache
import os
from curso import Curso
from db_utils import ja_assistido, marcar_como_assistido, desmarcar_como_assistido, listar_assistidos
#from waitress import serve

app = Flask(__name__)

app.config['CACHE_TYPE'] = 'simple'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300 
cache = Cache(app)

lista_cursos = {
    'exemplo', Curso(r'c:\exemplo', 'exemplo')
}

def find_video_id(curso, video_id):
    """Retorna o vídeo com o ID especificado a partir do cache do curso."""
    return curso.video_cache.get(video_id)

@app.route("/")
def home():
    """Exibe a página inicial."""
    return render_template("index.html")

@app.route("/cursos")
@cache.cached()  # Adicionando o cache para a rota de cursos
def cursos():
    """Exibe todos os cursos disponíveis."""
    return render_template("cursos.html", cursos=lista_cursos)

@app.route("/curso/<curso_id>")
def page_curso(curso_id):
    """
    Exibe a página com os detalhes de um curso específico.

    Args:
        curso_id (str): Identificador do curso.

    Returns:
        str | Response: Página do curso ou erro 404 se não encontrado.
    """
    curso = lista_cursos.get(curso_id)
    if not curso:
        return "Curso não encontrado", 404
    assistidos = listar_assistidos(curso_id)
    return render_template("curso.html", curso=curso, curso_id=curso_id, assistidos=assistidos)

@app.route("/video/<curso_id>/<video_id>")
def video(curso_id, video_id):
    """
    Exibe a página de um vídeo específico de um curso.

    Args:
        curso_id (str): Identificador do curso.
        video_id (str): Identificador do vídeo.

    Returns:
        str | Response: Página do vídeo ou erro 404 se não encontrado.
    """
    curso = lista_cursos.get(curso_id)
    if not curso:
        return render_template("404.html", erro="Curso não encontrado"), 404

    video = find_video_id(curso, video_id)
    if video:
        caminho_vídeo = video.path.split(curso.nome + "\\")[1].split("\\")
        if caminho_vídeo[-1] == video.title:
            caminho_vídeo.pop(-1)
        assistido = ja_assistido(video_id)
        return render_template("video.html", video=video, curso_id=curso_id, curso_nome=curso.nome, caminho_vídeo=caminho_vídeo, assistido=assistido)

    return render_template("404.html", erro="Vídeo não encontrado"), 404

@app.route("/media/<curso_id>/<video_id>")
def media(curso_id, video_id):
    """
    Serve o arquivo de mídia (vídeo) para reprodução.

    Args:
        curso_id (str): Identificador do curso.
        video_id (str): Identificador do vídeo.

    Returns:
        Response: Arquivo de mídia ou erro 404 se não encontrado.
    """
    curso = lista_cursos.get(curso_id)
    if not curso:
        return render_template("404.html", erro="Curso não encontrado"), 404

    video = find_video_id(curso, video_id)
    if video:
        return send_from_directory(video.path, video.filename)

    return render_template("404.html", erro="Mídia não encontrada"), 404


@app.route("/assistido", methods=["POST", "DELETE"])
def assistido():
    data = request.get_json()
    video_id = data.get("video_id")
    curso_id = data.get("curso_id")

    if not video_id:
        return jsonify({"error": "Dados incompletos"}), 400

    if request.method == "POST":
        marcar_como_assistido(video_id, curso_id)
        return jsonify({"status": "marcado"})

    if request.method == "DELETE":
        desmarcar_como_assistido(video_id)
        return jsonify({"status": "desmarcado"})


if __name__ == "__main__":
    app.run(debug=True)
    # serve(app, host='0.0.0.0', port=5000, threads=8)
