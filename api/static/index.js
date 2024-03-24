const accordion = document.querySelector('.accordion');
const categories = document.querySelectorAll('.category');
const dropdowns = document.querySelectorAll('.accordion-collapse');

accordion.addEventListener("dragover", initSortableList);

categories.forEach(item => {
    item.addEventListener("dragstart", () => {
        setTimeout(() => item.classList.add("dragging"), 0);
    });
    item.addEventListener("dragend", () => {
        item.classList.remove("dragging");
        sortDatabase();
    });
});

function initSortableList(e) {
    e.preventDefault()

    const draggingItem = accordion.querySelector(".dragging");
    const siblings = [...accordion.querySelectorAll(".category:not(.dragging)")];

    let nextSibling = siblings.find(sibling => {
        return e.clientY <= sibling.offsetTop + sibling.offsetHeight / 2;
    });

    accordion.insertBefore(draggingItem, nextSibling);
};

function toggle_visibility(category_id) {
    fetch('/toggle-visibility', {
        method: 'POST',
        body: JSON.stringify({ category_id: category_id })
    });
};

function sortDatabase() {
    const items = document.querySelectorAll(".accordion-item");

    var category_ids = []
    items.forEach(item => {
        category_ids.push(item.getAttribute("id"))
    });

    fetch('/sort-database', {
        method: 'POST',
        body: JSON.stringify({ category_ids: category_ids })
    });
};

function delete_assignment(assignment_id) {
    fetch('/delete-assignment', {
        method: 'POST',
        body: JSON.stringify({ assignment_id: assignment_id })
    }).then((_res) => {
        window.location.href = "/";
    });
};

function delete_category(category_id) {
    fetch('/delete-category', {
        method: 'POST',
        body: JSON.stringify({ category_id: category_id })
    }).then((_res) => {
        window.location.href = "/";
    });
};