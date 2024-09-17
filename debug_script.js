// Function to load city data from an external JSON file
async function loadCityData() {
  try {
    const response = await fetch('http://localhost:8000/cities.json'); // Path to your JSON file
    const cityData = await response.json();
    return cityData.cities; // Assuming 'cities' is the key in the JSON
  } catch (error) {
    console.error('Error loading city data:', error);
    return [];
  }
}

// Function to dynamically create and append city circles to the SVG
async function addCitiesToMap() {
  const cities = await loadCityData();

  // Access the SVG element inside the object tag
  const svgMap = document.getElementById('svg-map').contentDocument;
  if (!svgMap) {
    console.error('SVG content is not loaded yet.');
    return false; // Return false if not ready
  }

  const svgRoot = svgMap.querySelector('svg'); // Accessing the SVG root
  if (!svgRoot) {
    console.error('SVG root not found');
    return false; // Return false if not ready
  }

  // Iterate through cities and create circles for each
  cities.forEach(city => {
    const cityCircle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    cityCircle.setAttribute('class', 'city');
    cityCircle.setAttribute('id', city.id);
    cityCircle.setAttribute('cx', city.cx);
    cityCircle.setAttribute('cy', city.cy);
    cityCircle.setAttribute('r', 5); // Default radius
    cityCircle.setAttribute('fill', 'blue');

    // Append the circle to the SVG root
    svgRoot.appendChild(cityCircle);

    // Optionally, add event listeners for interaction (hover, click)
    cityCircle.addEventListener('mouseover', () => {
      document.getElementById('selected-city-name').textContent = city.name;
    });

    cityCircle.addEventListener('click', () => {
      alert(`City clicked: ${city.name}`);
    });
  });

  return true; // Return true when the SVG is ready and circles are added
}

// Polling function to ensure SVG is loaded
function pollSVGLoad() {
  const svgMap = document.getElementById('svg-map').contentDocument;
  if (svgMap && svgMap.querySelector('svg')) {
    const success = addCitiesToMap(); // Try adding the cities

    // If successfully added, stop polling
    if (success) {
      console.log('SVG loaded and cities added.');
      return; // Stop polling
    }
  }

  console.log('Waiting for SVG to load...');
  setTimeout(pollSVGLoad, 100); // Poll every 100ms until SVG is ready
}

// Initiate polling to check when the SVG is fully loaded
pollSVGLoad();
