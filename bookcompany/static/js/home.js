$(document).ready(function() {
	try{
        if(!$('#myCanvas1').tagcanvas({
          textColour: '#DC143C',
          outlineColour: 'white',
          reverse: true,
          depth: 0.8,
          maxSpeed: 0.1
        },'tags1')) {
          // something went wrong, hide the canvas container
          $('#myCanvasContainer').hide();
        }

        if(!$('#myCanvas2').tagcanvas({
          textColour: 'teal',
          outlineColour: 'white',
          reverse: true,
          depth: 0.8,
          maxSpeed: 0.1
        },'tags2')) {
          // something went wrong, hide the canvas container
          $('#myCanvasContainer').hide();
        }
    }catch(e){
    	console.log(e);
    }
});



$(document).ready(function(){

$("#booklist").stupidtable();

var Home = function(){

	

	$(".plus").click(function(){
		// alert($(this).parent().find("input").attr("value") );
		var number = $(this).parent().find("input").attr("value");
		var numbers = $(this).parent().parent().parent().find(".total_numbers").html();
		
		number = Number(number);
		numbers = Number(numbers);
		if(number >= numbers) return;
		$(this).parent().find("input").attr("value",number+1);
	})


	$(".minus").click(function(){
		// alert($(this).parent().find("input").attr("value") );
		var number = $(this).parent().find("input").attr("value");
		number = Number(number);
		if(number == 0 ) return;
		$(this).parent().find("input").attr("value",number-1);
	})

	$("#neworder").click(function(){

	})

	$("#updateorder").click(function(){
		var bookorder = [];
		var len = $("#booklist tr").size() - 1;
		for(var i = 1; i <= len; ++i )
		{
			if( $("#booklist tr").eq(i).find("td").eq(6).text() == 'done' )
			{
				$("#alert_error").slideDown();
				setTimeout(function(){$("#alert_error").fadeOut(5000);},2000);
				return;
			}

		}
		for(var i = 1; i <= len; ++i )
		{
			// if( document.querySelectorAll("#booklist tr")[i].querySelectorAll("td")[1].querySelector("input").checked )
			
			var book = {};
			book.id = Number($("#booklist tr").eq(i).find("td").eq(0).text());
			book.numbers = Number($("#booklist tr").eq(i).find("td").eq(2).find("input").attr("value"));
			book.state = document.querySelectorAll("#booklist tr")[i].querySelectorAll("td")[1].querySelector("input").checked;
			if (document.querySelector("#order_type").value == "0")
				book.price = Number($("#booklist tr").eq(i).find("td").eq(4).text());
			bookorder.push(book);
			// console.log(book);
		
		}
		
		// console.log(bookorder);
		// alert(JSON.stringify(bookorder));
		$.ajax({
			type:"GET",
			url:"/home/bookorder/update/",
			data:{"order":$("#updateorder").attr("value"),"bookorder":JSON.stringify(bookorder)},
			success:function(msg){
				console.log(msg);
				$("#alert_success").show();
				setTimeout(function(){window.location.reload();},1000);
			}
		})
		
	})

	
	$("#submitorder").click(function(){
		var bookorder = [];
		var len = $("#booklist tr").size() - 1;
		for(var i = 1; i <= len; ++i )
		{
			if( $("#booklist tr").eq(i).find("td").eq(6).text() == 'done' )
			{
				$("#alert_error").slideDown();
				setTimeout(function(){$("#alert_error").fadeOut(5000);},2000);
				return;
			}

		}
		for(var i = 1; i <= len; ++i )
		{
			// if( document.querySelectorAll("#booklist tr")[i].querySelectorAll("td")[1].querySelector("input").checked )
			
			var book = {};
			book.id = Number($("#booklist tr").eq(i).find("td").eq(0).text());
			book.numbers = Number($("#booklist tr").eq(i).find("td").eq(2).find("input").attr("value"));
			book.state = document.querySelectorAll("#booklist tr")[i].querySelectorAll("td")[1].querySelector("input").checked;
			if (document.querySelector("#order_type").value == "0")
				book.price = Number($("#booklist tr").eq(i).find("td").eq(4).text());
			bookorder.push(book);
			// console.log(book);
		
		}
		
		// console.log(bookorder);
		// alert(JSON.stringify(bookorder));
		$.ajax({
			type:"GET",
			url:"/home/bookorder/update/",
			data:{"order":$("#updateorder").attr("value"),"bookorder":JSON.stringify(bookorder)},
			success:function(msg){
				console.log(msg);
				$.ajax({
				type:"GET",
				url:"/home/bookorder/submit/",
				data:{"order":$("#submitorder").attr("value")},
				success:function(msg){
					console.log(msg);
					$("#alert_success").show();
					setTimeout(function(){window.location.reload();},1000);
					}
				})
				
			}
		})
		
	})
	

	$(".ordertype").click(function(){

		$.ajax({
			type:"GET",
			url:"/home/order/",
			data:{"type":$(this).attr("value")},
			success:function(msg){
				console.log(msg);
				window.location.reload();
			}
		})
	})

	$(".addbook").click(function(){
		// alert("ok");
		$.ajax({
			type:"GET",
			url:"/home/bookorder/add/",
			data:{"type":$(this)[0].checked,"book":$(this).parent().parent().find("td").eq(0).text(),"order":$("#orderid").html().split(':')[1].split(' ')[1]},
			success:function(msg){
				console.log(msg);
				// window.location.reload();
			}
		})

	})

	$("#addbooktoorder").click(function(){
		var len = $("#booklist tr").size() - 1;
		for(var i = 1; i <= len; ++i )
		{
			if( $("#booklist tr").eq(i).find("td").eq(6).text() == 'done' )
			{
				$("#alert_error").slideDown();
				setTimeout(function(){$("#alert_error").fadeOut(5000);},2000);
				return;
			}

		}
		window.location.href="/home/bookorder/add/?order="+$(this).attr("value");
	})

	var bgcolor,initvalue;
	$(".modifyprice").mouseover(function(){
		bgcolor	= $(this).css("background-color");
		$(this).css("background-color","rgba(80,180,80,0.5)");
	})
	$(".modifyprice").mouseout(function(){
		$(this).css("background-color",bgcolor);
	})
	$(".modifyprice").focus(function(){
		initvalue = $(this).text();
	})
	$(".modifyprice").blur(function(){
		var  newvalue = $(this).text();
		var patten = new RegExp(/^(([0-9]+\.[0-9]*[1-9][0-9]*)|([0-9]*[1-9][0-9]*\.[0-9]+)|([0-9]*[1-9][0-9]*))$/); 
		if ( patten.test(newvalue) == false )
		{
			alert("ILLEGAL NUMBER!");
			$(this).text(initvalue);
		}
			
	})

}();

})
