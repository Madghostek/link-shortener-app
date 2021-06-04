$.get("api/links", {
	c : 5
}).done( (r) => {
	console.log(r)
	let listview = $('#main_list').empty()
	r.forEach( (e,i) => {
		listview.append($("<li>").text(e['token']+" => "+e['destination']))
	})
})
