
console.log('hello world');
let m = document.getElementById('m')
if (m && m.textContent.trim() ==='correct answer'){
console.log('correct');
for (let index = 0; index < 10; index++) {
     confetti({
        position: { x: Math.random()*1200 +300, y: Math.random()*900 +100 },	// Origin position
        count: 1000,			// Number of particles
        size: 1,			// Size of the particles
        velocity: 200,		// Initial particle velocity
        fade: false,			// Particles fall off the screen, or fade out
    });
}

}else if (m && m.textContent.trim() === 'wrong answer'){
     console.log('wrong');
     
}else if (m){
console.log('you a dum dum');

}else {
    console.log('something very wrong');
    
}
