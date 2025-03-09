const books = [
    { name: "Cosmos", image: "img/1.jpg", original_price: 25.00, damage_type: "corner_damage", severity: 2, damage_image: "img/1D.jpg", discounted_price: 15.00 },
    { name: "Pride and Prejudice", image: "img/2.jpg", original_price: 10.00, damage_type: "spine_damage", severity: 1, damage_image: "img/2D.jpg", discounted_price: 7.50 },
    { name: "The Lean Startup", image: "img/3.jpg", original_price: 30.00, damage_type: "corner_damage", severity: 3, damage_image: "img/3D.jpg", discounted_price: 18.99 },
    { name: "1984", image: "img/4.jpg", original_price: 12.00, damage_type: "water_damage", severity: 2, damage_image: "img/4D.jpg", discounted_price: 10.20 },
    { name: "The 7 Habits of highly effective people", image: "img/5.jpg", original_price: 15.00, damage_type: "corner_damage", severity: 1, damage_image: "img/5D.jpg", discounted_price: 12.70 },
    { name: "Sapiens", image: "img/6.jpg", original_price: 28.00, damage_type: "missing_dust_jacket", severity: 3, damage_image: "img/6D.jpg", discounted_price: 22.40 },
    { name: "To Kill a Mockingbird", image: "img/7.jpg", original_price: 11.00, damage_type: "corner_damage", severity: 2, damage_image: "img/7D.jpg", discounted_price: 9.10 },
    { name: "The Innovator's Dilemma", image: "img/8.jpg", original_price: 32.00, damage_type: "cover_scratches", severity: 1, damage_image: "img/8D.jpg", discounted_price: 25.50 },
    { name: "The Lord of the Rings", image: "img/9.jpg", original_price: 20.00, damage_type: "corner_damage", severity: 4, damage_image: "img/9D.jpg", discounted_price: 17.90 },
    { name: "Zero to One", image: "img/10.jpg", original_price: 18.00, damage_type: "trim_issues", severity: 2, damage_image: "img/10D.jpg", discounted_price: 14.50 }
];

// Function to display books
function displayBooks(booksToShow) {
    const bookList = document.getElementById("book-list");
    bookList.innerHTML = ""; // Clear previous results

    booksToShow.forEach(book => {
        const bookDiv = document.createElement("div");
        bookDiv.classList.add("book-item");
        bookDiv.innerHTML = `
            <img src="${book.image}" alt="${book.name}" class = "book-cover">
            <h3>${book.name}</h3>
            <p class="original-price">$${book.original_price.toFixed(2)}</p>
            <p class="discounted-price">$${book.discounted_price.toFixed(2)}</p>
            <button class="damage-button" data-damage-image="${book.damage_image}">Show Damage</button>
            <img src="" alt="Damage Image" class="damage-image" style="display: none;">
            <button class="buy-button">Add to Cart</button>
        `;
        bookList.appendChild(bookDiv);
    });
}

// Initial display
displayBooks(books);

// Function to apply the image display and add to cart, it will pop up when the image is active.
document.getElementById("book-list").addEventListener("click", function(event) {
    if (event.target.classList.contains("damage-button")) {
        const button = event.target;
        const damageImageSrc = button.dataset.damageImage;
        const bookDiv = button.closest(".book-item");
        const damageImage = bookDiv.querySelector(".damage-image");

        if (damageImage.style.display === "none") {
            damageImage.src = damageImageSrc;
            damageImage.style.display = "block";
            button.textContent = "Hide Damage";
        } else {
            damageImage.src = ""; // Clear the image source
            damageImage.style.display = "none";
            button.textContent = "Show Damage";
        }
    }
});

// Filter logic
document.getElementById("apply-filter").addEventListener("click", function() {
    const maxDamage = parseInt(document.getElementById("max-damage").value);
    const filteredBooks = books.filter(book => book.severity <= maxDamage);
    displayBooks(filteredBooks);
});