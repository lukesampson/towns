import parse, util

def fixture(name):
    return util.readtext('fixtures', name)

def assert_template(item, name, data):
	assert item[0] == 'template'
	assert item[1] == name
	assert len(item[2]) == len(data)
	for key, val in data.items():
		assert key in item[2]
		assert item[2][key] == val

def assert_text(item, value):
	assert item[0] == 'text'
	assert item[1] == value

def test_parse_template_then_text():
	test = "{{parent | param = with nested {{child | test}} }}some text"

	items = parse.parse(test)
	assert len(items) == 2

	assert_template(items[0], 'parent', { 'param': 'with nested {{child | test}}'})
	assert_text(items[1], 'some text')

def test_text():
	test = "some text"

	items = parse.parse(test)
	assert len(items) == 1
	
	assert_text(items[0], 'some text')

def test_nested_template_as_first_param():
	test = "{{small|{{ref|fedelec}}}}"
	items = parse.parse(test)

	assert len(items) == 1
	assert_template(items[0], "small", { '{{ref|fedelec}}': None })

def test_template_param_with_link():
	test = "{{test|param=test [[link]]}}"
	items = parse.parse(test)

	assert len(items) == 1
	assert_template(items[0], "test", { 'param': 'test [[link]]' })

def test_template_param_has_link_with_pipe():
	test = "{{test|param=[[link|]]}}"
	items = parse.parse(test)

	assert len(items) == 1
	assert_template(items[0], "test", { 'param': '[[link|]]' })
