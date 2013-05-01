
$(document).ready(function(){

var Home = function(){

	$("#booklist").stupidtable();

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
			// if( document.querySelectorAll("#booklist tr")[i].querySelectorAll("td")[1].querySelector("input").checked )
			
			var book = {};
			book.id = Number($("#booklist tr").eq(i).find("td").eq(0).text());
			book.numbers = Number($("#booklist tr").eq(i).find("td").eq(2).find("input").attr("value"));
			book.state = document.querySelectorAll("#booklist tr")[i].querySelectorAll("td")[1].querySelector("input").checked;
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
				window.location.reload();
			}
		})
		
	})

	
	$("#submitorder").click(function(){
		var bookorder = [];
		var len = $("#booklist tr").size() - 1;
		for(var i = 1; i <= len; ++i )
		{
			// if( document.querySelectorAll("#booklist tr")[i].querySelectorAll("td")[1].querySelector("input").checked )
			
			var book = {};
			book.id = Number($("#booklist tr").eq(i).find("td").eq(0).text());
			book.numbers = Number($("#booklist tr").eq(i).find("td").eq(2).find("input").attr("value"));
			book.state = document.querySelectorAll("#booklist tr")[i].querySelectorAll("td")[1].querySelector("input").checked;
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
					window.location.reload();
					}
				})
				
			}
		})
		
	})
	

	$(".ordertype").click(function(){
		$.ajax({
			type:"GET",
			url:"/home/order/",
			data:{"type":$(this).text()},
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

}();

})
