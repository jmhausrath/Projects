let money = 0;
let rods = 1;
let maxRods = 10;
let fishPool = [
    { name: 'Trout', count: 100, value: 5 },
    { name: 'Salmon', count: 100, value: 10 },
    { name: 'Tuna', count: 100, value: 15 },
    { name: 'Catfish', count: 100, value: 20 },
    { name: 'Bass', count: 100, value: 25 },
    { name: 'Cod', count: 100, value: 30 },
    { name: 'Snapper', count: 100, value: 35 },
    { name: 'Mackerel', count: 100, value: 40 },
    { name: 'Sardine', count: 100, value: 45 },
    { name: 'Swordfish', count: 100, value: 50 },
];

let caughtFish = [];  // This will hold the caught fish
let totalMoneyEarned = 0;  // Track total money earned
let totalFishInSea = fishPool.reduce((sum, fish) => sum + fish.count, 0);  // Track total fish in the sea
let uniqueSpeciesInSea = fishPool.filter(fish => fish.count > 0).length;  // Track number of species in the sea

console.log("Initial Total Fish in Sea:", totalFishInSea); // Should log 1000
console.log("Initial Unique Species in Sea:", uniqueSpeciesInSea); // Should log 10

let activeProgressBars = 0;

document.getElementById('cast-rod-btn').addEventListener('click', () => {
    if (activeProgressBars < rods) {
        castRod();
    }
});

document.getElementById('sell-fish-btn').addEventListener('click', () => {
    let totalValue = 0;
    caughtFish.forEach((fish) => {
        totalValue += fish.value;
    });

    money += totalValue;
    totalMoneyEarned += totalValue;  // Update total money earned
    caughtFish = [];  // All fish are sold, so clear the caught fish array

    // Update the fish pool after selling
    updateFishPool();

    updateUI();
});

document.getElementById('buy-rod-btn').addEventListener('click', () => {
    if (money >= 20 && rods < maxRods) {
        money -= 20;
        rods++;
        updateUI();
    }
});

function castRod() {
    activeProgressBars++;
    const progressBars = document.getElementById('progress-bars');
    const progressBar = document.createElement('div');
    progressBar.className = 'progress-bar';
    const progressFill = document.createElement('div');
    progressBar.appendChild(progressFill);
    progressBars.appendChild(progressBar);

    let progress = 0;
    const interval = setInterval(() => {
        progress += 2;
        progressFill.style.width = `${progress}%`;

        if (progress >= 100) {
            clearInterval(interval);
            progressBars.removeChild(progressBar);
            activeProgressBars--;

            catchFish();
            updateUI();
        }
    }, 100);
}

function catchFish() {
    const totalFish = fishPool.reduce((sum, fish) => sum + fish.count, 0);
    if (totalFish === 0) return;

    const random = Math.floor(Math.random() * totalFish);
    let cumulative = 0;

    for (const fish of fishPool) {
        cumulative += fish.count;
        if (random < cumulative) {
            // Move fish from the sea to the caught inventory
            fish.count--;
            caughtFish.push(fish);

            // Recalculate totalFishInSea and uniqueSpeciesInSea dynamically
            totalFishInSea = fishPool.reduce((sum, fish) => sum + fish.count, 0);
            uniqueSpeciesInSea = fishPool.filter(fish => fish.count > 0).length;

            break;
        }
    }
}

function updateFishPool() {
    fishPool.forEach((fish) => {
        if (fish.count === 0) {
            uniqueSpeciesInSea--;
        }
    });
}

function updateFishBar() {
    const fishBar = document.getElementById('fish-bar');
    fishBar.innerHTML = '';

    const totalFishInSea = fishPool.reduce((sum, fish) => sum + fish.count, 0);
    fishPool.forEach((fish) => {
        const fraction = totalFishInSea > 0 ? (fish.count / totalFishInSea) * 100 : 10;
        const barSegment = document.createElement('div');
        barSegment.style.backgroundColor = getFishColor(fish.name);
        barSegment.style.width = `${fraction}%`;
        fishBar.appendChild(barSegment);
    });
}

function updateUI() {
    document.getElementById('money').textContent = money;
    document.getElementById('rod-count').textContent = rods;

    const inventory = document.getElementById('fish-inventory');
    inventory.innerHTML = '';
    let totalValue = 0;

    // Group caught fish by species and display their count and value
    let caughtFishCount = {};
    caughtFish.forEach((fish) => {
        if (!caughtFishCount[fish.name]) {
            caughtFishCount[fish.name] = { count: 0, value: fish.value };
        }
        caughtFishCount[fish.name].count++;
    });

    // Display caught fish by species and their counts
    for (const fishName in caughtFishCount) {
        const fish = caughtFishCount[fishName];
        if (fish.count > 0) {
            const item = document.createElement('li');
            item.textContent = `${fishName} x${fish.count}, $${fish.value}`;
            inventory.appendChild(item);
            totalValue += fish.count * fish.value;
        }
    }
    let money = 0;
    let rods = 1;
    let maxRods = 10;
    let fishPool = [
        { name: 'Trout', count: 100, value: 5 },
        { name: 'Salmon', count: 100, value: 10 },
        { name: 'Tuna', count: 100, value: 15 },
        { name: 'Catfish', count: 100, value: 20 },
        { name: 'Bass', count: 100, value: 25 },
        { name: 'Cod', count: 100, value: 30 },
        { name: 'Snapper', count: 100, value: 35 },
        { name: 'Mackerel', count: 100, value: 40 },
        { name: 'Sardine', count: 100, value: 45 },
        { name: 'Swordfish', count: 100, value: 50 },
    ];
    
    let caughtFish = [];  // This will hold the caught fish
    let totalMoneyEarned = 0;  // Track total money earned
    let totalFishInSea = fishPool.reduce((sum, fish) => sum + fish.count, 0);  // Track total fish in the sea
    let uniqueSpeciesInSea = fishPool.filter(fish => fish.count > 0).length;  // Track number of species in the sea
    
    console.log("Initial Total Fish in Sea:", totalFishInSea); // Should log 1000
    console.log("Initial Unique Species in Sea:", uniqueSpeciesInSea); // Should log 10
    
    let activeProgressBars = 0;
    
    document.getElementById('cast-rod-btn').addEventListener('click', () => {
        if (activeProgressBars < rods) {
            castRod();
        }
    });
    
    document.getElementById('sell-fish-btn').addEventListener('click', () => {
        let totalValue = 0;
        caughtFish.forEach((fish) => {
            totalValue += fish.value;
        });
    
        money += totalValue;
        totalMoneyEarned += totalValue;  // Update total money earned
        caughtFish = [];  // All fish are sold, so clear the caught fish array
    
        // Update the fish pool after selling
        updateFishPool();
    
        updateUI();
    });
    
    document.getElementById('buy-rod-btn').addEventListener('click', () => {
        if (money >= 20 && rods < maxRods) {
            money -= 20;
            rods++;
            updateUI();
        }
    });
    
    function castRod() {
        activeProgressBars++;
        const progressBars = document.getElementById('progress-bars');
        const progressBar = document.createElement('div');
        progressBar.className = 'progress-bar';
        const progressFill = document.createElement('div');
        progressBar.appendChild(progressFill);
        progressBars.appendChild(progressBar);
    
        let progress = 0;
        const interval = setInterval(() => {
            progress += 2;
            progressFill.style.width = `${progress}%`;
    
            if (progress >= 100) {
                clearInterval(interval);
                progressBars.removeChild(progressBar);
                activeProgressBars--;
    
                catchFish();
                updateUI();
            }
        }, 100);
    }
    
    function catchFish() {
        const totalFish = fishPool.reduce((sum, fish) => sum + fish.count, 0);
        if (totalFish === 0) return;
    
        const random = Math.floor(Math.random() * totalFish);
        let cumulative = 0;
    
        for (const fish of fishPool) {
            cumulative += fish.count;
            if (random < cumulative) {
                // Move fish from the sea to the caught inventory
                fish.count--;
                caughtFish.push(fish);
    
                // Recalculate totalFishInSea and uniqueSpeciesInSea dynamically
                totalFishInSea = fishPool.reduce((sum, fish) => sum + fish.count, 0);
                uniqueSpeciesInSea = fishPool.filter(fish => fish.count > 0).length;
    
                break;
            }
        }
        updateUI(); // Update the UI after catching a fish
    }
    
    function updateFishPool() {
        fishPool.forEach((fish) => {
            if (fish.count === 0) {
                uniqueSpeciesInSea--;
            }
        });
    }
    
    function updateFishBar() {
        const fishBar = document.getElementById('fish-bar');
        fishBar.innerHTML = '';
    
        const totalFishInSea = fishPool.reduce((sum, fish) => sum + fish.count, 0);
        fishPool.forEach((fish) => {
            const fraction = totalFishInSea > 0 ? (fish.count / totalFishInSea) * 100 : 10;
            const barSegment = document.createElement('div');
            barSegment.style.backgroundColor = getFishColor(fish.name);
            barSegment.style.width = `${fraction}%`;
            fishBar.appendChild(barSegment);
        });
    }
    
    function updateUI() {
        document.getElementById('money').textContent = money;
        document.getElementById('rod-count').textContent = rods;
    
        const inventory = document.getElementById('fish-inventory');
        inventory.innerHTML = '';
        let totalValue = 0;
    
        // Group caught fish by species and display their count and value
        let caughtFishCount = {};
        caughtFish.forEach((fish) => {
            if (!caughtFishCount[fish.name]) {
                caughtFishCount[fish.name] = { count: 0, value: fish.value };
            }
            caughtFishCount[fish.name].count++;
        });
    
        // Display caught fish by species and their counts
        for (const fishName in caughtFishCount) {
            const fish = caughtFishCount[fishName];
            if (fish.count > 0) {
                const item = document.createElement('li');
                item.textContent = `${fishName} x${fish.count}, $${fish.value}`;
                inventory.appendChild(item);
                totalValue += fish.count * fish.value;
            }
        }
    
        document.getElementById('sell-value').textContent = totalValue;
        updateFishBar();
    
        // Display the new stats (Total Money Earned, Total Fish in Sea, Unique Species in Sea)
        document.getElementById('total-money-earned').textContent = `Total Earned: $${totalMoneyEarned}`;
        document.getElementById('total-fish-in-sea').textContent = `Fish Remaining: ${totalFishInSea}`;
        document.getElementById('unique-species-in-sea').textContent = `Species Remaining: ${uniqueSpeciesInSea}`;
    }
    
    function getFishColor(name) {
        const colors = [
            '#ff9999', '#ffcc99', '#ffff99', '#ccff99', '#99ff99',
            '#99ffff', '#99ccff', '#9999ff', '#cc99ff', '#ff99cc',
        ];
        return colors[fishPool.findIndex((fish) => fish.name === name)];
    }
    
    updateUI();
    
    document.getElementById('sell-value').textContent = totalValue;
    updateFishBar();

    // Display the new stats (Total Money Earned, Total Fish in Sea, Unique Species in Sea)
    document.getElementById('total-money-earned').textContent = `Total Earned: $${totalMoneyEarned}`;
    document.getElementById('total-fish-in-sea').textContent = `Fish Remaining: ${totalFishInSea}`;
    document.getElementById('unique-species-in-sea').textContent = `Species Remaining: ${uniqueSpeciesInSea}`;
}

function getFishColor(name) {
    const colors = [
        '#ff9999', '#ffcc99', '#ffff99', '#ccff99', '#99ff99',
        '#99ffff', '#99ccff', '#9999ff', '#cc99ff', '#ff99cc',
    ];
    return colors[fishPool.findIndex((fish) => fish.name === name)];
}

updateUI();
