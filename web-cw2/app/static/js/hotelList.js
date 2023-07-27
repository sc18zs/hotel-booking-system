// check in and check out time control
$(function() {
    $( "#datepicker_start" ).datepicker({
      defaultDate: "+1w",
      changeMonth: true,
      changeYear: true,
      minDate: 0,
      dateFormat: "yy-mm-dd",
      onClose: function( selectedDate ) {
        $( "#datepicker_end" ).datepicker( "option", "minDate", selectedDate );
      }
    });
    $( "#datepicker_end" ).datepicker({
      defaultDate: "+1w",
      changeMonth: true,
      changeYear: true,
      dateFormat: "yy-mm-dd",
      onClose: function( selectedDate ) {
        $( "#datepicker_start" ).datepicker( "option", "maxDate", selectedDate );
      }
    });
  });


// form validation
function validateForm()
{
  var x=document.forms["search-form"]["check-in"].value;
  if (x==null || x=="")
  {
    alert("Please enter the check-in time.");
    return false;
  }
}

// show the login warning
function loginFirst()
{
  alert("Please login first.");
}



// form validation
function dateFill()
{
  var x=document.forms["detail-form"]["check-in"].value;
  var y=document.forms["detail-form"]["check-out"].value;
  if (x==null || x=="")
  {
    alert("Please enter the check-in and check-out time to search results.");
    return false;
  }
  if (y==null || y=="")
  {
    alert("Please enter the check-in and check-out time to search results.");
    return false;
  }
}