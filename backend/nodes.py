initial_nodes = [
    {
        "id": "1",
        "type": "start",
        "data": {"label": "start Node"},
        "position": {"x": 0, "y": 0},
        "sourcePosition": "right",
    },
    {
        "id": "2",
        "type": "end",
        "data": {"label": "end Node"},
        "position": {"x": 250, "y": -150},
        "sourcePosition": "right",
        "targetPosition": "left",
    },
]

initial_edges = [
    {"id": "e1-2", "source": "1", "target": "2"},
]
