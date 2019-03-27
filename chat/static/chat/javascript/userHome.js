let addContactToSideBar = function(result,$chatArea){
	let sendMessageLink = $chatArea.attr('view-profile-link')
		let listItem = `<li class="addShadowSearch" onclick='setCurrentChatWindow(event)'>
							<img src=${result["profile_picture"]}>
							<div class="outer">
								<h1>${result["username"]}</h1>
								<p>${result["status"]}</p>
								<div class="inner">
										<a>view profile</a>
										<a class="report">report user</a>
								</div>
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
}


let ajaxSearchSuccessFunction = function(response){

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
		addContactToSideBar(result,$chatArea)
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
			data:$search.serialize()+`&user=${$("#chatRoot").attr('current-user')}`,
			dataType:'json',
			success: (data) => ajaxSearchSuccessFunction(data),
		})
	}

											//tells if message was
											//sent or received
let addMessageToChatBox = function(message,senderClass){
	let $messageList = $("#messages > ul")
	let list = `<li class=${senderClass}>
					<p>${message}</p>
				</li>`	
		
	$messageList.append(list)
	$messageList.scrollTop($messageList.prop('scrollHeight'))
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
		var receiver = $("#chatRoot").attr('current-chat-window')

		var message=form.serialize()+`&sender=${sender}&receiver=${receiver}`
		var val = $text.val()
		$text.val('')
		
		addMessageToChatBox(val,"sent")

		$.ajax({
			url:form.attr('send-to'),
			method:"POST",
			dataType:'json',
			data:message,
			success:function(data){

			}
		})
}

let displayMessages = function(data,user){
	$messageList = $("#messages > ul")
	$messageList.empty()
	messages = data['messages']
	$.each(messages, function(index, message){
		if(user==message['related_contact__contact__username']){
			addMessageToChatBox(message['message'],"sent")
		}
		else{
			addMessageToChatBox(message['message'],"received")	
		}
	})
}

let setCurrentChatWindow = function(e){
	let $selectedWindow = $(e.currentTarget).eq(0)
	let $chatRoot = $("#chatRoot")
	$chatRoot.attr('current-chat-window',$selectedWindow.find("h1").text())
	
	let $prevWindow = $("#sideBar").find(".selectedChatWindow").eq(0)
	if($prevWindow != $selectedWindow){
		$prevWindow.toggleClass('selectedChatWindow')
		$selectedWindow.toggleClass('selectedChatWindow')
	}
	
	$selectedWindow.find(".inner > p").remove()
	var user = $chatRoot.attr('current-user')
	var receiver = $chatRoot.attr('current-chat-window')
	var url=$("#chatRoot").attr('get-message-url')
	var requestData = {
		"user" : user,
		"receiver" : receiver
	}
	$.ajax({
		method:"GET",
		data: requestData,
		dataType:"json",
		url:url,
		success:(data) => displayMessages(data,user)
	})
	
}

let showNotification = function(notification){
	let notificationBy = $(`[username=${notification['contact__username']}]`)
	notificationBy.parent().prepend(notificationBy)
	let $lastMessageDisplay = notificationBy.find(".outer > p").eq(0)
	$lastMessageDisplay.text(notification['last_message__message'])
	notificationBy = notificationBy.eq(0).find(".inner").eq(0)
	if(notificationBy.has("p").length === 0){
		notificationBy.append(`<p>${notification['unread_messages']}`)
	}
	else{
		notificationBy = notificationBy.find('p')
		notificationBy.text(notification['unread_messages'])	
	}
}

let displayNewMessages = function(data,user){
 	let currentChatWindow = $("#sideBar").find(".selectedChatWindow").find('h1').text()

	messages = data['messages']
	notifications =data['notifications']
	
	$.each(notifications,function(index,notification){
		showNotification(notification)
	})

	$.each(messages, function(index, message){
		if(user==message['related_contact__contact__username']){
			addMessageToChatBox(message['message'],"sent")
		}
		else{
			addMessageToChatBox(message['message'],"received")	
		}
	})
}

let checkNewMessages = function(){
	var $chatRoot = $("#chatRoot")
	var user = $chatRoot.attr('current-user')
	var url = $chatRoot.attr('check-new-message')
	var currentChatWindow = $chatRoot.attr('current-chat-window')
	var requestData = {
		"user" : user,
		"currentChatWindow":currentChatWindow
	}
	$.ajax({
		method:"GET",
		data: requestData,
		dataType:"json",
		url:url,
		success:(data) => displayNewMessages(data,user)
	})
}

let miscEffets = function($search,$send){
	$search.keydown(function(e){
			if(e.keyCode==13){
				e.preventDefault()
			}
		})

	$send.on('mousedown', function(){
			$(this).css('background-color',"#668cff")
		})
		$send.on('mouseup', function(){
			$(this).css('background-color',"rgb(70, 116, 191)")
		})
}

$(document).ready(function (){
		
		let $search = $("#searchInput")
		let $send = $("#messageTypeArea > button")
		
		miscEffets($search,$send)
		
		setInterval(checkNewMessages,1000)

		$search.on('input',() => onSearchFunction($search))
		$send.on('click',( (event) => sendFunction(event,$send) ))

	})
