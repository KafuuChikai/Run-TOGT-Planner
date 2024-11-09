from utils.RaceGenerator.GenerationTools import create_state, create_gate
from utils.RaceGenerator.GateShape import SingleBall, TrianglePrisma, RectanglePrisma, PentagonPrisma, HexagonPrisma
from utils.RaceGenerator.RaceTrack import RaceTrack

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

# print(ball_gate_no_name.to_dict())
# print(ball_gate.to_dict())
# print(tri_gate_no_name.to_dict())
# print(tri_gate.to_dict())
# print(rec_gate_no_name.to_dict())
# print(rec_gate.to_dict())
# print(pen_gate_no_name.to_dict())
# print(pen_gate.to_dict())
# print(hex_gate_no_name.to_dict())
# print(hex_gate.to_dict())

state_kwargs = {
    'pos' : [0.0, 0.0, 0.0],
    'vel' : [1.0, 0.0, 0.0],
    'acc' : [2.0, 0.0, 0.0],
    'jer' : [3.0, 0.0, 0.0],
    'rot' : [4.0, 1.0 ,1.0],
    'cthrustmass' : 5.0,
    'euler' : [6.0, 1.0 ,1.0]
}
init_state = create_state(state_kwargs)
# print(state.to_dict())
end_state = create_state(state_kwargs)

test_race = RaceTrack(init_state=init_state,
                      end_state=end_state,
                      race_name='test')
test_race.add_gate(ball_gate)
test_race.add_gate(tri_gate)
test_race.add_gate(rec_gate)
test_race.add_gate(pen_gate)
test_race.add_gate(hex_gate)

# print(test_race.to_dict())
# test_race.save_to_yaml(save_dir="track", overwrite=True, standard=False)
test_race.save_to_yaml(save_dir="track", overwrite=True, standard=True, save_output=True)
read_race = RaceTrack(init_state=init_state,
                      end_state=end_state,
                      race_name='test')
read_race.load_from_yaml(load_dir="track/test.yaml")
print(read_race.to_dict())
read_race.save_to_yaml(save_dir="track", overwrite=True, standard=True, save_output=True)