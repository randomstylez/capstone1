
nav_items = document.querySelectorAll(".nav-ref");

nav_items.forEach(item => {
    item.addEventListener("click",function(){
        reset_nav_elements();
        this.classList.add("active");//adding active tab to class that was selected
    } );
});

function reset_nav_elements (){
    nav_items.forEach(item => {
        item.classList.remove("active");
    });
}