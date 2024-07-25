document.addEventListener('DOMContentLoaded', function() {
  var form = document.getElementById('signupForm');
  form.addEventListener('submit', function(event) {
    event.preventDefault();
    if (validatePassword() && checkForEmptyField() && validatePhoneNumber()) {
      this.submit();
    }
  });

  function validatePassword() {
    var password = document.getElementById('password').value;
    var confirmPassword = document.getElementById('password_confirm').value;
    var passwordError = document.getElementById('password-error');

    if (password !== confirmPassword) {
      passwordError.textContent = 'Passwords do not match';
      return false;
    } else {
      passwordError.textContent = '';
      return true;
    }
  }

  function checkForEmptyField() {
    var firstName = document.getElementById("first_name").value;
    var lastName = document.getElementById("last_name").value;
    var email = document.getElementById("email").value;
    var phoneNumber = document.getElementById("phone_number").value;
    var gender = document.getElementById('gender').value;
    

    var firstNameError = document.getElementById('fname-error');
    var lastNameError = document.getElementById('lname-error');
    var emailError = document.getElementById('email-error');
    var phoneError = document.getElementById('phone-error');
    var genderError = document.getElementById('gender-error');

    let isValid = true;

    if (firstName.trim() === '') {
      firstNameError.textContent = "Please enter your first name";
      isValid = false;
    } else {
      firstNameError.textContent = '';
    }

    if (lastName.trim() === '') {
      lastNameError.textContent = "Please enter your last name";
      isValid = false;
    } else {
      lastNameError.textContent = '';
    }

    if (email.trim() === '') {
      emailError.textContent = "Please enter your email";
      isValid = false;
    } else {
      emailError.textContent = '';
    }

    if (phoneNumber.trim() === '') {
      phoneError.textContent = "Please enter your phone number";
      isValid = false;
    } else {
      phoneError.textContent = '';
    }

    if (gender === '') {
        genderError.textContent = 'Please select your gender';
        isValid = false;
    } else {
        genderError.textContent = '';
    }

    return isValid;
  }

  function validatePhoneNumber() {
    var phoneNumber = document.getElementById('phone_number').value;
    var phoneError = document.getElementById('phone-error');

    // Remove all non-digit characters
    var cleanedNumber = phoneNumber.replace(/\D/g, '');

    // Validate for 10-digit length or 12-digit length with country code
    if (cleanedNumber.length !== 10 && cleanedNumber.length !== 12) {
        phoneError.textContent = 'Please enter a valid 10 digit phone number';
        return false;
    }

    // Validate 10 digits
    if (cleanedNumber.length === 10 && !/^[6789]\d{9}$/.test(cleanedNumber)) {
        phoneError.textContent = 'Please enter a valid 10-digit mobile number';
        return false;
    }

    phoneError.textContent = '';
    return true;
}
});
