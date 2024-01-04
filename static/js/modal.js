const openModalBtn = document.querySelector('.open-modal')
const closeModalBtn = document.querySelector('.close-modal')
const modalOverlay = document.querySelector('.modal')

// opening the modal
function modalToggle() {
    modalOverlay.classList.toggle('is-open')
}

openModalBtn.addEventListener('click', modalToggle)
closeModalBtn.addEventListener('click', modalToggle)

// closing the modal
modalOverlay.addEventListener('click', e => {
    console.log('clicke', e.target)
    if (!e.target.closest('form')) {
        modalOverlay.classList.remove('is-open')
    }
})