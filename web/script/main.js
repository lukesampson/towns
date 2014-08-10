$(function() {
	map = init_map();
	towns = load_data();

	towns = filter(towns, [ { fn: filter_pop, args: { min: 2000, max: 3000 } }])

	show_towns(towns, map);
});

function init_map() {
	var options = {
		center: new google.maps.LatLng(-27.553986, 135.423151),
		zoom: 5
	};
	return new google.maps.Map(document.getElementById("map_canvas"), options);
}

function load_data() {
	var lines = $('#csv_data').text().split('\n');
	
	function row(line) {
		return line.split(',')
	}

	var headers = row(lines[0]);
	data = []
	for(var i = 1; i < lines.length; i++) {
		r = row(lines[i])
		var datarow = {}

		for(var j = 0; j < headers.length; j++) {
			val = r[j]
			if(!isNaN(val)) {
				val = Number(val)
			}
			datarow[headers[j]] = val;
		}

		data.push(datarow);
	}
	return data;
}

function filter(towns, filters) {
	var filtered = [];
	for(var i = 0; i < towns.length; i++) {
		var town = towns[i];
		var match = true;
		for(var j = 0; j < filters.length; j++) {
			filter = filters[j];
			if(!filter.fn(town, filter.args)) {
				match = false;
				break;
			}
		}
		if(match) {
			filtered.push(town);
		}
	}
	return filtered;
}

function filter_pop(town, args) {
	return (args.min == null || town.pop_total > args.min)
		&& (args.max == null || town.pop_total < args.max)
}

function show_towns(towns, map) {
	for(var i = 0; i < towns.length; i++) {
		town = towns[i];
		add_town(map, town);
	}
}

function add_town(map, town) {
	var marker = new google.maps.Marker({
		position: new google.maps.LatLng(town.lat,town.lng),
		map: map,
		title: town.name
	});

	var info = new google.maps.InfoWindow({
		content: '<div><h3>' + town.name + '</h3><dl><dt>Population</dt><dd>' + town.pop_total + '</dd></dl></div>'
	});

	google.maps.event.addListener(marker, 'click', function() {
		info.open(map, marker);
	});
}