$('#gen_stud_id_btn').click(function(){
    $.ajax({
	url : '/registration/generate_student_id',
	
	dataType : 'html',
	success : function(data){
	    $("#id_studentID").val(data);
	}
    });
});

$("#id_studentID").keydown(function(e){
    return allNumbers(e);
});
