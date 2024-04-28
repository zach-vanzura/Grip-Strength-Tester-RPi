var button = $("#move");

button.click(function() {


    $.ajax({
	url: '/process_data',
	method: 'POST',
	data: {num: num1},
	success: function(response) {
	   const out1 = document.getElementById('output1');
	   out1.innerHTML = response.result;
	},
	error: function(xhr, status, error) {
	    console.error('Error:', error);
	}
    });
});
