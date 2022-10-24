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

async function user_payment_commit(user_id)
{
    let response = await
        fetch(window.location.origin + '/API/add_user_payment', {
            method : 'POST', 
            headers: {'Content-Type': 'application/json'},
            body : JSON.stringify({id : user_id})})
    
    let data = await response.json()
    
    console.log(data);
}

async function user_edit_commit(user_id)
{
    let response = await
    fetch(window.location.origin + '/API/edit_user', {
        method : 'POST',
        headers: {'Content-Type': 'application/json'},
        body : JSON.stringify({id : user_id})})

    let data = await response.json()
    
    console.log(data);
}

async function get_user_by_id(user_id)
{
    let response = await fetch(window.location.origin + '/API/get_user_by_id', {
        method : 'POST',
        headers: {'Content-Type': 'application/json'},
        body : JSON.stringify({id : user_id})})

    let data = await response.json();

    return data;    
}

// Edit payment modal to display payment information
async function PaymentEvent(user_id) {
    // Get payment form elements
    let user = await get_user_by_id(user_id);
    console.log(user);
    
    $("#pay-name").val(user["name"]);
    $("#pay-date").val("26/01/1998");

    $("#PaymentModal").modal("show");

    user_payment_commit(user_id);
}

// Customize edit modal to display user information and payments
async function EditEvent(user_id) {

    let user = await get_user_by_id(user_id);

    $("#edit-name").val(user["name"]);
    $("#EditModal").modal("show");
    user_edit_commit(user_id);
}

// Get all buttons of the collapsable rows to bind the event listeners
function row_buttons_events() 
{
    let rows_id = document.getElementsByClassName("col-id");
    
    for (let index = 0; index < rows_id.length; index++) {
        let user_id = rows_id[index].innerHTML.trim();
        
        var payEvent = function(){ PaymentEvent(user_id) };
        var editEvent = function(){ EditEvent(user_id) };

        //Get buttons
        const PaymentButton = document.getElementById("pay-" + user_id);
        const EditButton = document.getElementById("edit-" + user_id);

        PaymentButton.addEventListener('click', payEvent.bind(user_id));
        EditButton.addEventListener('click', editEvent.bind(user_id));
    }
}

document.addEventListener('DOMContentLoaded', (event) => {
    // Add event listeners
    row_buttons_events();

  });