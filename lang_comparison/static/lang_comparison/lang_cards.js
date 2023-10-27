// window.scroll({
//     top: 0, 
//     left: 0, 
//     behavior: 'smooth'
//   });

//   window.scrollBy({ 
//     top: 100, // could be negative value
//     left: 0, 
//     behavior: 'smooth' 
//   });

//   document.querySelector('.hello').scrollIntoView({ 
//     behavior: 'smooth' 
//   });
function myFunction() {
    alert("Hello from a static file!");
  }
  

let activeIndex = 0;

const cards = document.getElementsByClassName("card");

const enterLang = () => {
//bump active index to move things around
    const nextIndex = activeIndex + 1 <= cards.length - 1 ? activeIndex + 1 : 0;

    const currentCard = document.querySelector('[data-index="${activeIndex}"]'),
            nextCard = document.querySelector('[data-index="${nextIndex}"]');
    nextCard.dataset.status = "active";

    currentCard.dataset.status = "after";
    activeIndex = nextIndex;
}
            

