let last_collapse = 0;
let date = new Date();

$('.collapse').collapse();

$(function() {
    $( "#pay-date" ).datepicker({
        dateFormat : "dd/mm/yy",
        currentText: "Now"
    });
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

async function user_payment_commit(user_data)
{
    let response = await
        fetch(window.location.origin + '/API/add_user_payment', {
            method : 'POST', 
            headers: {'Content-Type': 'application/json'},
            body : user_data})
    
    let data = await response.json()
    
    console.log(data);
}

async function user_edit_commit(user_data)
{
    let response = await
    fetch(window.location.origin + '/API/edit_user', {
        method : 'POST',
        headers: {'Content-Type': 'application/json'},
        body : user_data});

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
async function PaymentModalForUser(user_id) {
    // Get payment form elements
    let user = await get_user_by_id(user_id);
    console.log(user);

    var current_date = date.getDate() + "/" + (date.getMonth() + 1) + "/" + date.getFullYear();
    console.log(current_date);

    $("#pay-userid").val(user["id"]);
    $("#pay-name").val(user["name"]);
    $("#pay-date").val(current_date);
    $("#pay-confirm").click(save_user_payment);
    
    $("#PaymentModal").modal("show");
    
}

async function save_user_payment() {

    let date = new Date;
    date.parse($("#pay-date").val());
    console.log(date);

    let user_data = JSON.stringify({
        user_id : $("#pay-userid").val(),
        date    : date.getFullYear() + "-" + (date.getMonth() + 1) + "-" + date.getDate(),
        value   : $("#pay-value").val(),
        discount: $("#pay-discount").val()
    });
    console.log(user_data);
    // await  user_payment_commit(user_data);

    $("#PaymentModal").modal("hide");
    // location.reload();
}

// Customize edit modal to display user information and payments
async function EditModalForUser(user_id) {

    let user = await get_user_by_id(user_id);

    $("#edit-userid").val(user["id"])
    $("#edit-name").val(user["name"]);
    $("#edit-email").val(user["email"]);
    $("#edit-area").val(user["area"]);

    $("#edit-confirm").click(save_user_edit);

    $("#EditModal").modal("show");
    
}

async function save_user_edit() {

    let user_data = JSON.stringify({
        id      : $("#edit-userid").val(),
        name    : $("#edit-name").val(),
        email   : $("#edit-email").val(),
        area    : $("#edit-area").val() 
    });
    
    console.log(user_data);

    await user_edit_commit(user_data);

    $("#EditModal").modal("hide");
    location.reload();
}

// Get all buttons of the collapsable rows to bind the event listeners
function row_buttons_events() 
{
    let rows_id = document.getElementsByClassName("col-id");
    
    for (let index = 0; index < rows_id.length; index++) {
        let user_id = rows_id[index].innerHTML.trim();
        
        var ShowPayModal_Event = function(){ PaymentModalForUser(user_id) };
        var ShowEditModal_Event = function(){ EditModalForUser(user_id) };

        //Add event for each button in rows
        $("#pay-" + user_id).click(ShowPayModal_Event.bind(user_id));
        $("#edit-" + user_id).click(ShowEditModal_Event.bind(user_id));

    }
}

document.addEventListener('DOMContentLoaded', (event) => {
    // Add event listeners
    row_buttons_events();

  });