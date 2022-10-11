let last_collapse = 0;

$('.collapse').collapse();
$(".date").datepicker({
    format: "dd-mm-yyyy",
  });

// Toggle collapsable element by its id
function toggle_collapse(id)
{
    if (last_collapse)
    {
        $('#'+last_collapse).collapse('hide');
    }

    $('#'+id).collapse('toggle');
    last_collapse = id;
}

async function user_payment(user_id)
{
    let response = await
        fetch(window.location.origin + '/API/add_user_payment', {
            method : 'POST', 
            headers: {'Content-Type': 'application/json'},
            body : JSON.stringify({id : user_id})})
    
    let data = await response.json()
    
    console.log(data);
}

async function user_edit(user_id)
{
    let response = await
    fetch(window.location.origin + '/API/edit_user', {
        method : 'POST',
        headers: {'Content-Type': 'application/json'},
        body : JSON.stringify({id : user_id})})

    let data = await response.json()
    
    console.log(data);
}

// Get all buttons of the collapsable rows to bind the event listeners
function row_buttons_events() 
{
    let rows_id = document.getElementsByClassName("col-id");
    
    for (let index = 0; index < rows_id.length; index++) {
        let user_id = rows_id[index].innerHTML.trim();
        
        //Get buttons
        const PaymentButton = document.getElementById("pay-" + user_id);
        const EditButton = document.getElementById("edit-" + user_id);

        var PaymentEvent = function() {
            user_payment(user_id);
        }

        var EditEvent = function() {
            user_edit(user_id);
        }

        PaymentButton.addEventListener('click', PaymentEvent.bind(user_id));
        EditButton.addEventListener('click', EditEvent.bind(user_id));
    }
}

document.addEventListener('DOMContentLoaded', (event) => {
    // Add event listeners
    row_buttons_events();

  });