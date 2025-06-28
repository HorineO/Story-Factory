initial_nodes = [
    {
        "id": "1",
        "type": "text",
        "data": {"label": "Text Node"},
        "position": {"x": 0, "y": 0},
        "sourcePosition": "right",
    },
    {
        "id": "2",
        "type": "generate",
        "data": {"label": "Generate Node"},
        "position": {"x": 150, "y": 100},
        "sourcePosition": "right",
        "targetPosition": "left",
    },
    {
        "id": "3",
        "type": "chapter",
        "data": {"label": "Chapter Node"},
        "position": {"x": 350, "y": -100},
        "targetPosition": "left",
    },
]

initial_edges = [
    {"id": "e1-2", "source": "1", "target": "2"},
    {"id": "e2-3", "source": "2", "target": "3"},
]
