document.addEventListener("DOMContentLoaded", function(event) {

  const showNavbar = (toggleId, navId, bodyId, headerId) =>{
  const toggle = document.getElementById(toggleId),
  nav = document.getElementById(navId),
  bodypd = document.getElementById(bodyId),
  headerpd = document.getElementById(headerId)
  
  if(toggle && nav && bodypd && headerpd){
  toggle.addEventListener('click', ()=>{
  nav.classList.toggle('show')
  toggle.classList.toggle('bx-x')
  bodypd.classList.toggle('body-pd')
  headerpd.classList.toggle('body-pd')
  })
  }
  }
  
  showNavbar('header-toggle','nav-bar','body-pd','header')
  
  const linkColor = document.querySelectorAll('.nav_link')
  
  function colorLink(){
  if(linkColor){
  linkColor.forEach(l=> l.classList.remove('active'))
  this.classList.add('active')
  }
  }
  linkColor.forEach(l=> l.addEventListener('click', colorLink))
  
  });


  /* Show unread Notification   */
  $('#js-notification-menu').on('click', function(e) {
  if ($(e.target).parent('div').get(0) === $(this).get(0)
      || $(e.target).parent('svg').parent('div').get(0) === $(this).get(0)
      || $(e.target).get(0) === $(this).get(0)
  ) {
    $(this).toggleClass('notifications-visible');    
  }
});

$('.notification-remove').on('click', function() {
  if ($(this).parents('ul').find('li').length === 1) {
    $(this).parent()
      .removeClass('important unread')
      .html('Keine Benachrichtigungen mehr vorhanden.');
    $('#js-notification-menu').removeClass('notifications-unread');
    $('.notifications-count').remove();
  } else {
    $(this).parent().remove();
    $('.notifications-count').text($('#js-notification-menu li').length);
  }
});

/* end unread notification */

  
//start of multiple form registration javasript //
$(document).ready(function(){

  var current_fs, next_fs, previous_fs; //fieldsets
  var opacity;
  var current = 1;
  var steps = $("fieldset").length;

  setProgressBar(current);

  $(".next").click(function(){

  current_fs = $(this).parent();
  next_fs = $(this).parent().next();

  //Add Class Active
  $("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");

  //show the next fieldset
  next_fs.show();
  //hide the current fieldset with style
  current_fs.animate({opacity: 0}, {
  step: function(now) {
  // for making fielset appear animation
  opacity = 1 - now;

  current_fs.css({
  'display': 'none',
  'position': 'relative'
  });
  next_fs.css({'opacity': opacity});
  },
  duration: 500
  });
  setProgressBar(++current);
  });

  $(".previous").click(function(){

  current_fs = $(this).parent();
  previous_fs = $(this).parent().prev();

  //Remove class active
  $("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");

  //show the previous fieldset
  previous_fs.show();

  //hide the current fieldset with style
  current_fs.animate({opacity: 0}, {
  step: function(now) {
  // for making fielset appear animation
  opacity = 1 - now;

  current_fs.css({
  'display': 'none',
  'position': 'relative'
  });
  previous_fs.css({'opacity': opacity});
  },
  duration: 500
  });
  setProgressBar(--current);
  });

  function setProgressBar(curStep){
  var percent = parseFloat(100 / steps) * curStep;
  percent = percent.toFixed();
  $(".progress-bar")
  .css("width",percent+"%")
  }

  $(".submit").click(function(){
  return false;
  })

  });
//end of multiple form registration javasript //

$('.message a').click(function(){
   $('form').animate({height: "toggle", opacity: "toggle"}, "slow");
});



// JS for Tab navigation
function openTab(zoneName) {
  var i;
  var x = document.getElementsByClassName("tab-name");
  for (i = 0; i < x.length; i++) {
      x[i].style.display = "none";
  }
  document.getElementById(zoneName).style.display = "block";
  }


/* JS for adding new field */

$(document).ready(function() {
  var max_fields = 10;
  var wrapper = $(".container1");
  var add_button = $(".add_form_field");
  var x = 1;

  $(add_button).click(function(e) {
      e.preventDefault();
      if (x < max_fields) {
          x++;
          $(wrapper).append('<div><input type="text" name="newFieldText[]" required/><a href="#" class="btn float-end btn-danger delete">x</a></div>'); //add input box
      } else {
          alert('ይቅርታ! ከተፈቀድልዎ በላይ መጨመር አይችሉም።')
      }
  });

  $(wrapper).on("click", ".delete", function(e) {
      e.preventDefault();
      $(this).parent('div').remove();
      x--;
  })
  });

  // JS for checking checkbox is checked in table
$(document).ready(function(){
$(".tableCheck #checkall").click(function () {
        if ($(".tableCheck #checkall").is(':checked')) {
            $(".tableCheck input[type=checkbox]").each(function () {
                $(this).prop("checked", true);
            });

        } else {
            $(".tableCheck input[type=checkbox]").each(function () {
                $(this).prop("checked", false);
            });
        }
    });

    $("[data-bs-toggle=tooltip]").tooltip();
});

/* return message if at least one checkbox is not checked by the user  */

$(document).ready(function(){
    $("#checkedDelete").click(function(){
 if ($('input:checkbox').filter(':checked').length < 1){
        alert("ቢያንስ አንድ ሳጥን አመልክት!");

 return false;
 }
    });
});


/* Modal JS */
// Get the modal
// Get the modal
var modal = document.getElementById("modalAdd");

// Get the button that opens the modal
var btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("btn-close")[0];

// When the user clicks the button, open the modal
btn.onclick = function() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

/* When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}*/
// disable background click

$(document).ready(function(){
    $(".show-modal").click(function(){
        $("#modalAdd").modal({
            backdrop: 'static',
            keyboard: false
        });

    });
});


/* JS for editing table row live */
$(document).ready(function(){

 // Show Input element
 $('.edit').click(function(){
  $('.txtEdit').hide();
  $(this).next('.txtEdit').show().focus();
  $(this).hide();
 });

 // Save data
 $(".txtEdit").focusout(function(){

  // Get edit id, field name and value
  var id = this.id;
  var split_id = id.split("_");
  var field_name = split_id[0];
  var edit_id = split_id[1];
  var value = $(this).val();

  // Hide Input element
  $(this).hide();

  // Hide and Change Text of the container with input elmeent
  $(this).prev('.edit').show();
  $(this).prev('.edit').text(value);

  $.ajax({
   url: '/update',
   type: 'post',
   data: { field:field_name, value:value, id:edit_id },
   success:function(response){
      if(response == 1){
         console.log('Save successfully');
      }else{
         console.log("Not saved.");
      }
   }
  });

 });

});

// table search function
// Light Javascript Table Filter
// -by Chris Coyier
(function(document) {
	'use strict';
	var LightTableFilter = (function(Arr) {
		var _input;
		function _onInputEvent(e) {
			_input = e.target;
			var tables = document.getElementsByClassName(_input.getAttribute('data-table'));
			Arr.forEach.call(tables, function(table) {
				Arr.forEach.call(table.tBodies, function(tbody) {
					Arr.forEach.call(tbody.rows, _filter);
				});
			});
		}
		function _filter(row) {
			var text = row.textContent.toLowerCase(), val = _input.value.toLowerCase();
			row.style.display = text.indexOf(val) === -1 ? 'none' : 'table-row';
		}
		return {
			init: function() {
				var inputs = document.getElementsByClassName('table-filter');
				Arr.forEach.call(inputs, function(input) {
					input.oninput = _onInputEvent;
				});
			}
		};
	})(Array.prototype);

	document.addEventListener('readystatechange', function() {
		if (document.readyState === 'complete') {
			LightTableFilter.init();
		}
	});
})(document);

/* JS for searching from table */

function searchFunction() {
    // Declare variables
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("searchInput");
    filter = input.value.toUpperCase();
    table = document.getElementById("myTable");
    tr = table.getElementsByTagName("tr");
    td = table.getElementsByTagName("td")

    // Loop through all table rows, and hide those who don't match the search query
    for (i = 1; i < tr.length; i++) {
        // Hide the row initially.
        tr[i].style.display = "none";

        td = tr[i].getElementsByTagName("td");
        for (var j = 0; j < td.length; j++) {
          cell = tr[i].getElementsByTagName("td")[j];
          if (cell) {
            if (cell.innerHTML.toUpperCase().indexOf(filter) > -1) {
              tr[i].style.display = "";
              break;

            }

          }
        }
    }
  //getPagination('.table-id');
}

// JS for auto delete alert message dialog after 3 seconds

$(function() {

  // Hide the hidden sections.
  // Use JS to do this in case the user doesn't have JS
  // enabled.
  $('.hidden').hide();

  // Setup an event listener for each trigger checkbox that
  // fires when the state of the checkbox changes.
  $('.trigger').change(function() {
   	// Get the ID of the hidden area from the data-trigger
    // attribute.
    var hiddenId = $(this).attr("data-trigger");

    // Check to see if the checkbox is checked.
    // If it is, show the fields and populate the input.
    // If not, hide the fields.
    if ($(this).is(':checked')) {
      // Show the hidden fields.
      $("#" + hiddenId).show();
    } else {
      // Make sure that the hidden fields are indeed
      // hidden.
      $("#" + hiddenId).hide();

      // You may also want to clear the value of the
      // hidden fields here. Just in case somebody
      // shows the fields, enters data to them and then
      // unticks the checkbox.
      //
      // This would do the job:
      //
      // $("#hidden_field").val("");
    }
  });
});

// Password change modal js
function openForm() {
  document.getElementById("changePass").style.display = "block";
}

function closeForm() {
  document.getElementById("changePass").style.display = "none";
}

// JS for auto closing flash message
$("#alert-success").fadeTo(2000, 500).slideUp(500, function(){
    $("#alert-success").slideUp(500);
});

// Animated barchart for displaying percentage
$(document).ready(function() {
	$('.percentage-bar').each(function(){
		$(this).find('.bar').animate({
			width: $(this).attr('data-percent')
		}, 6000);
	});
});

function createPDF() {
  var sTable = document.getElementById('tab').innerHTML;

  var style = "<style>";
  style = style + "table {width: 100%;font: 17px Calibri;}";
  style = style + "table, th, td {border: solid 1px #DDD; border-collapse: collapse;";
  style = style + "padding: 2px 3px;text-align: center;}";
  style = style + "</style>";

  // CREATE A WINDOW OBJECT.
  var win = window.open('', '', 'height=700,width=700');

  win.document.write('<html><head>');
  win.document.write('<title>የብልፅግና ፓርቲ አመራሮችና አባላት የአባልነት ክፍያ ወርኃዊ እና ዓመታዊ መዋጮ </title>');   // <title> FOR PDF HEADER.
  win.document.write(style);          // ADD STYLE INSIDE THE HEAD TAG.
  win.document.write('</head>');
  win.document.write('<body>');
  win.document.write(sTable);         // THE TABLE CONTENTS INSIDE THE BODY TAG.
  win.document.write('</body></html>');

  win.document.close(); 	// CLOSE THE CURRENT WINDOW.

  win.print();    // PRINT THE CONTENTS.
}

/* convert page to pdf */
function generatePDF() {
  var doc = new jsPDF();  //create jsPDF object
   doc.fromHTML(document.getElementById("test"), // page element which you want to print as PDF
   15,
   15, 
   {
     'width': 170  //set width
   },
   function(a) 
    {
     doc.save("HTML2PDF.pdf"); // save file name as HTML2PDF.pdf
   });
 }

 /* JS- to handle max file size */
 function upload_check()
{
    var upl = document.getElementById("file_id");

    if(upl.files[0].size > 1000000000)
    {
       alert("የፋይል መጠኑ ከ10 ሜጋ ባይት ይበልጣል! እባክዎ መጠኑን ይቀንሱ?");
       upl.value = "";
    }
};