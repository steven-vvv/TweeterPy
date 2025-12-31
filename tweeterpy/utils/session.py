import pickle
from pathlib import Path
from typing import Any, List
import logging.config
from curl_cffi.requests.session import Session
from tweeterpy.constants import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


def save_session(file_path: Path, session: Session) -> Path:
    """
    Save session headers and cookies to a file.
    
    This function serializes session headers and cookies using pickle
    to preserve all attributes and data structures. The parent directory
    will be created if it doesn't exist.
    
    Args:
        file_path (Path): Path where to save the session file.
        session (Session): The curl_cffi Session object to save.
    
    Returns:
        Path: The path to the saved session file.
    
    Raises:
        TypeError: If session is not a valid Session object.
    """
    # 验证会话对象类型
    if not isinstance(session, Session):
        raise TypeError(
            f"Invalid session type. {session} is not a requests.Session Object...")
    
    # 确保父目录存在
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 使用pickle序列化headers和cookies的内部属性
    session_data: List[Any] = [
        dict(session.headers),
        session.cookies.jar._cookies
    ]
    
    # 将会话数据写入文件，使用二进制模式
    with file_path.open("wb") as file:
        pickle.dump(session_data, file)
    
    return file_path


def load_session(file_path: Path, session: Session) -> Session:
    """
    Load session headers and cookies from a file.
    
    This function reads a session file and restores the headers and
    cookies to the provided session object using pickle to preserve
    all attributes and data structures.
    
    Args:
        file_path (Path): Path to the session file to load.
        session (Session): The curl_cffi Session object to restore.
    
    Returns:
        Session: The session object with restored headers and cookies.
    
    Raises:
        FileNotFoundError: If the session file doesn't exist.
        TypeError: If session is not a valid Session object.
    """
    # 验证会话对象类型
    if not isinstance(session, Session):
        raise TypeError(
            f"Invalid session type. {session} is not a requests.Session Object...")
    
    # 使用pickle读取文件并解析会话数据
    with file_path.open("rb") as file:
        session_data: List[Any] = pickle.load(file)
    
    # 恢复会话headers
    session.headers = session_data[0]  # type: ignore
    # 从pickle数据恢复cookies的内部属性
    session.cookies.jar._cookies.update(session_data[1])  # type: ignore
    
    return session


if __name__ == "__main__":
    pass
