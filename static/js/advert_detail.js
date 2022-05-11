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
    var y = document.getElementById("main");
    var width = y.style.width
    if (x.style.display === "none") {
        x.style.display = "block";
        x.style.width = "350px";
        y.style.width = width - '350px';
    } else {
        x.style.display = "none";
         x.style.width = "0";
         y.style.marginRight = "0";
    }
}

const btn = document.getElementById('btn');

btn.addEventListener('click', function handleClick() {
    const initialText = 'Скрити';

    if (btn.textContent.toLowerCase().includes(initialText.toLowerCase())) {
        btn.textContent = 'Сформувати команду';
    } else {
        btn.textContent = initialText;
    }
});
