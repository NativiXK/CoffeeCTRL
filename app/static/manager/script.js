let last_collapse = 0;
let date = new Date();

$('.collapse').collapse();

$(function() 
{
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
    
}

async function user_edit_commit(user_data) 
{
    let response = await
    fetch(window.location.origin + '/API/edit_user', {
        method : 'POST',
        headers: {'Content-Type': 'application/json'},
        body : user_data});

    let data = await response.json()
    
}

async function new_user_commit(user_data) 
{
    let response = await
    fetch(window.location.origin + '/API/add_new_user', {
        method : 'POST',
        headers: {'Content-Type': 'application/json'},
        body : user_data});

    let data = await response.json()
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

    var current_date = date.getDate() + "/" + (date.getMonth() + 1) + "/" + date.getFullYear();

    $("#pay-userid").val(user["id"]);
    $("#pay-name").val(user["name"]);
    $("#pay-date").val(current_date);
    $("#pay-confirm").click(save_user_payment);
    
    $("#PaymentModal").modal("show");
    
}

async function save_user_payment() 
{

    let user_data = JSON.stringify({
        user_id : $("#pay-userid").val(),
        date    : $("#pay-date").val(),
        value   : $("#pay-value").val(),
        discount: $("#pay-discount").val()
    });
    
    await  user_payment_commit(user_data);

    $("#PaymentModal").modal("hide");
    location.reload();
}

// Customize edit modal to display user information and payments
async function EditModalForUser(user_id) 
{
    console.log(user_id);
    if (typeof user_id !== "undefined")
    {
       let user = await get_user_by_id(user_id);

        $("#EditModal-title").text("EDIT");
        $("#edit-userid").val(user["id"]);
        $("#edit-name").val(user["name"]);
        $("#edit-email").val(user["email"]);
        $("#edit-area").val(user["area"]);

        $("#edit-confirm").unbind('click');
        $("#edit-confirm").click(save_user_edit); 
    }
    else // Show add modal
    {
        $("#EditModal-title").text("ADD NEW USER");
        $("#edit-userid").val("");
        $("#edit-name").val("");
        $("#edit-email").val("");
        $("#edit-area").val("");

        $("#edit-confirm").unbind('click');
        $("#edit-confirm").click(add_new_user);
    }
    
    $("#EditModal").modal("show");
    
}

async function save_user_edit() 
{

    let user_data = JSON.stringify({
        id      : $("#edit-userid").val(),
        name    : $("#edit-name").val(),
        email   : $("#edit-email").val(),
        area    : $("#edit-area").val() 
    });

    await user_edit_commit(user_data);

    $("#EditModal").modal("hide");
    location.reload();
}

async function add_new_user() 
{

    let user_data = JSON.stringify({
        name    : $("#edit-name").val(),
        email   : $("#edit-email").val(),
        area    : $("#edit-area").val() 
    });

    await new_user_commit(user_data);

    $("#EditModal").modal("hide");
    location.reload();

}

async function RemoveUserById(user_id)
{
    if (confirm("Do you really want to remove this user?"))
    {
            let user_data = JSON.stringify({
                user_id : user_id
            });
        
            let response = await fetch("/API/remove_user_by_id", {
                method : 'POST',
                headers: {'Content-Type': 'application/json'},
                body : user_data});
        
            let data = await response.json();
            window.location.reload();
    }
}

// Get all buttons of the collapsable rows to bind the event listeners
function row_buttons_events() 
{
    let rows_id = document.getElementsByClassName("col-id");
    
    for (let index = 0; index < rows_id.length; index++) {
        let user_id = rows_id[index].innerHTML.trim();
        
        var ShowPayModal_Event = function(){ PaymentModalForUser(user_id) };
        var ShowEditModal_Event = function(){ EditModalForUser(user_id) };
        var RemoveUser = function() { RemoveUserById(user_id) };

        //Add event for each button in rows
        $("#pay-" + user_id).click(ShowPayModal_Event.bind(user_id));
        $("#edit-" + user_id).click(ShowEditModal_Event.bind(user_id));
        $("#remove-" + user_id).click(RemoveUser.bind(user_id));

    }
}

function update_payment_total()
{
    let value = parseFloat($("#pay-value").val());
    let discount = parseFloat($("#pay-discount").val());
    
    $("#pay-total").val("R$ " + (value - discount));
}

document.addEventListener('DOMContentLoaded', (event) => {
    $("#btn-logout").click(
        function() {
            window.location.href='auth/logout';
        }
    );
    
    $("#btn-add-person").click(
        function() {
            EditModalForUser();
        }
    );
    
    $("#pay-value").change(
        function() {
            update_payment_total();
        }
    )

    $("#pay-discount").change(
        function() {
            update_payment_total();
        }
    )


    // Add event listeners
    row_buttons_events();

  });