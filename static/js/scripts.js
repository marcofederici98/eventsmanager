$(document).ready(function() {
    $('#submit-btn').on('click', function() {
      var checkedRows = [];

      $('#myTable tbody tr').each(function() {
        var row = $(this);
        var checkbox = row.find('input[type=checkbox]');
        if (checkbox.prop('checked')) {
          checkedRows.push({
            column1: row.find('td:eq(0)').text(),
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


function search() {
    var input, filter, table, tr, td, i, txtValue, txtValue1, txtValue2;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    table = document.getElementById("myTable");
    tr = table.getElementsByTagName("tr");
    
    for (i = 0; i < tr.length; i++) {
      td = tr[i].getElementsByTagName("td");
      if (td[1]) {
        txtValue = td[0].textContent || td[0].innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
          tr[i].style.display = "";
        } else {
          tr[i].style.display = "none";
        }
      }
    }
}