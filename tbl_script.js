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

  const svgObject = document.getElementById('svg-map'); // Get the SVG object

  // Wait for the SVG to load
  svgObject.addEventListener('load', function () {
    const svgDoc = svgObject.contentDocument; // Get the inner document of the SVG
    const svgRoot = svgDoc.querySelector('svg'); // Access the SVG root

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
  });
}

// Load the cities when the SVG map is ready
addCitiesToMap();
