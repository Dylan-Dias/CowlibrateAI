<script>
  import 'carbon-components-svelte/css/g10.css';
  import { Grid, Row, Column, Tile } from 'carbon-components-svelte';
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';

  let ApexCharts;
  let pieChart, barChart, lineChart;

  // Chart options and series
  const pieOptions = {
    chart: { type: 'pie', height: 300 },
    labels: ['Goats', 'Cows', 'Sheep'],
    legend: { position: 'bottom' },
    responsive: [{ breakpoint: 480, options: { chart: { width: 300 } } }],
  };
  const pieSeries = [44, 55, 41];

  const barOptions = {
    chart: { id: 'milk-yield', type: 'bar', height: 300 },
    xaxis: { categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'] },
    title: { text: 'Milk Yield (Liters)', align: 'center' },
  };
  const barSeries = [{ name: 'Milk Yield', data: [30, 40, 35, 50, 49, 60] }];

  const lineOptions = {
    chart: { id: 'feed-efficiency', type: 'line', height: 300 },
    xaxis: { categories: ['Week 1', 'Week 2', 'Week 3', 'Week 4'] },
    stroke: { curve: 'smooth' },
    title: { text: 'Feed Efficiency (%)', align: 'center' },
  };
  const lineSeries = [{ name: 'Efficiency', data: [75, 78, 80, 85] }];

  onMount(async () => {
    const module = await import('apexcharts');
    ApexCharts = module.default;

    pieChart = new ApexCharts(document.querySelector('#pieChart'), {
      ...pieOptions,
      series: pieSeries,
    });
    pieChart.render();

    barChart = new ApexCharts(document.querySelector('#barChart'), {
      ...barOptions,
      series: barSeries,
    });
    barChart.render();

    lineChart = new ApexCharts(document.querySelector('#lineChart'), {
      ...lineOptions,
      series: lineSeries,
    });
    lineChart.render();
  });

  function navigateTo(path) {
    goto(path);
  }
</script>

<nav class="nav-bar">
  <div class="brand">Goat Analytics & Insights</div>
  <ul class="nav-links">
    <li><button on:click={() => navigateTo('/dashboard/goat')}>Dairy Input</button></li>
  </ul>
</nav>

<Grid>
  <Row>
    <Column sm="4" md="4" lg="4">
      <Tile>
        <h2>Breed Distribution</h2>
        <div id="pieChart" class="chart-container"></div>
      </Tile>
    </Column>

    <Column sm="4" md="4" lg="4">
      <Tile>
        <h2>Milk Yield (Monthly)</h2>
        <div id="barChart" class="chart-container"></div>
      </Tile>
    </Column>

    <Column sm="4" md="4" lg="4">
      <Tile>
        <h2>Feed Efficiency</h2>
        <div id="lineChart" class="chart-container"></div>
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
