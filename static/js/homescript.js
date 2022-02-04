const houseCardTemplate = document.querySelector("[house-card-template]")
const houseCardsContainer = document.querySelector("[house-cards-container]")
const searchInput = document.querySelector("[houses-search]")

let houses = []

searchInput.addEventListener("input", e => {
    const value = e.target.value.toLowerCase().trim()

    houses.forEach(house => {
        const isVisible = house.name.toLowerCase().includes(value) || 
                        house.address.toLowerCase().includes(value)
        house.element.classList.toggle("hide", !isVisible)
    })
})

fetch("/housesdata/")
    .then(response => response.json())
    .then(data => {
        houses = data.data.map(house => {
            const card = houseCardTemplate.content.cloneNode(true).children[0]
            const carouselSlide = card.querySelector("[carousel-slide]")
            const cardBody = card.querySelector("[card-body]")
            const title = card.querySelector("[house-name]")
            const address = card.querySelector("[house-address]")
            const image = card.querySelector("[house-image]")

            carouselSlide.id = "carousel" + house.HOUSE_ID
            
            card.querySelectorAll("[data-bs-target]").forEach(element => {
                element.setAttribute("data-bs-target", "#carousel" + house.HOUSE_ID)
            })
            
            title.textContent = house.HOUSE_NAME
            address.textContent = house.CITY_NAME + ', ' + house.COUNTRY_NAME
            
            if(house.PHOTOS_PATH)
                image.src = house.PHOTOS_PATH
            else
            {
                image.src = '../static/img/home-6.jpg'
            }
                
            cardBody.onclick = function() {
                location.href = "/house/?houseId=" + house.HOUSE_ID
            }

            houseCardsContainer.append(card)

            return {name: house.HOUSE_NAME, 
                    address: house.CITY_NAME + ', ' + house.COUNTRY_NAME,
                    element: card}
        })

        $('.carousel').carousel({
            interval: false,
        });
    })