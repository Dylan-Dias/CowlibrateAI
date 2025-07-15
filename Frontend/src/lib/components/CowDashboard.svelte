<script>
  import 'carbon-components-svelte/css/g10.css';
  import { Grid, Row, Column, Tile } from 'carbon-components-svelte';
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';

  let ApexCharts;
  let pieChart, barChart, lineChart;

  let pieChartContainer;
  let barChartContainer;
  let lineChartContainer;

  // Initial options (will be updated dynamically)
  const pieOptions = {
    chart: { type: 'pie', height: 300 },
    labels: [],  // start empty, will fill from API
    legend: { position: 'bottom' },
    responsive: [{ breakpoint: 480, options: { chart: { width: 300 } } }],
  };

  const barOptions = {
    chart: { id: 'milk-yield', type: 'bar', height: 300 },
    xaxis: { categories: [] }, // fill dynamically
    title: { text: 'Milk Yield (Liters)', align: 'center' },
  };

  const lineOptions = {
    chart: { id: 'feed-efficiency', type: 'line', height: 300 },
    xaxis: { categories: [] }, // fill dynamically
    stroke: { curve: 'smooth' },
    title: { text: 'Feed Efficiency (%)', align: 'center' },
  };

  onMount(async () => {
    const module = await import('apexcharts');
    ApexCharts = module.default;

    pieChart = new ApexCharts(pieChartContainer, { ...pieOptions, series: [] });
    await pieChart.render();

    barChart = new ApexCharts(barChartContainer, { ...barOptions, series: [] });
    await barChart.render();

    lineChart = new ApexCharts(lineChartContainer, { ...lineOptions, series: [] });
    await lineChart.render();

    await fetchOptimizedData(); // Fetch data and update charts dynamically
  });

 async function fetchOptimizedData() {
  try {
    const res = await fetch('http://localhost:8080/api/optimize-run/cows'); // full backend URL
    if (!res.ok) throw new Error('Network response was not ok');

    const data = await res.json();

    // Normalize breed strings to lowercase for counting
    const breedCounts = {};
    data.selected_cows.forEach(cow => {
      const breedNormalized = cow.breed.toLowerCase();
      breedCounts[breedNormalized] = (breedCounts[breedNormalized] || 0) + 1;
    });

    // Capitalize first letter for display labels
    const pieLabels = Object.keys(breedCounts).map(
      b => b.charAt(0).toUpperCase() + b.slice(1)
    );
    const pieSeries = Object.values(breedCounts);

    // Example bar chart: average milk yield for placeholder months
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'];
    const avgMilkYield = data.selected_cows.reduce((sum, c) => sum + c.milk_yield, 0) / data.selected_cows.length;
    const milkYields = months.map(() => parseFloat(avgMilkYield.toFixed(2)));

    // Dummy feed efficiency data for line chart
    const weeks = ['Week 1', 'Week 2', 'Week 3', 'Week 4'];
    const feedEfficiency = [75, 78, 80, 85];

    // Update charts
    if (pieChart) {
      pieChart.updateOptions({ labels: pieLabels });
      pieChart.updateSeries(pieSeries);
    }
    if (barChart) {
      barChart.updateOptions({ xaxis: { categories: months } });
      barChart.updateSeries([{ name: 'Milk Yield', data: milkYields }]);
    }
    if (lineChart) {
      lineChart.updateOptions({ xaxis: { categories: weeks } });
      lineChart.updateSeries([{ name: 'Feed Efficiency', data: feedEfficiency }]);
    }
  } catch (error) {
    console.error('Failed to fetch or update charts:', error);
  }
}


  function navigateTo(path) {
    goto(path);
  }
</script>

<nav class="nav-bar">
  <div class="brand">Bovine Analytics & Insights</div>
  <ul class="nav-links">
    <li><button on:click={() => navigateTo('/dashboard/cow')}>Dairy Input</button></li>
  </ul>
</nav>

<Grid>
  <Row>
    <Column sm="4" md="4" lg="4">
      <Tile>
        <h2>Breed Distribution</h2>
        <div bind:this={pieChartContainer} class="chart-container"></div>
      </Tile>
    </Column>

    <Column sm="4" md="4" lg="4">
      <Tile>
        <h2>Milk Yield (Monthly)</h2>
        <div bind:this={barChartContainer} class="chart-container"></div>
      </Tile>
    </Column>

    <Column sm="4" md="4" lg="4">
      <Tile>
        <h2>Feed Efficiency</h2>
        <div bind:this={lineChartContainer} class="chart-container"></div>
      </Tile>
    </Column>
  </Row>
</Grid>

<style>
  /* Nav Bar */
  .nav-bar {
    display: flex;
    align-items: center;
    background-color: #3949ab;
    padding: 0.75rem 1.5rem;
    color: white;
    font-weight: 700;
  }

  .brand {
    flex-grow: 1;
    font-size: 1.25rem;
  }

  .nav-links {
    list-style: none;
    display: flex;
    gap: 1rem;
    margin: 0;
    padding: 0;
  }

  .nav-links button {
    background: transparent;
    border: none;
    color: white;
    cursor: pointer;
    font-size: 1rem;
    font-weight: 600;
    padding: 0.5rem 1rem;
    border-radius: 6px;
    transition: background-color 0.25s ease;
  }

  .nav-links button:hover {
    background-color: #5561f0;
  }

  /* Tiles */
  :global(.bx--tile) {
    padding: 1rem 1.5rem;
  }

  h2 {
    font-size: 1.25rem;
    margin-bottom: 1rem;
    color: var(--cds-text-primary);
    font-weight: 600;
  }

  .chart-container {
    width: 100%;
    height: 300px;
    min-height: 300px;
    background-color: var(--cds-layer);
    border-radius: 8px;
    box-shadow: inset 0 0 8px rgba(0, 0, 0, 0.05);
  }

  /* Responsive adjustments */
  @media (max-width: 600px) {
    .chart-container {
      height: 250px;
      min-height: 250px;
    }

    h2 {
      font-size: 1.1rem;
    }
  }
</style>
