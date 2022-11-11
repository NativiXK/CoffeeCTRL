let last_collapse = 0;
let date = new Date();

$('.collapse').collapse();

$(function() 
{
    $( ".datepicker" ).datepicker({
        dateFormat : "dd/mm/yy",
        currentText: "Now"
    });
});

// Toggle collapsable element by its id
function toggle_collapse(id)
{

    $('#'+last_collapse).collapse('hide');

    $('#'+id).collapse('show');
    last_collapse = id;
}

function toMonthName(monthNumber) 
    {
        const date = new Date();
        date.setMonth(monthNumber - 1);

        return date.toLocaleString('en-US', {
        month: 'long',
        });
    }

function confirmSubmit()
{
    var agree=confirm("Are you sure you wish to continue?");
    if (agree)
        return true ;
    else
        return false ;
}

async function API_UserPaymentCommit(user_data) 
{
    let response = await
        fetch(window.location.origin + '/API/add_user_payment', {
            method : 'POST', 
            headers: {'Content-Type': 'application/json'},
            body : user_data})
    
    let data = await response.json()
    
}

async function API_UserEditCommit(user_data) 
{
    let response = await
    fetch(window.location.origin + '/API/edit_user', {
        method : 'POST',
        headers: {'Content-Type': 'application/json'},
        body : user_data});

    let data = await response.json()
    
}

async function API_NewUserCommit(user_data) 
{
    let response = await
    fetch(window.location.origin + '/API/add_new_user', {
        method : 'POST',
        headers: {'Content-Type': 'application/json'},
        body : user_data});

    let data = await response.json()
}

async function API_GetUserById(user_id)
{
    let response = await fetch(window.location.origin + '/API/get_user_by_id', {
        method : 'POST',
        headers: {'Content-Type': 'application/json'},
        body : JSON.stringify({id : user_id})})

    let data = await response.json();

    return data;    
}

async function API_RemoveUserById(user_id)
{
    let user_data = JSON.stringify({
        user_id : user_id
    });

    let response = await fetch("/API/remove_user_by_id", {
        method : 'POST',
        headers: {'Content-Type': 'application/json'},
        body : user_data});

        return await response.json();
}

async function API_GetReport(type, month)
{
    let report;
    let data;

    if (type === "income" || type === "spent" || type === "total")
    {
        data = JSON.stringify({
            type : type,
            month : month
        });
    }
    else
    {
        return null;
    }

    let response = await fetch("/API/cash_report", {
        method : 'POST',
        headers: {'Content-Type': 'application/json'},
        body : data});

    report = await response.json();

    return report;
}

async function API_GetModal(modal, parameters)
{
    /*
    Must receive the modal type name to be built in the server and returned.
    Available modals types:
    [
        "purchase"      -> Returns a custom modal to add a purchase log
        "coffee"        -> Returns a custom modal to configurate coffee parameters such as monthly price, date of charge
        "user_payments" -> Returns a custom modal to modify user payments
    ]

    */
    data = JSON.stringify({
        type : modal,
        parameters : parameters
    });

    let response = await fetch("/API/get_modal", {
        method : 'POST',
        headers: {'Content-Type': 'application/json'},
        body : data});

    modal = await response.json();
    console.log(modal);
    return modal;
}

async function OpenPurchaseModal()
{
    let modal = await API_GetModal("purchase");

    $(modal["html"]).appendTo("body");
    $("#PurchaseModal").modal("show");

    $('#PurchaseModal').on('hidden.bs.modal', function (e) {
        $("#PurchaseModal").remove();
      })
    
    $( ".datepicker" ).datepicker({
        dateFormat : "dd/mm/yy",
        currentText: "Now"
    });

}

async function PaymentsModalForUser(user_id)
{
    let modal = await API_GetModal("user-payments", {user_id : user_id});

    $(modal["html"]).appendTo("body");
    $("#UserPaymentsModal").modal("show");

    $('#UserPaymentsModal').on('hidden.bs.modal', function (e) {
        $("#UserPaymentsModal").remove();
      })
    
    $( ".datepicker" ).datepicker({
        dateFormat : "dd/mm/yy"
    });
}

// Edit payment modal to display payment information
async function PaymentModalForUser(user_id) 
{
    // Get payment form elements
    let user = await API_GetUserById(user_id);

    var current_date = date.getDate() + "/" + (date.getMonth() + 1) + "/" + date.getFullYear();

    $("#pay-userid").val(user["id"]);
    $("#pay-name").val(user["name"]);
    $("#pay-date").val(current_date);
    $("#pay-confirm").click(SaveUserPayment);
    
    $("#PaymentModal").modal("show");
    
}

async function SaveUserPayment() 
{

    let user_data = JSON.stringify({
        user_id : $("#pay-userid").val(),
        date    : $("#pay-date").val(),
        value   : $("#pay-value").val(),
        discount: $("#pay-discount").val()
    });
    
    await  API_UserPaymentCommit(user_data);

    $("#PaymentModal").modal("hide");
    location.reload();
}

// Customize edit modal to display user information and payments
async function EditModalForUser(user_id) 
{
    console.log(user_id);
    if (typeof user_id !== "undefined")
    {
       let user = await API_GetUserById(user_id);

        $("#EditModal-title").text("EDIT");
        $("#edit-userid").val(user["id"]);
        $("#edit-name").val(user["name"]);
        $("#edit-email").val(user["email"]);
        $("#edit-area").val(user["area"]);

        $("#edit-confirm").unbind('click');
        $("#edit-confirm").click(SaveUserEdit); 
    }
    else // Show add modal
    {
        $("#EditModal-title").text("ADD NEW USER");
        $("#edit-userid").val("");
        $("#edit-name").val("");
        $("#edit-email").val("");
        $("#edit-area").val("");

        $("#edit-confirm").unbind('click');
        $("#edit-confirm").click(AddNewUser);
    }
    
    $("#EditModal").modal("show");
    
}

async function SaveUserEdit() 
{

    let user_data = JSON.stringify({
        id      : $("#edit-userid").val(),
        name    : $("#edit-name").val(),
        email   : $("#edit-email").val(),
        area    : $("#edit-area").val() 
    });

    await API_UserEditCommit(user_data);

    $("#EditModal").modal("hide");
    location.reload();
}

async function AddNewUser() 
{

    let user_data = JSON.stringify({
        name    : $("#edit-name").val(),
        email   : $("#edit-email").val(),
        area    : $("#edit-area").val() 
    });

    await API_NewUserCommit(user_data);

    $("#EditModal").modal("hide");
    location.reload();

}

async function RemoveUserById(user_id)
{
    if (confirm("Do you really want to remove this user?"))
    {    
        await API_RemoveUserById(user_id);
        window.location.reload();
    }
}

async function EditGroupInfo()
{
    let modal = await API_GetModal("coffee");

    $(modal["html"]).appendTo("body");
    $("#CoffeeModal").modal("show");

    $('#CoffeeModal').on('hidden.bs.modal', function (e) {
        $("#CoffeeModal").remove();
      })

}

async function IncomeReportByMonth()
{
    let month_num = parseInt($("#cash-income-filter").val());

    console.log(month_num);

    let report = await API_GetReport("income", month_num);
    console.log(report); 

    $(report["html"]).appendTo("body");
    $("#ReportModal").modal("show");

    $('#ReportModal').on('hidden.bs.modal', function (e) {
        $("#ReportModal").remove();
      })

}

async function SpentReportByMonth()
{
    let month_num = parseInt($("#cash-spent-filter").val());

    console.log(month_num);

    let report = await API_GetReport("spent", month_num);
    console.log(report); 

    $(report["html"]).appendTo("body");
    $("#ReportModal").modal("show");

    $('#ReportModal').on('hidden.bs.modal', function (e) {
        $("#ReportModal").remove();
      })

}

async function TotalCashReportByMonth()
{
    let month_num = parseInt($("#cash-total-filter").val());

    console.log(month_num);

    let report = await API_GetReport("total", month_num);
    console.log(report); 

    $(report["html"]).appendTo("body");
    $("#ReportModal").modal("show");

    $('#ReportModal').on('hidden.bs.modal', function (e) {
        $("#ReportModal").remove();
      })

}

// Get all buttons of the collapsable rows to bind the event listeners
function row_buttons_events() 
{
    let rows_id = document.getElementsByClassName("col-id");
    
    for (let index = 0; index < rows_id.length; index++) {
        let user_id = rows_id[index].innerHTML.trim();
        
        var ShowPayModal_Event = function(){ PaymentModalForUser(user_id) };
        var ShowPaymentsModal_Event = function(){ PaymentsModalForUser(user_id)}
        var ShowEditModal_Event = function(){ EditModalForUser(user_id) };
        var RemoveUser = function() { RemoveUserById(user_id) };

        //Add event for each button in rows
        $("#pay-" + user_id).click(ShowPayModal_Event.bind(user_id));
        $("#payments-" + user_id).click(ShowPaymentsModal_Event.bind(user_id));
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

document.addEventListener('DOMContentLoaded', (event) => 
{
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
    $("#btn-purchase").click(OpenPurchaseModal);
    $("#pay-value").change(update_payment_total);
    $("#pay-discount").change(update_payment_total);
    $("#edit-coffee").click(EditGroupInfo);
    $("#cash-income-filter").change(IncomeReportByMonth);
    $("#cash-spent-filter").change(SpentReportByMonth);
    // Add event listeners
    row_buttons_events();

});