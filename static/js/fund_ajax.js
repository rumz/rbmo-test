function getAllocBudget(){
    $.get('/agency/fund/get_budget',
	  {'activity_id' : $('#id_activity').val(),
	   'month'       : $('#id_month').val()
	  },
	  function(data){
	      var amount_bal = JSON.parse(data)
	      $('#budget').html(amount_bal.amount);
	      $('#balance').html(amount_bal.balance);
	  }
	 );
}

$('#id_month').change(function(){
    getAllocBudget();    
});


function viewFundStatDetails(agency, year, allocation){
    $.get('/agency/fund/view_fstat_detail', 
	  {'agency_id' : agency,
	   'year'      : year,
	   'allocation': allocation
	  },
	  function(data){
	     $('#fund_stat_detail').html(data);
	  }
	 );
}

$(document).ready(
    function(){
	viewFundStatDetails(1, 2014, 'PS');
    }
);
