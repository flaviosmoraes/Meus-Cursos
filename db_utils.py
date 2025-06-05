from models import WatchedVideo, Session

def marcar_como_assistido(video_id, curso_id):
    session = Session()
    if not session.query(WatchedVideo).filter_by(id=video_id).first():
        novo = WatchedVideo(id=video_id, curso_id=curso_id)
        session.add(novo)
        session.commit()
    session.close()

def listar_assistidos(curso_id=None):
    session = Session()
    query = session.query(WatchedVideo)
    if curso_id:
        query = query.filter_by(curso_id=curso_id)
    resultados = query.all()
    session.close()
    videos = []
    for video in resultados:
        id = video.id
        videos.append(id)
    return videos

def ja_assistido(video_id):
    session = Session()
    resultado = session.query(WatchedVideo).filter_by(id=video_id).first()
    session.close()
    return resultado is not None

def desmarcar_como_assistido(video_id):
    session = Session()
    registro = session.query(WatchedVideo).filter_by(id=video_id).first()
    if registro:
        session.delete(registro)
        session.commit()
    session.close()
