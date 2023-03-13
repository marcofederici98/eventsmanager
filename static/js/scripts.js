$(document).ready(function() {
    $('#submit-btn').on('click', function() {
      var checkedRows = [];

      $('#myTable tbody tr').each(function() {
        var row = $(this);
        var checkbox = row.find('input[type=checkbox]');
        if (checkbox.prop('checked')) {
          checkedRows.push({
            column1: row.find('td:eq(0)').text(),
            column2: row.find('td:eq(1)').text(),
            column3: row.find('td:eq(2)').text()
          });
        }
      });

      $.ajax({
        type: 'POST',
        url: '/submit-form',
        data: JSON.stringify(checkedRows),
        contentType: 'application/json;charset=UTF-8',
        success: function(response) {
          console.log(response)
          console.log(checkedRows)

          window.location.href = "/success";
        },
        error: function(xhr, status, error) {
          console.log(xhr.responseText);
        }
      });
    });
});


function myFunction() {
    // Declare variables
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    table = document.getElementById("myTable");
    tr = table.getElementsByTagName("tr");
  
    // Loop through all table rows, and hide those who don't match the search query
    for (i = 0; i < tr.length; i++) {
      td = tr[i].getElementsByTagName("td")[1];
      if (td) {
        txtValue = td.textContent || td.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
          tr[i].style.display = "";
        } else {
          tr[i].style.display = "none";
        }
      }
    }
}