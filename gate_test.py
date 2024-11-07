from utils.RaceGenerator.GenerationTools import create_gate
from utils.RaceGenerator.GateShape import SingleBall, TrianglePrisma, RectanglePrisma, PentagonPrisma, HexagonPrisma

ball_kwargs = {
    'radius': 0.5,
    'margin': 0.0
}
ball_gate_no_name = create_gate(SingleBall, [0.0, 0.0, 0.0], True, ball_kwargs)
ball_gate = create_gate(SingleBall, [0.0, 0.0, 0.0], True, ball_kwargs, 'ball_gate')

tri_kwargs = {
    'rpy': [0.0, -90, 0.0],
    'width': 2.4,
    'height': 2.4,
    'margin': 0.0,
    'length': 0.0,
    'midpoints': 0
}
tri_gate_no_name = create_gate(TrianglePrisma, [0.0, 0.0, 0.0], True, tri_kwargs)
tri_gate = create_gate(TrianglePrisma, [0.0, 0.0, 0.0], True, tri_kwargs, 'tri_gate')

rec_kwargs = {
    'rpy': [0.0, -90, 0.0],
    'width': 2.4,
    'height': 2.4,
    'marginW': 0.0,
    'marginH': 0.0,
    'length': 0.0,
    'midpoints': 0
}
rec_gate_no_name = create_gate(RectanglePrisma, [0.0, 0.0, 0.0], True, rec_kwargs)
rec_gate = create_gate(RectanglePrisma, [0.0, 0.0, 0.0], True, rec_kwargs, 'rec_gate')

pen_kwargs = {
    'rpy': [0.0, -90, 0.0],
    'radius': 2.4,
    'margin': 0.0,
    'length': 0.0,
    'midpoints': 0
}
pen_gate_no_name = create_gate(PentagonPrisma, [0.0, 0.0, 0.0], True, pen_kwargs)
pen_gate = create_gate(PentagonPrisma, [0.0, 0.0, 0.0], True, pen_kwargs, 'pen_gate')

hex_kwargs = {
    'rpy': [0.0, -90, 0.0],
    'side': 2.4,
    'margin': 0.0,
    'length': 0.0,
    'midpoints': 0
}
hex_gate_no_name = create_gate(HexagonPrisma, [0.0, 0.0, 0.0], True, hex_kwargs)
hex_gate = create_gate(HexagonPrisma, [0.0, 0.0, 0.0], True, hex_kwargs, 'hex_gate')

print(ball_gate_no_name.to_dict())
print(ball_gate.to_dict())
print(tri_gate_no_name.to_dict())
print(tri_gate.to_dict())
print(rec_gate_no_name.to_dict())
print(rec_gate.to_dict())
print(pen_gate_no_name.to_dict())
print(pen_gate.to_dict())
print(hex_gate_no_name.to_dict())
print(hex_gate.to_dict())