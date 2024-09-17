// Wait for the SVG to load before adding event listeners
document.getElementById('svg-map').addEventListener('load', function () {
  const svgDoc = this.contentDocument;  // Access the inner SVG document
  const cities = ['newyork', 'la', 'chicago']; // List of city IDs in the SVG

  cities.forEach(cityId => {
    const cityElement = svgDoc.getElementById(cityId);

    // Check if the cityElement exists in the SVG before adding event listeners
    if (cityElement) {
      // Add hover event to display city name
      cityElement.addEventListener('mouseover', function() {
        document.getElementById('selected-city-name').textContent = cityId.charAt(0).toUpperCase() + cityId.slice(1).replace(/_/g, ' ');
      });

      // Add click event to handle city clicks
      cityElement.addEventListener('click', function() {
        alert('City clicked: ' + cityId);
      });
    } else {
      console.error(`City element with ID ${cityId} not found in the SVG.`);
    }
  });
});
