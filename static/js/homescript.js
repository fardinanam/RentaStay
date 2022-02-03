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
            const title = card.querySelector("[house-name]")
            const address = card.querySelector("[house-address]")
            const button = card.querySelector("[button]")

            title.textContent = house.HOUSE_NAME
            address.textContent = house.CITY_NAME + ', ' + house.COUNTRY_NAME
            button.onclick = function() {
                location.href = "/house/?houseId=" + house.HOUSE_ID
            }

            houseCardsContainer.append(card)

            return {name: house.HOUSE_NAME, 
                    address: house.CITY_NAME + ', ' + house.COUNTRY_NAME,
                    element: card}
        })
    })