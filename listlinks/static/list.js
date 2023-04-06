$.get("api/links", {
	c : 5
}).done( (r) => {
	let listview = $('#main_list').empty()
	r.forEach( (e,i) => {

		let mainLink = "<a href="+e['destination']+">"+e['token']+" => "+e['destination']+"</a>"
		let deleteBtn = "<button class='stolen_button' type=submit onclick='deleteLink(this)' id="+e['token']+">delete</button>"
		listview.append($("<li>").html(mainLink+deleteBtn))
	})
})

function deleteLink(e)
{
	let csrf = $('#csrftoken')[0].value
	console.log(csrf)

	$.post("/api/delete",{token: e["id"],csrfmiddlewaretoken: csrf}).done(() =>{
  console.log("removed")
  window.location=window.location
});
}