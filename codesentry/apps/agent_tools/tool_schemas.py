"""
Описание доступных инструментов в формате function calling (совместимо
с Ollama /api/chat при поддержке моделью tools, напр. qwen2.5-coder, llama3.1).
"""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "Показать список файлов и папок внутри указанной директории рабочей папки.",
            "parameters": {
                "type": "object",
                "properties": {
                    "relative_dir": {
                        "type": "string",
                        "description": "Относительный путь внутри рабочей папки, например '.' или 'src'.",
                    }
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Прочитать содержимое текстового файла из рабочей папки.",
            "parameters": {
                "type": "object",
                "properties": {
                    "relative_path": {"type": "string", "description": "Относительный путь к файлу."}
                },
                "required": ["relative_path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Создать файл или полностью перезаписать его содержимое.",
            "parameters": {
                "type": "object",
                "properties": {
                    "relative_path": {"type": "string", "description": "Относительный путь к файлу."},
                    "content": {"type": "string", "description": "Полное новое содержимое файла."},
                },
                "required": ["relative_path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "append_file",
            "description": "Дописать текст в конец существующего файла, не стирая его содержимое.",
            "parameters": {
                "type": "object",
                "properties": {
                    "relative_path": {"type": "string", "description": "Относительный путь к файлу."},
                    "content": {"type": "string", "description": "Текст, который нужно дописать."},
                },
                "required": ["relative_path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_file",
            "description": "Удалить файл (не папку) из рабочей папки.",
            "parameters": {
                "type": "object",
                "properties": {
                    "relative_path": {"type": "string", "description": "Относительный путь к файлу."}
                },
                "required": ["relative_path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_directory",
            "description": "Создать новую папку (и промежуточные папки при необходимости).",
            "parameters": {
                "type": "object",
                "properties": {
                    "relative_path": {"type": "string", "description": "Относительный путь к новой папке."}
                },
                "required": ["relative_path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_files_recursive",
            "description": "Показать полный список файлов во всех вложенных папках рабочей директории.",
            "parameters": {
                "type": "object",
                "properties": {
                    "relative_dir": {
                        "type": "string",
                        "description": "С какой подпапки начинать обход, по умолчанию вся рабочая папка ('.').",
                    }
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_files_by_name",
            "description": "Найти файлы и папки, в имени которых встречается указанная подстрока (по всей рабочей папке рекурсивно).",
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern": {"type": "string", "description": "Подстрока для поиска в имени файла/папки."},
                    "relative_dir": {"type": "string", "description": "Подпапка для поиска, по умолчанию вся рабочая папка."},
                },
                "required": ["pattern"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_file_content",
            "description": "Найти текст внутри содержимого файлов (рекурсивно по всей рабочей папке). Возвращает файл, номер строки и фрагмент.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Текст, который нужно найти внутри файлов."},
                    "relative_dir": {"type": "string", "description": "Подпапка для поиска, по умолчанию вся рабочая папка."},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "explain_file",
            "description": "Объяснить простым языком, что делает указанный файл (анализирует содержимое через ИИ).",
            "parameters": {
                "type": "object",
                "properties": {
                    "relative_path": {"type": "string", "description": "Относительный путь к файлу."}
                },
                "required": ["relative_path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "explain_folder",
            "description": "Дать общий обзор простым языком, что за файлы находятся в папке и как они связаны между собой.",
            "parameters": {
                "type": "object",
                "properties": {
                    "relative_dir": {"type": "string", "description": "Подпапка для обзора, по умолчанию вся рабочая папка."}
                },
                "required": [],
            },
        },
    },
]
