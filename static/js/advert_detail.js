function addFormElements() {
    $('.form-list').append($("#form-template .form-row").clone())
}

function removeFormElements() {
    $(this).parents('.form-row').remove();
}

$(document).ready(addFormElements);
$(document).on("click", ".add-btn", addFormElements);
$(document).on("click", ".remove-btn", removeFormElements);

function showEstimate() {
    var x = document.getElementById("estimate");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}

const btn = document.getElementById('btn');

btn.addEventListener('click', function handleClick() {
    const initialText = 'HIDE ESTIMATION';

    if (btn.textContent.toLowerCase().includes(initialText.toLowerCase())) {
        btn.textContent = 'FORM TEAM';
    } else {
        btn.textContent = initialText;
    }
});
