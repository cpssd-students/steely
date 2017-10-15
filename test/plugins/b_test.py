import steely.plugins.b as b


data = [
    ('Hello', 'Hello'),
    ('Pasta', '{}asta'),
    ('Pizza Pie', '{}izza {}ie'),
    ('Brandon', '{}randon'),
    ('Great! Good!', '{}reat! {}ood!'),
    ('Oh boy, this pasta is good', 'Oh {}oy, this {}asta is {}ood'),
]
for input_, expected_format in data:
    expected_output = expected_format.format(*([b.REPLACEMENT] * expected_format.count('{}')))
    assert expected_output == b.encode(input_)
