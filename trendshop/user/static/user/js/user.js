function getResponseForSignup() {
    getToasterMessage("success", "Signed Up Successfully");
    setTimeout(function() {
    $("#signup").submit();
    }, 1000);
}

function getResponseForLogin() {
    getToasterMessage("success", "Logged In Successfully");
    setTimeout(function() {
    $("#login").submit();
    }, 1000);
}

function getResponseForProfileUpdate() {
    getToasterMessage("success", "Profile Updated Successfully");
    setTimeout(function() {
    $("#updateProfile").submit();
    }, 1000);
}

function getResponseForAddressUpdate() {
    setTimeout(function() {
    $("#updateAddress").submit();
    }, 1000);
}

