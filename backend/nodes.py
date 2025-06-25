initial_nodes = [
    {
        "id": "1",
        "type": "input",
        "data": {"label": "Input Node"},
        "position": {"x": 250, "y": 5},
        "sourcePosition": "right",
    },
    {
        "id": "2",
        "data": {"label": "Default Node"},
        "position": {"x": 100, "y": 100},
        "sourcePosition": "right",
        "targetPosition": "left",
    },
    {
        "id": "3",
        "type": "output",
        "data": {"label": "Output Node"},
        "position": {"x": 400, "y": 200},
        "targetPosition": "left",
    },
]

initial_edges = [
    {"id": "e1-2", "source": "1", "target": "2", "animated": True},
    {"id": "e2-3", "source": "2", "target": "3"},
]
