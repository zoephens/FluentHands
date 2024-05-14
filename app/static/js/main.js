document.addEventListener("DOMContentLoaded", function() {
    const roleSelect = document.getElementById("role-select");
    
    roleSelect.addEventListener("change", function() {
        if (roleSelect.value !== "") {
            roleSelect.classList.remove("placeholder-selected");
        } else {
            roleSelect.classList.add("placeholder-selected");
        }
    });
});
