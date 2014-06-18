function getSchedules(section_id){
    var url = '/scheduling/get_schedules';
    $('#section_id').val(section_id);
    $.get(url, {id:section_id}, function(data){
	$("#sched_panel_id").html(data);
    });
}

function removeSched(sched_id){
    var conf = confirm("Are you sure to delete this schedule?");

    if (conf){
	$.ajax({
	    data : {'sched_id':sched_id},
	    url : '/scheduling/remove_get_sched',
	    type : 'GET',
	    success : function(data){
		$("#sched_panel_id").html(data);
	    },
	    error : function(data){
		alert('Cannot delete schedule. Technical Error Occur');
	    }	
	});
    }
}

function addGetSchedules(){
    $('#id_alert').removeClass();
    var inputs = {'section_id': $('#section_id').val(),
		  'subject': $('#id_subject').val(),
		  'teacher': $('#id_teacher').val(),
		  'time_start': $('#id_time_start').val(),
		  'time_end': $('#id_time_end').val(),
		  'day': $('#id_day').val()
		 }
    $.ajax({
	data: inputs,
	type: 'GET',
	url: '/scheduling/set_get_schedules',
	success: function(data){
	    rs_data = new String(data).trim();

	    if(rs_data == 'Error'){
		$('#id_alert').addClass('alert alert-danger');
		$('#id_alert').html('Error Occur');
	    }else if(rs_data == 'Duplicate'){
		$('#id_alert').addClass('alert alert-danger');
		$('#id_alert').html('Schedule currently taken');
	    }else{
		$('#sched_panel_id').html(data);
		$('.close').click();
	    }

	},
	error: function(data){
	    alert(data);
	}
    });
}

$().ready(function(){
    $('#all_year').click();   
});

$('#all_year').click(function(){
    $('.year_level_class').prop('checked', this.checked);
});

function getSubjects(section_id){
    $.get('/scheduling/subject_for_section', {'section_id':section_id}, 
	  function(data){
	    $('#subject_field').html(data);
	  }
	 );
}


function viewSubjectInfo(subject_id){
    $.ajax({
	data : {'subject_id': subject_id},
	url : '/scheduling/get_subject_info',
	type : 'GET',
	success: function(data){
	    $('#subject_info_id').html(data);
	}
    });
}

function checkSectionAction(){
    /*
      before redirecting or taking an action
      this function checks whether the action is edit or delete
     */
    if ($('action').val()=='del'){
	return false;
    }else{
	return true;
    }
}