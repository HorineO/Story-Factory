import os

# Flask配置
DEBUG = True
PORT = 5000

# API配置
API_PREFIX = "/api"

# OpenAI配置
OPENAI_BASE_URL = "https://xiaohumini.site/v1"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEFAULT_MODEL = "gpt-4o-mini"

# 静态文件配置
STATIC_FOLDER = "../frontend/build"
STATIC_URL_PATH = "/"

# Socket.IO配置
SOCKETIO_CORS = "*"
