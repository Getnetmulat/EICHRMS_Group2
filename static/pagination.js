/* Pagination starts here */
  //getPagination('.table-id');
  getPagination('.table-class');
  //getPagination('table');

/*	PAGINATION
- on change max rows select options fade out all rows gt option value mx = 10
- append pagination list as per numbers of rows / max rows option (20row/5= 4pages )
- each pagination li on click -> fade out all tr gt max rows * li num and (10*pagenum 2 = 10 rows)
- fade out all tr lt max rows * li num - max rows ((10*pagenum 2 = 10) - 5)
- fade in all tr between (maxRows*PageNum) and (maxRows*pageNum)- MaxRows
*/


function getPagination(table) {
var lastPage = 1;

$('#maxRows')
.on('change', function(evt) {
//$('.paginationprev').html('');						// reset pagination

lastPage = 1;
$('.pagination')
.find('li')
.slice(1, -1)
.remove();
var trnum = 0; // reset tr counter
var maxRows = parseInt($(this).val()); // get Max Rows from select option

if (maxRows == 5000) {
$('.pagination').hide();
} else {
$('.pagination').show();
}

var totalRows = $(table + ' tbody tr').length; // numbers of rows
$(table + ' tr:gt(0)').each(function() {
// each TR in  table and not the header
trnum++; // Start Counter
if (trnum > maxRows) {
  // if tr number gt maxRows

  $(this).hide(); // fade it out
}
if (trnum <= maxRows) {
  $(this).show();
} // else fade in Important in case if it ..
}); //  was fade out to fade it in
if (totalRows > maxRows) {
// if tr total rows gt max rows option
var pagenum = Math.ceil(totalRows / maxRows); // ceil total(rows/maxrows) to get ..
//	numbers of pages
for (var i = 1; i <= pagenum; ) {
  // for each page append pagination li
  $('.pagination #prev')
    .before(
      '<li class="page-item" data-page="' +
        i +
        '"><a class="page-link">\
          <span>' +
        i++ +
        '<span class="sr-only">(current)</span></span></a>\
        </li>'
    )
    .show();
} // end for i
} // end if row count > max rows
$('.pagination [data-page="1"]').addClass('active'); // add active class to the first li
//SHOWING ROWS NUMBER OUT OF TOTAL DEFAULT
       showig_rows_count(maxRows, 1, totalRows);
        //SHOWING ROWS NUMBER OUT OF TOTAL DEFAULT
$('.pagination li').on('click', function(evt) {
// on click each page
evt.stopImmediatePropagation();
evt.preventDefault();
var pageNum = $(this).attr('data-page'); // get it's number

var maxRows = parseInt($('#maxRows').val()); // get Max Rows from select option

if (pageNum == 'prev') {
  if (lastPage == 1) {
    return;
  }
  pageNum = --lastPage;
}
if (pageNum == 'next') {
  if (lastPage == $('.pagination li').length - 2) {
    return;
  }
  pageNum = ++lastPage;
}

lastPage = pageNum;
var trIndex = 0; // reset tr counter
$('.pagination li').removeClass('active'); // remove active class from all li
$('.pagination [data-page="' + lastPage + '"]').addClass('active'); // add active class to the clicked
// $(this).addClass('active');					// add active class to the clicked

limitPagging();
//SHOWING ROWS NUMBER OUT OF TOTAL
 showig_rows_count(maxRows, pageNum, totalRows);
  //SHOWING ROWS NUMBER OUT OF TOTAL
$(table + ' tr:gt(0)').each(function() {
  // each tr in table not the header
  trIndex++; // tr index counter
  // if tr index gt maxRows*pageNum or lt maxRows*pageNum-maxRows fade if out
  if (
    trIndex > maxRows * pageNum ||
    trIndex <= maxRows * pageNum - maxRows
  ) {
    $(this).hide();
  } else {
    $(this).show();
  } //else fade in
}); // end of for each tr in table
}); // end of on click pagination list
limitPagging();
})
.val(5)
.change();

// end of on select change

// END OF PAGINATION
}

function limitPagging(){
// alert($('.pagination li').length)

if($('.pagination li').length > 7 ){
if( $('.pagination li.active').attr('data-page') <= 3 ){
$('.pagination li:gt(5)').hide();
$('.pagination li:lt(5)').show();
$('.pagination [data-page="next"]').show();
}if ($('.pagination li.active').attr('data-page') > 3){
$('.pagination li:gt(0)').hide();
$('.pagination [data-page="next"]').show();
for( let i = ( parseInt($('.pagination li.active').attr('data-page'))  -2 )  ; i <= ( parseInt($('.pagination li.active').attr('data-page'))  + 2 ) ; i++ ){
$('.pagination [data-page="'+i+'"]').show();

}

}
}
}

$(function() {
// Just to append id number for each row
$('table tr:eq(0)').prepend('<th> # </th>');

var id = 0;

$('table tr:gt(0)').each(function() {
id++;
$(this).prepend('<td>' + id + '</td>');
});
});


//end of pagination */


//ROWS SHOWING FUNCTION
function showig_rows_count(maxRows, pageNum, totalRows) {
   //Default rows showing
        var end_index = maxRows*pageNum;
        var start_index = ((maxRows*pageNum)- maxRows) + parseFloat(1);
        var string = ' ከጠቅላላ ' + totalRows + ' መረጃዎች ' + ' ከ' + start_index  + ' - ' + end_index + ' በማሳየት ላይ ';
        $('.rows_count').html(string);
}
// JS for  Search Table data

function search() {

// Count td if you want to search on all table instead of specific column

  var count = $('.table').children('tbody').children('tr:first-child').children('td').length;

        // Declare variables
  var input, filter, table, tr, td, i;
  input = document.getElementById("searchInput");
  var input_value =  document.getElementById("searchInput").value;
    filter = input.value.toLowerCase();
  if(input_value !=''){
        table = document.getElementById("myTable");
        tr = table.getElementsByTagName("tr");

        // Loop through all table rows, and hide those who don't match the search query
        for (i = 1; i < tr.length; i++) {

          var flag = 0;

          for(j = 0; j < count; j++){
            td = tr[i].getElementsByTagName("td")[j];
            if (td) {

                var td_text = td.innerHTML;
                if (td.innerHTML.toLowerCase().indexOf(filter) > -1) {
                  flag = 1;
                } else {
                  //DO NOTHING
                }
              }
            }
          if(flag==1){
            tr[i].style.display = "";
            break;
          }else {
             tr[i].style.display = "none";
          }
        }
    }else {
      //RESET TABLE
      $('#maxRows').trigger('change');
    }
}

// end of search