let ajaxSearchSuccessFunction = function(response){

	console.log("sdafsda")
	let results = response['result']
	let $chatArea = $('#chats > ul')
	$chatArea.empty()
	if(results.length == 0){
		let countNoResultFlag = $chatArea.has(".noResult")['length']
		if(!countNoResultFlag){
			$chatArea.append('<p class="noResult addShadowSearch">no results found</p>')
		}
		return
	}
	$.each(results, function(index, result){
		let sendMessageLink = $chatArea.attr('view-profile-link')
		let listItem = `<li class="addShadowSearch">
							<img src=${result["profile_picture"]}>
							<div>
								<p>${result["username"]}</p>
								<a>view profile</a>
							</div>
						</li>`
		$chatArea.append(listItem)
		$("#chats > ul").children().each(function(){
			$(this).find("a").on('mouseenter',function(){
				$(this).addClass("addShadow")
			})
			$(this).find("a").on('mouseleave',function(){
				$(this).removeClass("addShadow")
			})
		})
	})
}



let onSearchFunction = function($search){
		let searchQuery = $search.children(':text').val()
		if(searchQuery == ""){
			$("#chats > ul").empty()
			return
		}
		$.ajax({
			url:$search.attr('search-url'),
			data:$search.serialize(),
			dataType:'json',
			success: (data) => ajaxSearchSuccessFunction(data),
		})
	}

let messageSucessfullySent = function(data,$text){
	$text.val("")
}

let sendFunction = function(event,$send){
		event.preventDefault()
		event.stopPropagation()
		var form = $send.parent().eq(0)
		var $text = $send.siblings().eq(1)
		if ($text.val()==""){
			return
		}
		var sender = $("#chatRoot").attr("current-user")
		
		$.ajax({
			url:form.attr('send-to'),
			method:"POST",
			dataType:'json',
			data:form.serialize()+`&sender=${sender}&receiver=himanshu`,
			success:(data) => messageSucessfullySent(data,$text)
		})
}

$(document).ready(function (){
		let $search = $("#searchInput")
		$search.on('input',() => onSearchFunction($search))

		let $send = $("#messageTypeArea > button")
		$send.on('mousedown', function(){
			$(this).css('background-color',"#668cff")
		})
		$send.on('mouseup', function(){
			$(this).css('background-color',"rgb(70, 116, 191)")
		})
		$send.on('click',( (event) => sendFunction(event,$send) ))
	})
